#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ShizuSU / SukiSU-Ultra 管理器「模块仓库」生成器

读取 modules.config.json 中的模块清单，调用 GitHub API 抓取每个模块的
仓库元数据（stars/时间/简介）与 release 资产信息，产出管理器可直接使用的：

  output/modules.json            —— 模块目录（列表）
  output/module/<moduleId>.json  —— 每个模块的详情

生成格式严格对齐 SukiSU-Ultra/ShizuSU 管理器解析代码：
  manager/app/src/main/java/com/sukisu/ultra/data/repository/ModuleRepoRepositoryImpl.kt
  manager/app/src/main/java/com/sukisu/ultra/ui/util/module/ModuleRepoApi.kt

用法：
  python build.py                       # 按配置生成全部输出
  python build.py --search <关键词>      # 搜索 GitHub 仓库，帮助确定 canonical repo
  python build.py --repo owner/name     # 核验单个仓库元数据

环境变量：
  GITHUB_TOKEN     GitHub 个人访问令牌（强烈建议，避免 60次/小时 限流）
  HTTPS_PROXY      HTTP 代理（如 http://127.0.0.1:7890）
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://api.github.com"
RAW_BASE = "https://raw.githubusercontent.com"
USER_AGENT = "shizusu-module-repo-builder/1.0"

HERE = Path(__file__).resolve().parent
CONFIG_PATH = HERE / "modules.config.json"
DEFAULT_OUTPUT = HERE / "output"
DEFAULT_CACHE = HERE / "cache"


# ---------------------------------------------------------------------------
# HTTP 基础
# ---------------------------------------------------------------------------

def _proxy_opener():
    proxies = {}
    for key in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy"):
        val = os.environ.get(key)
        if val:
            proxies["https" if key.upper().startswith("HTTPS") else "http"] = val
    handlers = [urllib.request.ProxyHandler(proxies)] if proxies else []
    return urllib.request.build_opener(*handlers)


class ApiError(Exception):
    def __init__(self, status, message, retry_after=None):
        super().__init__(f"HTTP {status}: {message}")
        self.status = status
        self.retry_after = retry_after


