---
name: publisher-checklist
description: >-
  真实发布前合规与字段校验清单。在调用 Publisher 或实现发布按钮逻辑时使用。
---

# 发布前清单

## 何时使用

- 用户点击「立即发布」前后
- 实现或修改 `PublisherAdapter`
- 接入官方/第三方凭证时

## 必读

- `specs/005-publisher-adapter.md`
- `.cursor/rules/security-secrets.mdc`

## 校验清单

- [ ] `PUBLISHER_DRIVER` 已设且非误用生产凭证做实验（优先 `noop` / 测试号）
- [ ] 标题、正文、标签非空且符合平台限制
- [ ] 每张图有 `source` + `license`；无未授权转载
- [ ] Token 有效或已 `refreshAuthIfNeeded`
- [ ] 失败时返回可读 `errorCode`（如 `PUBLISH_SCOPE_MISSING`）
- [ ] 成功后写入 `externalNoteId` 并入指标队列

## 缺口

若官方未开放发笔记权限：停止并说明缺口，**不要**改为抓包方案。
