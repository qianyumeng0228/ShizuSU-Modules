# ShizuSU-Modules

ShizuSU 定制管理器的自建模块仓库源（A 路线），同时输出 MMRL 兼容格式（B 路线），替代已失效的官方源 `modules.kernelsu.org`。

## 结构与协议

```
modules.json                  # A 路线：模块目录（列表 schema，与官方一致）
module/<moduleId>.json        # A 路线：每个模块的详情（含 releases、README、下载链接）
json/config.json              # B 路线：MMRL 仓库描述
json/modules.json             # B 路线：MMRL 模块索引
modules/<id>/track.json       # B 路线：每个模块的 MMRL track 定义
modules/<id>/update.json      # B 路线：MagiskUpdateJson（版本/下载）
signatures/public.pem         # 签名公钥（进阶2）
signatures/modules.sig        # modules.json 的 Ed25519 签名
signatures/<moduleId>.sig     # 私有模块 zip 的签名
audit.json                    # 开源门槛审核结果（进阶3）
catalog/candidates.json       # topic 自动发现的候选清单（进阶1）
private/*.zip                 # 私有模块（管理员背书）
compat/                       # 适配模块
```

数据由 `build.py`（A 路线）+ `tools/build_mmrl.py`（B 路线）+ `tools/validate.py`（审核）+ `tools/sign.py`（签名）生成，每日 GitHub Actions 自动更新。A 路线 schema 与 SukiSU-Ultra / ShizuSU 管理器的解析代码逐字段对齐。

## 在 ShizuSU 管理器中切换

管理器已支持运行时覆盖仓库源：向「settings」偏好写入键 `module_repo_base_url`，值为本仓库的 Pages 地址：

```
https://qianyumeng0228.github.io/ShizuSU-Modules
```

不写则回退到默认源（`ModuleRepoConfig.DEFAULT_BASE_URL`）。

## MMRL 加载本仓库

在 MMRL 中添加仓库，URL 填：

```
https://qianyumeng0228.github.io/ShizuSU-Modules/
```

MMRL 读取 `json/config.json` 与 `json/modules.json`，可直接浏览/安装其中已收录的模块。

## 在 BakaSU 中添加本仓库

BakaSU 的「仓库设置 → + 添加仓库」支持自定义源，接入本仓库：

- **API 格式：必须选 `MMRL`**（本仓库输出 MMRL 兼容格式；不要选 `KernelSU Modules API`——那是 Registry 协议，本仓库不提供 `api/v1` 接口，且 BakaSU 对 Registry 源下载强制校验真实 SHA-256，会 404/安装失败）
- **服务器 URL**（不带 `/json/modules.json` 后缀）：

```
https://qianyumeng0228.github.io/ShizuSU-Modules
```

添加后即可浏览/安装其中已收录的模块，每日构建自动更新索引。

## 收录与审核

见 [CONTRIBUTING.md](CONTRIBUTING.md)：开源+源码+许可证+可下载 release 为硬门槛；支持人工提交、topic 自动发现、手机端上传+审批三种收录路径。

## 内容清单（共 546 个模块）

覆盖 KernelSU 模块全网生态 19 个分类：Root 隐藏 / Play Integrity、元模块（挂载引擎）、Zygisk 实现、性能调度、网络代理、广告拦截、音频、字体显示、备份救砖、Xposed/LSPosed 等。模块按「开源 + 许可证 + 可下载 release」硬门槛收录（来源：KernelSU 模块全网汇总 1,532 条清单筛选）。

- 根 `modules.json`（A 路线）：546 个模块目录与详情
- `json/modules.json`（B 路线 / MMRL / BakaSU）：499 个可安装模块索引
- `catalog/candidates.json`：topic 自动发现的候选清单

每日 GitHub Actions 自动更新版本、下载链接与统计。
