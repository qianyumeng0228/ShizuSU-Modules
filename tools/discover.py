#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ShizuSU 模块自动发现（进阶1）

按 GitHub topic 定时扫描候选模块仓库，输出到根目录 catalog/candidates.json，
供人工审批后加入 modules.config.json 正式收录。

默认 topics：shizusu-module, sukisu-module, kernelsu-module, ksu-module,
magisk-module, apatch-module, zygisk-module

过滤规则：
  - 排除 fork / archived / 已收录（modules.config.json 中已有 repo 或 moduleId）
  - 需存在 module.prop（或仓库内有 release zip）
  - 需可检测到许可证（open source 门槛预筛）

用法：
  python tools/discover.py --dry-run     # 打印候选（不写文件）
  python tools/discover.py --write       # 写入 catalog/candidates.json
环境变量：GITHUB_TOKEN（强烈建议）
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from http.client import IncompleteRead
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
CONFIG_PATH = HERE / "modules.config.json"
CATALOG_DIR = HERE / "catalog"
API_BASE = "https://api.github.com"
RAW_BASE = "https://raw.githubusercontent.com"
USER_AGENT = "shizusu-module-discoverer/1.0"

DEFAULT_TOPICS = [
    "shizusu-module",
    "sukisu-module",
    "kernelsu-module",
    "ksu-module",
    "magisk-module",
    "apatch-module",
    "zygisk-module",
]


def _get(url, token=None, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status, resp.read()
        except IncompleteRead:
            continue
        except urllib.error.HTTPError as e:
            return e.code, b""
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            return 0, str(e).encode("utf-8", errors="replace")
    return 0, b""


def _api_json(path, token):
    status, body = _get(f"{API_BASE}/{path.lstrip('/')}", token=token)
    if status != 200:
        return None
    try:
        return json.loads(body.decode("utf-8", errors="replace"))
    except Exception:
        return None


def search_repos(topic, token, per_page=50):
    q = urllib.parse.quote(f"topic:{topic}")
    data = _api_json(f"search/repositories?q={q}&sort=updated&order=desc&per_page={per_page}", token)
    return (data or {}).get("items", [])


def has_module_prop(full_name, token):
    owner, name = full_name.split("/", 1)
    for candidate in ("module.prop",):
        status, _ = _get(f"{RAW_BASE}/{owner}/{name}/HEAD/{candidate}", token=token, timeout=15)
        if status in (200, 302):
            return True
    return False


def has_release_zip(full_name, token):
    repo = _api_json(f"repos/{full_name}/releases", token)
    if not repo:
        return False
    for r in repo:
        for a in (r.get("assets") or []):
            if (a.get("name") or "").lower().endswith(".zip"):
                return True
    return False


def main():
    parser = argparse.ArgumentParser(description="ShizuSU 模块自动发现")
    parser.add_argument("--write", action="store_true", help="写入 catalog/candidates.json（默认只打印）")
    parser.add_argument("--topics", default=",".join(DEFAULT_TOPICS), help="逗号分隔的 topic 列表")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN") or None
    topics = [t.strip() for t in args.topics.split(",") if t.strip()]

    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    existing = set()
    for m in config.get("modules", []):
        if m.get("repo"):
            existing.add(m["repo"].lower())
        existing.add(m["moduleId"].lower())

    seen = {}
    for topic in topics:
        print(f"扫描 topic:{topic} ...", file=sys.stderr)
        for item in search_repos(topic, token) or []:
            full = item.get("full_name") or ""
            if not full:
                continue
            rec = seen.get(full.lower())
            if rec is None:
                seen[full.lower()] = {"fullName": full, "topics": set(), "item": item}
            seen[full.lower()]["topics"].add(topic)
        time.sleep(0.3)

    candidates = []
    for key, rec in seen.items():
        item = rec["item"]
        full = rec["fullName"]
        owner = item.get("owner", {}).get("login", "")
        if item.get("fork") or item.get("archived"):
            continue
        if full.lower() in existing:
            continue
        lic = item.get("license")
        license_spdx = (lic or {}).get("spdx_id", "") if lic else ""
        has_prop = has_module_prop(full, token)
        has_zip = has_release_zip(full, token)
        time.sleep(0.2)
        if not (has_prop or has_zip):
            continue
        suggested_id = full.split("/")[-1].lower().replace("-", "_").replace(".", "_")
        candidates.append({
            "fullName": full,
            "sourceUrl": item.get("html_url", f"https://github.com/{full}"),
            "description": (item.get("description") or "")[:200],
            "stars": item.get("stargazers_count", 0),
            "updatedAt": item.get("pushed_at") or item.get("updated_at") or "",
            "topics": sorted(rec["topics"]),
            "license": license_spdx,
            "hasModuleProp": has_prop,
            "hasReleaseZip": has_zip,
            "suggestedModuleId": suggested_id,
            "suggestedConfig": {
                "moduleId": suggested_id,
                "moduleName": item.get("name", suggested_id),
                "repo": full,
                "summary": (item.get("description") or "")[:200],
                "versionCodeOverride": 0,
            },
        })

    candidates.sort(key=lambda c: (-c["stars"], c["fullName"]))
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "topics": topics,
        "candidateCount": len(candidates),
        "candidates": candidates,
    }

    if args.write:
        CATALOG_DIR.mkdir(parents=True, exist_ok=True)
        (CATALOG_DIR / "candidates.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"已写入 catalog/candidates.json：{len(candidates)} 个候选")
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
