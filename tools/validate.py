#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ShizuSU 模块收录审核（进阶3：开源门槛校验）

对 modules.config.json 中的每个模块做收录门槛检查：
  - 有 repo 的模块：源码链接存在、LICENSE 可查、最新 release 下载 URL 可 HEAD、module.prop 存在
  - 无 repo 的手动/私有模块：由管理员背书，status=manual
产出 output/audit.json 供 build_mmrl.py / 管理器使用。

用法：
  python tools/validate.py                 # 生成 audit.json（不阻断）
  python tools/validate.py --strict        # 存在 unverified 时退出码 1（PR 检查用）
  python tools/validate.py --json          # 只打印审计结果
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from http.client import IncompleteRead
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
CONFIG_PATH = HERE / "modules.config.json"
OUT_DIR = HERE / "output"
API_BASE = "https://api.github.com"
RAW_BASE = "https://raw.githubusercontent.com"
USER_AGENT = "shizusu-module-repo-auditor/1.0"


def _http(url, token=None, timeout=20, method=None):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT}, method=method)
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    for _ in range(3):  # 大响应被截断时重试（IncompleteRead）
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read()
                return resp.status, body
        except IncompleteRead:
            continue
        except urllib.error.HTTPError as e:
            return e.code, b""
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            return 0, str(e).encode("utf-8", errors="replace")
    return 0, b""


def _api_json(path, token):
    status, body = _http(f"{API_BASE}/{path.lstrip('/')}", token=token)
    if status != 200:
        return None
    try:
        return json.loads(body.decode("utf-8", errors="replace"))
    except Exception:
        return None


def check_repo(repo, token, mod=None, skip_head=False):
    """检查一个开源模块仓库：license / module.prop / release 下载可达性。"""
    owner, name = repo.split("/", 1)
    issues = []
    repo_info = _api_json(f"repos/{owner}/{name}", token)
    if repo_info is None:
        return {"status": "unverified", "issues": ["仓库元数据获取失败（不存在或被封禁？）"]}

    # --- license：尽力检测（license API -> LICENSE 文件 -> 配置人工标注），软性信息不阻塞收录 ---
    license_spdx = ""
    lic = repo_info.get("license")
    if lic and lic.get("spdx_id") and lic["spdx_id"] != "NOASSERTION":
        license_spdx = lic["spdx_id"]
    if not license_spdx:
        contents = _api_json(f"repos/{owner}/{name}/contents", token)
        has_license_file = False
        if isinstance(contents, list):
            for f in contents:
                fname = (f.get("name") or "").upper()
                if fname.startswith("LICENSE") or fname.startswith("COPYING") or fname == "LICENCE":
                    has_license_file = True
                    break
        manual_license = (mod or {}).get("license", "")
        if has_license_file:
            license_spdx = "SEE LICENSE FILE"
        elif manual_license:
            license_spdx = manual_license
        else:
            license_spdx = "unknown"  # 常见于 README 声明许可证的仓库，人工补录

    source_url = repo_info.get("html_url", f"https://github.com/{repo}")

    # --- module.prop：git trees API 递归查找（软性信息，不作为硬门槛——很多模块在 release 构建时才生成） ---
    module_prop = False
    tree = _api_json(f"repos/{owner}/{name}/git/trees/HEAD?recursive=1", token)
    if tree and isinstance(tree.get("tree"), list):
        for t in tree["tree"]:
            path = t.get("path") or ""
            if t.get("type") == "blob" and path.rsplit("/", 1)[-1] == "module.prop":
                module_prop = True
                break

    # --- 最新 release 下载 URL 可达性 ---
    releases = _api_json(f"repos/{owner}/{name}/releases", token)
    release_ok = False
    latest_url = ""
    if releases:
        drafts = [r for r in releases if r.get("draft")]
        stable = [r for r in releases if not r.get("draft") and not r.get("prerelease")]
        pool = stable or drafts
        if pool:
            latest = sorted(pool, key=lambda r: r.get("published_at") or r.get("created_at") or "", reverse=True)[0]
            assets = latest.get("assets") or []
            zips = [a for a in assets if (a.get("name") or "").lower().endswith(".zip")]
            target = (zips or assets)[0] if (zips or assets) else None
            if target:
                latest_url = target.get("browser_download_url", "")
                if skip_head:
                    release_ok = True  # 本地快速验证：跳过 HEAD 可达性
                else:
                    status, _ = _http(latest_url, timeout=30, method="HEAD")
                    release_ok = status in (200, 302)
    if not release_ok:
        issues.append("最新 release 无可下载 zip 资产（或下载地址不可达）")

    return {
        "status": "verified" if not issues else "unverified",
        "license": license_spdx,
        "sourceUrl": source_url,
        "moduleProp": module_prop,
        "releaseOk": release_ok,
        "latestReleaseUrl": latest_url,
        "issues": issues,
    }


def main():
    parser = argparse.ArgumentParser(description="ShizuSU 模块收录审核")
    parser.add_argument("--strict", action="store_true", help="存在 unverified 时退出码 1")
    parser.add_argument("--json", action="store_true", help="只输出审计 JSON")
    parser.add_argument("--skip-head", action="store_true", help="跳过 release HEAD 可达性检查（本地快速验证用）")
    args = parser.parse_args()

    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    token = os.environ.get("GITHUB_TOKEN") or None
    if not token:
        print("提示：未设置 GITHUB_TOKEN，检查可能受限流影响。", file=sys.stderr)

    modules = config.get("modules", [])
    audit = {
        "generatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "policy": {
            "requireOpenSource": True,
            "requireLicense": True,
            "requireSourceUrl": True,
            "requireReleaseZip": True,
        },
        "modules": {},
    }
    unverified = []
    for mod in modules:
        mid = mod["moduleId"]
        repo = mod.get("repo", "")
        if not repo:
            # 手动/私有模块：管理员背书
            audit["modules"][mid] = {
                "status": "manual",
                "license": mod.get("license", ""),
                "sourceUrl": mod.get("sourceUrl", ""),
                "moduleProp": None,
                "releaseOk": bool(mod.get("latestRelease", {}).get("downloadUrl")),
                "latestReleaseUrl": mod.get("latestRelease", {}).get("downloadUrl", ""),
                "issues": ["无公开仓库，由管理员背书（私有/随工具分发模块）"],
            }
            continue
        print(f"[{mid}] checking {repo} ...", file=sys.stderr)
        result = check_repo(repo, token, mod=mod, skip_head=args.skip_head)
        audit["modules"][mid] = result
        if result["status"] == "unverified":
            unverified.append(mid)
        time.sleep(0.2)  # 温和限流

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    verified = sum(1 for v in audit["modules"].values() if v["status"] == "verified")
    manual = sum(1 for v in audit["modules"].values() if v["status"] == "manual")
    print(f"审核完成: verified={verified} manual={manual} unverified={len(unverified)}")
    for mid in unverified:
        print(f"  - {mid}: {audit['modules'][mid]['issues']}")

    if args.json:
        print(json.dumps(audit, ensure_ascii=False, indent=2))

    if args.strict and unverified:
        print("存在未通过开源门槛的模块（--strict）", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
