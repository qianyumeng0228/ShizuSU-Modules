# ShizuSU-Modules

[![更新状态](https://github.com/qianyumeng0228/ShizuSU-Modules/actions/workflows/update-modules.yml/badge.svg)](https://github.com/qianyumeng0228/ShizuSU-Modules/actions/workflows/update-modules.yml)
[![在线](https://img.shields.io/website?url=https%3A%2F%2Fqianyumeng0228.github.io%2FShizuSU-Modules&label=Pages)](https://qianyumeng0228.github.io/ShizuSU-Modules)
[![模块数](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fqianyumeng0228.github.io%2FShizuSU-Modules%2Fmodules.json&query=length&label=%E6%A8%A1%E5%9D%97%E6%80%BB%E6%95%B0&color=blue)](https://qianyumeng0228.github.io/ShizuSU-Modules/modules.json)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

**语言：** 中文 · [English](docs/i18n/README.en.md) · [Deutsch](docs/i18n/README.de.md) · [Русский](docs/i18n/README.ru.md) · [日本語](docs/i18n/README.ja.md) · [Français](docs/i18n/README.fr.md) · [Italiano](docs/i18n/README.it.md) · [Español](docs/i18n/README.es.md)

面向 **KernelSU / Magisk / APatch** 生态的开源模块仓库源：一套配置，同时输出 **ShizuSU / SukiSU-Ultra（A 路线）** 与 **MMRL / BakaSU（B 路线）** 两种兼容格式，替代已失效的官方源 `modules.kernelsu.org`。

收录 **1,532 条全网清单** 筛选出的开源模块，每日自动构建更新版本与下载链接。

## 特性

- **双格式输出**：`modules.json`（管理器原生 schema）+ `json/modules.json`（MMRL 协议），一个仓库通吃 ShizuSU、KernelSU、SukiSU-Ultra、MMRL、BakaSU
- **全自动维护**：GitHub Actions 每日 UTC 00:30 自动抓取仓库元数据、最新 release、下载直链并重新签名
- **开源门槛审计**：`tools/validate.py` 逐模块核验「源码可达 + 许可证 + release 可下载」，结果写入 `audit.json` 可追溯
- **签名机制**：索引与私有模块 zip 由 Ed25519 签名，公钥随仓库公开，可离线验签
- **人工 + 自动双收录**：支持 Issue 提交、GitHub topic 自动发现、手机端上传审批三种收录路径
- **管理员背书**：许可证不明的模块经管理员审核后收录（`adminApproved`），标注透明、风险自评

## 快速开始

### ShizuSU / SukiSU-Ultra 管理器

管理器支持运行时覆盖仓库源：向「settings」偏好写入键 `module_repo_base_url`，值为本仓库 Pages 地址：

```
https://qianyumeng0228.github.io/ShizuSU-Modules
```

### KernelSU 官方管理器（A 路线）

使用支持 `modules.json` 列表格式的管理器，添加仓库源：

```
https://qianyumeng0228.github.io/ShizuSU-Modules/modules.json
```

### MMRL

MMRL 中添加仓库，URL 填（带或不带末尾 `/` 均可）：

```
https://qianyumeng0228.github.io/ShizuSU-Modules/
```

MMRL 读取 `json/config.json` 与 `json/modules.json`，可直接浏览/安装。

### BakaSU

BakaSU「仓库设置 → + 添加仓库」：

- **API 格式：必须选 `MMRL`**
- **服务器 URL**（不带 `/json/modules.json` 后缀）：

```
https://qianyumeng0228.github.io/ShizuSU-Modules
```

> 不要选 `KernelSU Modules API`：那是 Registry 协议，本仓库不提供 `api/v1` 接口，且 BakaSU 对 Registry 源强制校验真实 SHA-256，会 404/安装失败。

## 仓库结构

```
modules.json                  # A 路线：模块目录（列表，与官方 schema 一致）
module/<moduleId>.json        # A 路线：每个模块详情（releases / README / 下载链接）
json/config.json              # B 路线：MMRL 仓库描述
json/modules.json             # B 路线：MMRL 模块索引
modules/<id>/track.json       # B 路线：MMRL track 定义
modules/<id>/update.json      # B 路线：MagiskUpdateJson（版本/下载）
signatures/public.pem         # Ed25519 签名公钥
signatures/modules.sig        # modules.json 签名
signatures/<moduleId>.sig     # 私有模块 zip 签名
audit.json                    # 开源门槛审核结果
catalog/candidates.json       # topic 自动发现候选清单
private/*.zip                 # 私有模块（管理员背书）
compat/                       # 适配模块
```

数据由 `build.py`（A 路线）+ `tools/build_mmrl.py`（B 路线）+ `tools/validate.py`（审核）+ `tools/sign.py`（签名）生成，A 路线 schema 与 SukiSU-Ultra / ShizuSU 管理器解析代码逐字段对齐。

## 收录内容

- **861 个模块**进入 A 路线索引，**794 个**可在 MMRL/BakaSU 直接安装
- 覆盖 **19 个分类**：Root 隐藏 / Play Integrity、元模块（挂载引擎）、Zygisk 实现、性能调度、网络代理、广告拦截、音频、字体显示、备份救砖、Xposed/LSPosed、WebUI 等
- **322 个为管理员背书收录**（`adminApproved`）：上游许可证未声明或不明确，由管理员审核后收录，条目带 `note` 说明，使用时自行评估风险
- 数据来源：KernelSU 模块全网汇总（1,532 条去重清单）

## 收录标准

模块满足以下条件才会进入索引（详见 [CONTRIBUTING.md](CONTRIBUTING.md)）：

1. **源码可达**：公开的 GitHub 仓库
2. **许可证**：可检测到标准开源许可证（SPDX）；许可证不明走管理员背书
3. **可下载**：最新 release 包含可下载 zip
4. **非内核构建**：内核源码/LKM 构建类不收（模块仓库只收可安装模块）

未达标模块会被标记 `unverified`（仍展示待审核状态）；无公开仓库的私有模块由管理员背书，标记 `origin=manual`。

## 提交模块

三种方式任选：

1. **Issue 提交（推荐）**：使用 [模块提交模板](.github/ISSUE_TEMPLATE/module_submission.md) 开 Issue，附源码仓库与 release 地址
2. **自动发现**：`discover-modules.yml` 每日按 topic（`shizusu-module` / `kernelsu-module` / `magisk-module` / `apatch-module`）扫描，候选进 `catalog/candidates.json`
3. **手机端上传**：ShizuSU 管理器「模块上传」入口 → 待审队列 → 管理员审批入库

## 更新机制

- **每日构建**：UTC 00:30（北京时间 08:30）自动更新版本、下载链接、统计
- **手动触发**：仓库 Actions 页可手动运行 `Update module repo` workflow
- 构建链路：A 路线生成 → 开源门槛审计 → MMRL 输出 → 签名 → schema 校验 → 同步 GitHub Pages

## 引用与接入（欢迎使用）

欢迎任何管理器、工具、网站引用本仓库数据。推荐方式：

- **直接读 JSON**：`https://qianyumeng0228.github.io/ShizuSU-Modules/modules.json`（列表）、`module/<id>.json`（详情）
- **动态徽章**：模块总数徽章已支持（见文首，shields.io 动态读取）
- **接入规范**：字段定义见 [API.md](API.md)；下载直链均为上游 GitHub release，可直接落盘
- **引用约定**：请在引用处注明「数据来源 ShizuSU-Modules」并附仓库链接；为减轻上游压力，建议对 JSON 做缓存（数据每日 08:30 左右更新）

## 许可证与免责声明

- 本仓库**代码与索引**采用 [MIT License](LICENSE)
- 收录的第三方模块**版权归原作者所有**：本仓库仅作索引/链接收录，「收录」不代表授权使用，使用前请查看各模块上游许可证；管理员背书模块（`adminApproved`）许可证不明确，使用者自行评估风险
- 若上游作者主张权利，可开 Issue，仓库将在 24h 内下架对应条目
