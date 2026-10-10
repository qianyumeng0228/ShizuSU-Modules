#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ShizuSU 模块仓库 MMRL 兼容输出生成器（B 路线）

读取 A 路线产物（output/modules.json + output/module/*.json）和审核结果
（output/audit.json），生成 MMRL 标准仓库布局：

  output/json/config.json          —— MMRL 仓库描述
  output/json/modules.json         —— MMRL 模块索引（modules[] + metadata）
  output/modules/<id>/track.json   —— 每个模块的 track 定义
  output/modules/<id>/update.json  —— MagiskUpdateJson（update_to 指向它）

布局对齐 mmrl-util（MMRLApp/MMRL-Util）的输出约定，保证 MMRL 应用可直接加载。

用法：python tools/build_mmrl.py [--base-url URL] [--id ID] [--name NAME]
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
OUT_DIR = HERE / "output"
CONFIG_PATH = HERE / "modules.config.json"

DEFAULT_BASE_URL = "https://qianyumeng0228.github.io/ShizuSU-Modules/"
DEFAULT_NAME = "ShizuSU 模块仓库"
DEFAULT_ID = "shizusu-modules"
DEFAULT_SUPPORT = "https://github.com/qianyumeng0228/ShizuSU-Modules/issues"
DEFAULT_SUBMISSION = "https://github.com/qianyumeng0228/ShizuSU-Modules/issues/new?template=module_submission.md"


def load_audit():
    audit_file = OUT_DIR / "audit.json"
    if not audit_file.exists():
        return {}
    return json.loads(audit_file.read_text(encoding="utf-8")).get("modules", {})


def load_detail(mid):
    f = OUT_DIR / "module" / f"{mid}.json"
    if not f.exists():
        return {}
    return json.loads(f.read_text(encoding="utf-8"))


def guess_category(mod):
    if mod.get("metamodule"):
        return "MetaModule"
    if mod.get("zygisk"):
        return "Zygisk"
    summary = (mod.get("summaryZh") or mod.get("summary") or "").lower()
    if any(k in summary for k in ("广告", "hosts", "adblock", "广告屏蔽")):
        return "AdBlock"
    if any(k in summary for k in ("性能", "调度", "调速", "performance", "tweak", "温控")):
        return "Performance"
    if any(k in summary for k in ("隐藏", "hide", "integrity", "认证", "检测")):
        return "Privacy"
    return "Utility"


def build_track(mid, mod, audit_entry):
    detail = load_detail(mid)
    source = ""
    repo = mod.get("repo", "")
    if repo:
        source = f"https://github.com/{repo}"
    else:
        source = mod.get("sourceUrl", "")

    license_spdx = ""
    if audit_entry:
        license_spdx = audit_entry.get("license", "")
    if not license_spdx:
        license_spdx = mod.get("license", "")

    verified = bool(audit_entry and audit_entry.get("status") == "verified")
    update_to = "update.json"  # LOCAL_JSON：指向本目录 update.json

    track = {
        "id": mid,
        "enable": True,
        "verified": verified,
        "update_to": update_to,
        "source": source,
        "license": license_spdx,
        "category": guess_category(mod),
        "arch": ["arm64-v8a"],
        "changelog": "",
    }
    return track


def build_update_json(mid, catalog_by_id):
    """从 A 路线 catalog 条目取真实 latestRelease（含 API 拉取的 downloadUrl）。"""
    entry = catalog_by_id.get(mid) or {}
    latest = entry.get("latestRelease") or {}
    return {
        "version": latest.get("name") or "",
        "versionCode": int(latest.get("versionCode") or 0),
        "zipUrl": latest.get("downloadUrl") or "",
        "changelog": "",
    }


def build_modules_json(catalog, tracks):
    now = datetime.now(timezone.utc).timestamp()
    modules_out = []
    for entry in catalog:
        mid = entry["moduleId"]
        track = tracks.get(mid)
        if not track:
            continue
        latest = entry.get("latestRelease") or {}
        version = latest.get("name") or ""
        version_code = int(latest.get("versionCode") or 0)
        zip_url = latest.get("downloadUrl") or ""
        try:
            ts = datetime.strptime(latest.get("time") or "", "%Y-%m-%dT%H:%M:%SZ").timestamp()
        except (ValueError, TypeError):
            ts = now
        modules_out.append({
            "id": mid,
            "version": version,
            "versionCode": version_code,
            "latest": {"zipUrl": zip_url, "changelog": ""},
            "versions": [{
                "timestamp": ts,
                "version": version,
                "versionCode": version_code,
                "zipUrl": zip_url,
                "changelog": "",
                "size": 0,
            }],
            "track": track,
            "timestamp": ts,
        })
    return {"modules": modules_out, "metadata": {"timestamp": now}}


def main():
    parser = argparse.ArgumentParser(description="ShizuSU 模块仓库 MMRL 兼容输出")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--id", default=DEFAULT_ID)
    parser.add_argument("--name", default=DEFAULT_NAME)
    parser.add_argument("--support", default=DEFAULT_SUPPORT)
    parser.add_argument("--submission", default=DEFAULT_SUBMISSION)
    args = parser.parse_args()

    if not args.base_url.endswith("/"):
        args.base_url += "/"

    config_src = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    catalog = json.loads((OUT_DIR / "modules.json").read_text(encoding="utf-8"))
    audit = load_audit()
    by_id = {m["moduleId"]: m for m in config_src.get("modules", [])}

    # config.json
    repo_config = {
        "id": args.id,
        "name": args.name,
        "base_url": args.base_url,
        "website": "https://github.com/qianyumeng0228/ShizuSU-Modules",
        "support": args.support,
        "submission": args.submission,
        "description": "ShizuSU 自建模块收录中心：A 路线（ShizuSU 管理器原生源）+ B 路线（MMRL 兼容）双输出。",
        "max_num": 100,
        "enable_log": False,
        "log_dir": "log",
    }
    json_dir = OUT_DIR / "json"
    json_dir.mkdir(parents=True, exist_ok=True)
    (json_dir / "config.json").write_text(
        json.dumps(repo_config, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # tracks + update.json
    tracks = {}
    modules_dir = OUT_DIR / "modules"
    catalog_by_id = {e["moduleId"]: e for e in catalog}
    for mid, mod in by_id.items():
        audit_entry = audit.get(mid)
        track = build_track(mid, mod, audit_entry)
        tracks[mid] = track
        tdir = modules_dir / mid
        tdir.mkdir(parents=True, exist_ok=True)
        (tdir / "track.json").write_text(
            json.dumps(track, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (tdir / "update.json").write_text(
            json.dumps(build_update_json(mid, catalog_by_id), ensure_ascii=False, indent=2), encoding="utf-8"
        )

    # modules.json（MMRL 索引）
    mmrl_index = build_modules_json(catalog, tracks)
    (json_dir / "modules.json").write_text(
        json.dumps(mmrl_index, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"MMRL 输出完成: json/config.json, json/modules.json, modules/<id>/{{track,update}}.json ({len(tracks)} tracks)")
    print(f"base_url = {args.base_url}")


if __name__ == "__main__":
    main()
