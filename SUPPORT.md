# 支持（SUPPORT）

## 常见问题

### 怎么把我的管理器接入这个仓库？

- **ShizuSU / SukiSU-Ultra**：偏好写入 `module_repo_base_url=https://qianyumeng0228.github.io/ShizuSU-Modules`
- **MMRL**：添加仓库，URL 填 `https://qianyumeng0228.github.io/ShizuSU-Modules/`
- **BakaSU**：API 格式选 `MMRL`，服务器 URL 填裸 base（不带 `/json/modules.json`）
- 详见 [README.md](README.md) 快速开始

### 为什么某些模块显示「待审核 / unverified」？

该模块某项门槛未达标（通常是最新 release 无 zip 或仓库暂不可达），仍展示但标记待审核。每日构建会自动重试。

### 模块下载失败 / 404？

- 下载直链指向**上游** GitHub release，上游可能删除或移动了资产——等待下一轮构建自动更新，或开 Issue 反馈该模块
- 私有模块（`origin=manual`）zip 托管在本仓库 `private/`，如 404 请开 Issue

### 如何提交我的模块？

开 Issue 使用[模块提交模板](.github/ISSUE_TEMPLATE/module_submission.md)，或参考 [CONTRIBUTING.md](CONTRIBUTING.md) 的三种收录方式。

### 想用仓库数据做工具 / 网站？

参考 [API.md](API.md) 数据格式文档，欢迎引用（注明来源即可）。

## 反馈渠道

| 渠道 | 用途 |
|---|---|
| [GitHub Issues](https://github.com/qianyumeng0228/ShizuSU-Modules/issues) | 模块提交、问题反馈、收录申请 |
| [安全报告](SECURITY.md) | 安全漏洞 / 恶意模块 |
| 仓库 Discussions | 讨论与建议 |

## 服务状态

- 索引数据：`https://qianyumeng0228.github.io/ShizuSU-Modules/modules.json`
- 每日 UTC 00:30 自动更新（可查看 [Actions](https://github.com/qianyumeng0228/ShizuSU-Modules/actions) 运行状态）
