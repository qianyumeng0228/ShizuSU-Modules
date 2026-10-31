# ShizuSU-Modules 数据格式文档（API）

本文档描述本仓库对外输出的数据结构，供管理器、工具、网站等第三方接入。数据每日 UTC 00:30 更新（北京时间 08:30），建议对 JSON 做缓存并附带 `User-Agent`。

基础 URL：

```
https://qianyumeng0228.github.io/ShizuSU-Modules
```

---

## A 路线：ShizuSU / SukiSU-Ultra / KernelSU 管理器

### GET /modules.json

模块目录（数组）。每条结构：

```json
{
  "moduleId": "zygisksu",
  "moduleName": "Zygisk Next",
  "authors": [
    { "name": "Nullptr", "link": "" },
    { "name": "5ec1cff", "link": "" }
  ],
  "summary": "独立 Zygisk 实现，为 KernelSU 提供 Zygisk API，可替代 Magisk 内置 Zygisk",
  "metamodule": false,
  "zygisk": true,
  "stargazerCount": 997,
  "updatedAt": "2026-10-13T14:24:45Z",
  "createdAt": "2026-09-19T10:48:59Z",
  "latestRelease": {
    "name": "v1.5.2",
    "time": "2026-10-13T14:24:46Z",
    "versionCode": 0,
    "downloadUrl": "https://github.com/LSPosed/ZygiskNext/releases/download/v1.5.2/Zygisk-Next-1.5.2-864-a4a72ce-release.zip"
  },
  "origin": "github",
  "note": "官方仓库已迁至 LSPosed 组织（原 Dr-TSNG/ZygiskNext）"
}
```

字段说明：

| 字段 | 类型 | 说明 |
|---|---|---|
| `moduleId` | string | 唯一 ID（小写，字母开头，2–64 字符） |
| `moduleName` | string | 展示名 |
| `authors` | array | 作者列表（`name` + 可选 `link`） |
| `summary` | string | 一句话简介 |
| `metamodule` | bool | 是否为元模块（挂载引擎） |
| `zygisk` | bool | 是否 Zygisk 模块 |
| `stargazerCount` | int | 上游仓库 star 数 |
| `updatedAt` / `createdAt` | string | 上游仓库最后推送 / 创建时间（ISO 8601） |
| `latestRelease.name` | string | 最新 release 标签 |
| `latestRelease.time` | string | release 发布时间 |
| `latestRelease.versionCode` | int | 版本号（0 表示未知） |
| `latestRelease.downloadUrl` | string | **zip 直链**（上游 GitHub release） |
| `latestRelease.note` | string | 可选：回退说明（如最新版未打包 zip） |
| `origin` | string | `github`（公开仓库）/ `manual`（管理员背书，无公开仓库） |
| `note` | string | 可选：管理备注（含管理员背书说明） |

### GET /module/{moduleId}.json

单个模块详情。结构：

```json
{
  "readme": "# Zygisk Next\n...",
  "readmeHTML": "<h1>Zygisk Next</h1>...",
  "homepageUrl": "https://github.com/LSPosed/ZygiskNext",
  "sourceUrl": "https://github.com/LSPosed/ZygiskNext",
  "url": "https://github.com/LSPosed/ZygiskNext",
  "latestRelease": {
    "name": "v1.5.2",
    "version": "v1.5.2",
    "time": "2026-10-13T14:24:46Z",
    "downloadUrl": "https://github.com/LSPosed/ZygiskNext/releases/download/v1.5.2/Zygisk-Next-1.5.2-864-a4a72ce-release.zip"
  },
  "releases": [
    {
      "name": "v1.5.2",
      "tagName": "v1.5.2",
      "publishedAt": "2026-10-13T14:24:46Z",
      "descriptionHTML": "",
      "releaseAssets": [
        {
          "name": "Zygisk-Next-1.5.2-864-a4a72ce-release.zip",
          "downloadUrl": "https://github.com/LSPosed/ZygiskNext/releases/download/v1.5.2/Zygisk-Next-1.5.2-864-a4a72ce-release.zip",
          "size": 6714344,
          "downloadCount": 192209
        }
      ]
    }
  ],
  "note": "官方仓库已迁至 LSPosed 组织（原 Dr-TSNG/ZygiskNext）"
}
```