def _get(url, token=None, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    opener = _proxy_opener()
    for _ in range(5):  # 403/429 退避重试
        try:
            with opener.open(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                return json.loads(body) if body.strip() else None
        except urllib.error.HTTPError as e:
            if e.code in (403, 429):
                retry_after = e.headers.get("Retry-After")
                wait = int(retry_after) if retry_after and retry_after.isdigit() else 10
                print(f"  [rate-limit] {url} -> {e.code}, waiting {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            detail = ""
            try:
                detail = e.read().decode("utf-8", errors="replace")[:200]
            except Exception:
                pass
            raise ApiError(e.code, detail) from None
        except urllib.error.URLError as e:
            # 网络瞬时错误：短暂重试
            print(f"  [network] {url} -> {e.reason}, retrying", file=sys.stderr)
            time.sleep(3)
    raise ApiError(0, "exhausted retries")


def api_get(path, params=None, token=None):
    url = f"{BASE}/{path.lstrip('/')}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    return _get(url, token=token)


def raw_get(owner, repo, filepath, token=None, timeout=15):
    url = f"{RAW_BASE}/{owner}/{repo}/HEAD/{filepath}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    opener = _proxy_opener()
    try:
        with opener.open(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError):
        return None


def cache_get(key, ttl, fetcher, token=None):
    """带 TTL 的简单 JSON 缓存"""
    cache_dir = DEFAULT_CACHE
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / (key.replace("/", "__").replace("?", "_") + ".json")
    now = time.time()
    if cache_file.exists():
        try:
            rec = json.loads(cache_file.read_text(encoding="utf-8"))
            if now - rec["at"] < ttl:
                return rec["data"]
        except Exception:
            pass
    data = fetcher()
    cache_file.write_text(
        json.dumps({"at": now, "data": data}, ensure_ascii=False), encoding="utf-8"
    )
    return data


# ---------------------------------------------------------------------------
# GitHub 数据抓取
# ---------------------------------------------------------------------------

def fetch_repo(spec, token):
    owner, name = spec.split("/", 1)
    key = f"repo_{owner}_{name}"
    return cache_get(
        key,
        3600,
        lambda: api_get(f"repos/{owner}/{name}", token=token),
        token=token,
    )


def fetch_releases(spec, token):
    owner, name = spec.split("/", 1)
    key = f"releases_{owner}_{name}"
    return cache_get(
        key,
        21600,
        lambda: api_get(f"repos/{owner}/{name}/releases", params={"per_page": 30}, token=token),
        token=token,
    )


def fetch_readme(spec, token):
    owner, name = spec.split("/", 1)
    for candidate in ("README.md", "readme.md", "README"):
        text = raw_get(owner, name, candidate, token=token)
        if text is not None:
            return text
    return None


def pick_latest_release(releases):
    """选最新正式 release；没有正式版则取最新 pre-release；过滤 draft"""
    drafts = [r for r in releases if r.get("draft")]
    stable = [r for r in releases if not r.get("draft") and not r.get("prerelease")]
    pre = [r for r in releases if not r.get("draft") and r.get("prerelease")]
    pool = stable or pre or drafts
    if not pool:
        return None
    return sorted(pool, key=lambda r: r.get("published_at") or r.get("created_at") or "", reverse=True)[0]


def pick_asset(release):
    """优先 zip；其次任意第一个可下载资产"""
    assets = release.get("assets") or []
    if not assets:
        return None
    for a in assets:
        if (a.get("name") or "").lower().endswith(".zip"):
            return a
    return assets[0]


# ---------------------------------------------------------------------------
# 输出 schema（对齐管理器解析代码）
# ---------------------------------------------------------------------------

def build_catalog_entry(mod, token):
    spec = mod["repo"]
    repo = fetch_repo(spec, token)
    releases = fetch_releases(spec, token)
    latest = pick_latest_release(releases)
    asset = pick_asset(latest) if latest else None

    authors = mod.get("authors")
    if not authors:
        authors = [{"name": repo.get("owner", {}).get("login", spec.split("/")[0]),
                    "link": repo.get("owner", {}).get("html_url", "")}]

    entry = {
        "moduleId": mod["moduleId"],
        "moduleName": mod.get("moduleName") or repo.get("name") or mod["moduleId"],
        "authors": authors,
        "summary": mod.get("summary") or repo.get("description") or "",
        "metamodule": bool(mod.get("metamodule", False)),
        "zygisk": bool(mod.get("zygisk", False)),
        "stargazerCount": repo.get("stargazers_count", 0),
        "updatedAt": repo.get("pushed_at") or repo.get("updated_at") or "",
        "createdAt": repo.get("created_at") or "",
        "latestRelease": {
            "name": (latest or {}).get("tag_name") or "",
            "time": (latest or {}).get("published_at") or (latest or {}).get("created_at") or "",
            "versionCode": mod.get("versionCodeOverride", 0),
            "downloadUrl": (asset or {}).get("browser_download_url") or "",
        },
    }
    return entry


def _naive_md_to_html(md):
    """极简 markdown → HTML。只覆盖常见结构；复杂文档建议用真实渲染器。"""
    if not md:
        return ""
    out = []
    in_code = False
    code_buf = []
    for raw_line in md.splitlines():
        line = raw_line.rstrip()
        if line.startswith("```"):
            if in_code:
                out.append("<pre>" + "\n".join(code_buf) + "</pre>")
                code_buf = []
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code_buf.append(line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
            continue
        if not line.strip():
            out.append("")
            continue
        if line.startswith("### "):
            out.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith("## "):
            out.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("# "):
            out.append(f"<h1>{line[2:]}</h1>")
        elif re.match(r"^[-*] ", line):
            out.append(f"<li>{line[2:]}</li>")
        elif re.match(r"^\d+\. ", line):
            item = re.sub(r"^\d+\. ", "", line)
            out.append(f"<li>{item}</li>")
        else:
            text = re.sub(r"`([^`]+)`", r"<code>\1</code>", line)
            text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
            text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
            out.append(f"<p>{text}</p>")
    if in_code:
        out.append("<pre>" + "\n".join(code_buf) + "</pre>")
    return "\n".join(out)


def build_detail(mod, token):
    spec = mod["repo"]
    repo = fetch_repo(spec, token)
    releases = fetch_releases(spec, token)
    readme = fetch_readme(spec, token)

    latest = pick_latest_release(releases)
    asset = pick_asset(latest) if latest else None

    releases_out = []
    for r in releases:
        assets_out = []
        for a in (r.get("assets") or []):
            assets_out.append({
                "name": a.get("name") or "",
                "downloadUrl": a.get("browser_download_url") or "",
                "size": a.get("size") or 0,
                "downloadCount": a.get("download_count") or 0,
            })
        releases_out.append({
            "name": r.get("tag_name") or "",
            "tagName": r.get("tag_name") or "",
            "publishedAt": r.get("published_at") or r.get("created_at") or "",
            "descriptionHTML": "",
            "releaseAssets": assets_out,
        })

    html_url = repo.get("html_url") or f"https://github.com/{spec}"
    return {
        "readme": readme or "",
        "readmeHTML": _naive_md_to_html(readme) if readme else "",
        "homepageUrl": mod.get("homepageUrl") or repo.get("homepage") or html_url,
        "sourceUrl": mod.get("sourceUrl") or html_url,
        "url": html_url,
        "latestRelease": {
            "name": (latest or {}).get("tag_name") or "",
            "version": (latest or {}).get("tag_name") or "",
            "time": (latest or {}).get("published_at") or (latest or {}).get("created_at") or "",
            "downloadUrl": (asset or {}).get("browser_download_url") or "",
        },
        "releases": releases_out,
    }


# ---------------------------------------------------------------------------
# 搜索 / 核验辅助
# ---------------------------------------------------------------------------

def cmd_search(keyword, token):
    q = keyword if ":" in keyword else f"{keyword} in:name"
    params = {"q": q, "sort": "stars", "order": "desc", "per_page": 6}
    try:
        data = api_get("search/repositories", params=params, token=token)
    except ApiError as e:
        print(f"搜索失败 {keyword}: {e}", file=sys.stderr)
        return
    print(f"搜索结果：{keyword}")
    for item in data.get("items", []):
        print(f"  {item['full_name']:<45} stars={item['stargazers_count']:<6} {item.get('description') or ''}")
    if not data.get("items"):
        print("  （无结果）")


def cmd_repo(spec, token):
    try:
        repo = fetch_repo(spec, token)
        releases = fetch_releases(spec, token)
        print(f"repo   : {repo['full_name']}")
        print(f"stars  : {repo.get('stargazers_count', 0)}")
        print(f"created: {repo.get('created_at')}")
        print(f"pushed : {repo.get('pushed_at')}")
        print(f"desc   : {repo.get('description') or ''}")
        print(f"releases: {len(releases)}")
        latest = pick_latest_release(releases)
        asset = pick_asset(latest) if latest else None
        print(f"latest : {latest.get('tag_name') if latest else None}")
        print(f"zip    : {(asset or {}).get('browser_download_url') or '(none)'}")
    except ApiError as e:
        print(f"FAIL {spec}: {e}")


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="ShizuSU 模块仓库生成器")
    parser.add_argument("--search", metavar="KEYWORD", help="搜索 GitHub 仓库")
    parser.add_argument("--repo", metavar="owner/name", help="核验单个仓库")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN") or None
    if not token:
        print("提示：未设置 GITHUB_TOKEN，将受 60 次/小时 限流。", file=sys.stderr)

    if args.search:
        cmd_search(args.search, token)
        return
    if args.repo:
        cmd_repo(args.repo, token)
        return

    if not CONFIG_PATH.exists():
        print(f"缺少配置文件：{CONFIG_PATH}", file=sys.stderr)
        sys.exit(1)

    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    modules = config["modules"]
    output_dir = Path(config.get("outputDir", DEFAULT_OUTPUT))
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "module").mkdir(parents=True, exist_ok=True)

    print(f"开始生成 {len(modules)} 个模块...")
    catalog = []
    errors = []
    skipped_ids = set()
    for i, mod in enumerate(modules, 1):
        module_id = mod["moduleId"]
        spec = mod.get("repo", "")
        print(f"[{i}/{len(modules)}] {module_id} <- {spec or '(未配置 repo)'}")
        if not spec:
            errors.append(f"{module_id}: 未配置 repo")
            skipped_ids.add(module_id)
            continue
        try:
            entry = build_catalog_entry(mod, token)
            detail = build_detail(mod, token)
            catalog.append(entry)
            (output_dir / "module" / f"{module_id}.json").write_text(
                json.dumps(detail, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        except Exception as e:  # noqa: BLE001 单模块失败不中断整体
            errors.append(f"{module_id}: {type(e).__name__}: {e}")

    catalog_path = output_dir / "modules.json"
    catalog_path.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\n完成：{len(catalog)}/{len(modules)} 成功")
    print(f"目录    : {catalog_path}")
    print(f"详情目录: {output_dir / 'module'}")
    if errors:
        print("\n失败项：")
        for e in errors:
            print("  - " + e)
        # 预期跳过（未配置 repo）不算失败：CI 中这些模块本来就缺，不应导致任务失败
        real_errors = [e for e in errors if not any(e.startswith(f"{mid}: 未配置 repo") for mid in skipped_ids)]
        if real_errors:
            sys.exit(2)


if __name__ == "__main__":
    main()
