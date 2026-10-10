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

## 收录与审核

见 [CONTRIBUTING.md](CONTRIBUTING.md)：开源+源码+许可证+可下载 release 为硬门槛；支持人工提交、topic 自动发现、手机端上传+审批三种收录路径。

## 内容清单（27 个模块）

| moduleId | 上游仓库 |
| --- | --- |
| zygisksu | LSPosed/ZygiskNext |
| playintegrityfix | osm0sis/PlayIntegrityFork |
| tricky_store | 5ec1cff/TrickyStore |
| bindhosts | bindhosts/bindhosts |
| device_faker | Seyud/device_faker |
| meta-hybrid | Hybrid-Mount/meta-hybrid_mount |
| netproxy | Fanju6/NetProxy-Magisk |
| MagicNet | LIghtJUNction/MagicNet |
| magic_mount_rs | Tools-cx-app/meta-magic_mount-rs |
| FreePPS | Seyud/FreePPS |
| Mediatek_Mali_GPU_Governor | Seyud/Mediatek_Mali_GPU_Governor |
| deviceidchanger | sidex15/deviceidchanger |
| HyperUnlocked | ukriu/HyperUnlocked |
| AZenith | Liliya2727/AZenith |
| zygisk_lsposed | JingMatrix/LSPosed |
| hma_oss_zygisk | frknkrc44/HMA-OSS |
| zygisk-assistant | snake-4/Zygisk-Assistant |
| ksuwebui | 5ec1cff/KsuWebUIStandalone |
| busybox-ndk | Magisk-Modules-Repo/busybox-ndk |
| RescueX | jiayuxuan123/RescueX |
| Automatic_brick_rescue / Eclipse / Violet / WorkSettingPro / YHGames / YH_YC / shizu-test | private/（管理员背书） |

> funbox / asl / meta-mm / meta-overlayfs / MFGA 暂缺（原仓库不可定位），补地址后重新生成即可。