---

## B 路线：MMRL / BakaSU 兼容

### GET /json/config.json

仓库描述：

```json
{
  "id": "shizusu-modules",
  "name": "ShizuSU 模块仓库",
  "base_url": "https://qianyumeng0228.github.io/ShizuSU-Modules/",
  "website": "https://github.com/qianyumeng0228/ShizuSU-Modules",
  "support": "https://github.com/qianyumeng0228/ShizuSU-Modules/issues",
  "submission": "https://github.com/qianyumeng0228/ShizuSU-Modules/issues/new?template=module_submission.md",
  "description": "ShizuSU 自建模块收录中心：A 路线（ShizuSU 管理器原生源）+ B 路线（MMRL 兼容）双输出。",
  "max_num": 100,
  "enable_log": false,
  "log_dir": "log"
}
```

### GET /json/modules.json

模块索引。结构：

```json
{
  "id": "shizusu-modules",
  "name": "ShizuSU 模块仓库",
  "description": "...",
  "metadata": { "version": 1 },
  "modules": [
    {
      "id": "zygisksu",
      "name": "Zygisk Next",
      "version": "v1.5.2",
      "versionCode": 0,
      "author": "Nullptr",
      "description": "独立 Zygisk 实现...",
      "stars": 997,
      "timestamp": 1791901486.0,
      "latest": {
        "zipUrl": "https://github.com/LSPosed/ZygiskNext/releases/download/v1.5.2/Zygisk-Next-1.5.2-864-a4a72ce-release.zip",
        "changelog": ""
      },
      "versions": [
        { "timestamp": 1791901486.0, "version": "v1.5.2", "versionCode": 0, "zipUrl": "..." }
      ],
      "track": "zygisksu",
      "readme": "https://qianyumeng0228.github.io/ShizuSU-Modules/module/zygisksu.json",
      "icon": ""
    }
  ]
}
```

字段与 MMRL 仓库协议对齐：`latest.zipUrl` 为安装直链，`track` 指向 track 定义，`readme` 指向详情页。

### GET /modules/{id}/track.json

```json
{
  "id": "zygisksu",
  "enable": true,
  "verified": true,
  "update_to": "update.json",
  "source": "https://github.com/LSPosed/ZygiskNext",
  "license": "GPL-3.0",
  "category": "Zygisk",
  "arch": ["arm64-v8a"],
  "changelog": "",
  "note": "官方仓库已迁至 LSPosed 组织（原 Dr-TSNG/ZygiskNext）"
}
```

### GET /modules/{id}/update.json

MagiskUpdateJson 格式：

```json
{
  "version": "v1.5.2",
  "versionCode": 0,
  "zipUrl": "https://github.com/LSPosed/ZygiskNext/releases/download/v1.5.2/Zygisk-Next-1.5.2-864-a4a72ce-release.zip",
  "changelog": ""
}
```

---

## 签名与审计

| 文件 | 说明 |
|---|---|
| `signatures/public.pem` | Ed25519 公钥（验签用） |
| `signatures/modules.sig` | `modules.json` 签名 |
| `signatures/{moduleId}.sig` | 私有模块 zip 签名 |
| `audit.json` | 开源门槛审核结果（每模块 verified/unverified + 原因） |

验签：`python tools/sign.py --verify`

---

## 接入约定

1. **缓存**：数据每日 08:30 左右更新，建议缓存 ≥ 1 小时
2. **User-Agent**：请求时附带合理 UA（`ShizuSU-Modules/<工具名>`），便于统计
3. **下载**：`downloadUrl` / `zipUrl` 均为上游 GitHub release 直链，可直接下载安装
4. **引用**：注明「数据来源 ShizuSU-Modules」并附 [仓库链接](https://github.com/qianyumeng0228/ShizuSU-Modules)
