---
name: 模块收录 PR
about: 通过 PR 提交模块收录（模块信息变更）
title: "[modules] <模块名>"
labels: submission
---

## 变更内容

- 模块 ID：
- 模块名称：
- 源码仓库：
- 许可证：
- 变更类型：□ 新增收录 □ 更新信息 □ 下架

## 自查清单

- [ ] moduleId 英文小写、字母开头、2–64 字符
- [ ] 源码仓库公开可达
- [ ] 最新 release 有可下载 zip
- [ ] 有标准许可证或申请管理员背书
- [ ] 已运行 `python verify_schema.py` 通过

> 说明：合并后产物由每日构建自动生成，无需手动更新 `output/` 目录。
