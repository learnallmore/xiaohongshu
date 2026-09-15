# AGENTS.md — Cursor Agent 总入口

本仓库采用 **Spec 驱动** 的 AI Native 开发流程。改代码前先读 Spec，改完做一致性检查。

## 开工顺序

1. 阅读 [`specs/000-overview.md`](specs/000-overview.md) 了解产品定位。
2. 按任务阅读对应 Spec：
   - 内容流水线 → `001-content-pipeline.md`
   - 领域与审美 → `002-domains.md`
   - 预览 UI → `003-xhs-preview-ui.md`
   - 数据与爆款 → `004-analytics-virality.md`
   - 真实发布 → `005-publisher-adapter.md`
   - 技术选型 → `006-tech-stack.md`
3. 遵循 `.cursor/rules/` 中的项目宪法与安全规则。
4. 需要领域能力时加载 `.cursor/skills/` 下对应 Skill。

## 硬性约束

- **中文**与用户沟通。
- **禁止** Cookie 抓包、逆向签名、非官方模拟登录发帖。
- **禁止** 擅自 `git commit` / `git push` / 改 git config；仅当用户明确要求时执行。
- **禁止** 提交 `.env`、密钥、token、Cookie。
- 功能变更必须先更新对应 `specs/*.md`，再改代码。
- 当前阶段（Phase 1）仅工作流基建；不要提前实现 Next.js 业务应用，除非用户明确进入 Phase 2+。

## 阶段路线图

| 阶段 | 内容 |
|------|------|
| Phase 1（当前） | Git 隔离、Specs、Rules、Skills、Hooks、CI、凭证清单 |
| Phase 2 | 应用骨架 + DB schema + 模拟小红书预览 |
| Phase 3 | 每日 3 候选生成 + 审阅工作流 |
| Phase 4 | 真实 Publisher + 指标回流 + 爆款评分闭环 |

## 合并前检查

- Spec 与实现一致
- 无密钥入库
- 本地/CI 检查通过
- 建议对 branch changes 跑 Bugbot / Security Review
