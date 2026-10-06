# ShizuSU-Modules

ShizuSU 定制管理器的自建模块仓库源，替代已失效的官方源 `modules.kernelsu.org`（上游托管组织被 GitHub 临时封禁，全站 404）。

## 结构与协议

```
modules.json           # 模块目录（列表 schema，与官方一致）
module/<moduleId>.json # 每个模块的详情（含 releases、README、下载链接）
```

数据由 [module-repo-builder](https://github.com/qianyumeng0228/ShizuSU) 的生成脚本从各模块的 GitHub release 元数据生成，schema 与 SukiSU-Ultra / ShizuSU 管理器的解析代码逐字段对齐。

## 在 ShizuSU 管理器中切换

管理器已支持运行时覆盖仓库源：向「settings」偏好写入键 `module_repo_base_url`，值为本仓库的 Pages 地址：

```
https://qianyumeng0228.github.io/ShizuSU-Modules
```

不写则回退到默认源（`ModuleRepoConfig.DEFAULT_BASE_URL`）。

## 内容清单（14 个模块）

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

> funbox / asl / meta-mm / meta-overlayfs / MFGA 暂缺（原仓库不可定位），补地址后重新生成即可。
