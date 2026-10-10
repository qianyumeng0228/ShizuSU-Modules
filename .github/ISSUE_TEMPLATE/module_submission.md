---
name: 模块提交
about: 提交一个 KernelSU / Magisk / APatch 模块收录申请（人工收录路径）
title: "[模块提交] <模块名>"
labels: submission
assignees: ''
---

## 模块信息

- **模块 ID**：（建议英文小写，如 `my_module`）
- **模块名称**：
- **源码仓库**：（必须为公开开源仓库，如 `owner/repo`）
- **最新 release 下载地址**：（zip 直链）
- **许可证**：（如 GPL-3.0 / MIT / Apache-2.0）
- **模块类型**：□ KernelSU □ Magisk □ APatch □ Zygisk □ 元模块（MetaModule）
- **简介**：（一句话说明功能）

## 收录门槛自查

- [ ] 源码仓库公开可访问
- [ ] 有开源许可证（LICENSE 文件或 README 声明）
- [ ] 最新 release 提供可下载的 zip 资产
- [ ] 无恶意/投毒行为，代码可审计

> 管理员审核通过后将加入 `modules.config.json`，每日构建自动生成 A 路线（ShizuSU 管理器）+ B 路线（MMRL）双格式产物。
