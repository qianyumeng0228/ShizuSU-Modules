#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
输出 schema 校验：按 SukiSU-Ultra/ShizuSU 管理器解析代码的逻辑逐字段复验，
确保生成的 modules.json / module/<id>.json 能被管理器原样消费。

对照代码：
  manager/.../data/repository/ModuleRepoRepositoryImpl.kt  (parseRepoModule)
  manager/.../ui/util/module/ModuleRepoApi.kt             (fetchModuleDetail)
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_CFG = json.loads((HERE / "modules.config.json").read_text(encoding="utf-8"))
OUT = HERE / _CFG.get("outputDir", "output")


def opt_str(obj, key, default=""):
    v = obj.get(key)
    return default if v is None else str(v)


def opt_bool(obj, key, default=False):
    v = obj.get(key)
    if v is None:
        return default
    if isinstance(v, bool):
        return v
    return v not in (0, "", "false", "False")


def opt_int(obj, key, default=0):
    v = obj.get(key)
    if v is None:
        return default
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def check_catalog(entry):
    """复刻 parseRepoModule 的字段读取路径。
    返回 (errors, warnings)：errors=结构性问题（硬失败），warnings=数据质量问题（如无下载 asset）。
    """
    errors, warnings = [], []
    module_id = opt_str(entry, "moduleId")
    if not module_id:
        errors.append("moduleId 为空（管理器会跳过该条目）")
    name = opt_str(entry, "moduleName")
    if not name:
        errors.append("moduleName 为空")
    authors_raw = entry.get("authors")
    if authors_raw is None:
        errors.append("authors 缺失（管理器回退为字符串，建议补齐数组）")
    elif isinstance(authors_raw, list):
        for a in authors_raw:
            if not opt_str(a, "name"):
                errors.append("authors[] 中存在无 name 的项")
    lr = entry.get("latestRelease")
    if not isinstance(lr, dict):
        errors.append("latestRelease 缺失或非对象")
    else:
        if not opt_str(lr, "name") and not opt_str(lr, "version"):
            warnings.append("latestRelease 无 name/version（管理器显示空版本）")
        vc = opt_int(lr, "versionCode")
        if not isinstance(vc, int):
            errors.append("latestRelease.versionCode 非整数")
        url = opt_str(lr, "downloadUrl")
        if not url:
            warnings.append("latestRelease.downloadUrl 为空（管理器会生成空 asset，模块暂不可下载）")
    return errors, warnings


def check_detail(detail):
    """复刻 fetchModuleDetail 的字段读取路径。
    返回 (errors, warnings)。
    """
    errors, warnings = [], []
    if not isinstance(detail, dict):
        return ["详情 JSON 非对象"], []
    for key in ("readme", "readmeHTML", "homepageUrl", "sourceUrl", "url"):
        if key not in detail:
            errors.append(f"缺少字段 {key}")
    lr = detail.get("latestRelease")
    if not isinstance(lr, dict):
        errors.append("latestRelease 缺失或非对象")
    else:
        tag = opt_str(lr, "name") or opt_str(lr, "version")
        if not tag:
            warnings.append("latestRelease 无 name/version")
        if not opt_str(lr, "downloadUrl"):
            warnings.append("latestRelease.downloadUrl 为空（模块暂不可下载）")
    releases = detail.get("releases")
    if not isinstance(releases, list):
        errors.append("releases 缺失或非数组")
    else:
        for r in releases:
            rname = opt_str(r, "name") or opt_str(r, "tagName") or opt_str(r, "version")
            if not rname:
                errors.append("releases[] 中存在无 name/tagName/version 的项")
            assets = r.get("releaseAssets")
            if assets is not None and isinstance(assets, list):
                for a in assets:
                    if not opt_str(a, "name") or not opt_str(a, "downloadUrl"):
                        errors.append("releaseAssets[] 中存在 name/downloadUrl 为空的项")
    return errors, warnings


def main():
    catalog = json.loads((OUT / "modules.json").read_text(encoding="utf-8"))
    print(f"目录条目数: {len(catalog)}")
    total_err, total_warn = 0, 0
    for entry in catalog:
        errs, warns = check_catalog(entry)
        mid = entry.get("moduleId", "?")
        if errs:
            total_err += len(errs)
            print(f"  [目录] {mid}: " + "; ".join(errs))
        if warns:
            total_warn += len(warns)
            print(f"  [目录][warn] {mid}: " + "; ".join(warns))
    print(f"目录校验: 错误 {total_err} 处，警告 {total_warn} 处")

    detail_dir = OUT / "module"
    det_files = sorted(detail_dir.glob("*.json"))
    print(f"详情文件数: {len(det_files)}")
    det_err, det_warn = 0, 0
    for f in det_files:
        detail = json.loads(f.read_text(encoding="utf-8"))
        errs, warns = check_detail(detail)
        if errs:
            det_err += len(errs)
            print(f"  [详情] {f.stem}: " + "; ".join(errs))
        if warns:
            det_warn += len(warns)
            print(f"  [详情][warn] {f.stem}: " + "; ".join(warns))
    print(f"详情校验: 错误 {det_err} 处，警告 {det_warn} 处")

    # 交叉核对：详情文件集合与目录 moduleId 集合一致
    cat_ids = {e.get("moduleId") for e in catalog}
    det_ids = {f.stem for f in det_files}
    diff = cat_ids ^ det_ids
    if diff:
        print(f"[交叉] 目录与详情集合不一致: {sorted(diff)}")
        det_err += 1
    else:
        print("[交叉] 目录 moduleId 与详情文件一一对应: 通过")

    ok = total_err == 0 and det_err == 0
    print("结果:", "OK" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
