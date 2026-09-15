# AGENTS.md — Cursor Agent 总入口

本仓库采用 **Spec 驱动** 的 AI Native 开发流程。改代码前先读 Spec，改完强制自审 CR。

## 开工顺序

1. 阅读 [`specs/000-overview.md`](specs/000-overview.md) 了解产品定位。
2. 按任务阅读对应 Spec：
   - 内容流水线 → `001-content-pipeline.md`
   - 领域与审美 → `002-domains.md`
   - 预览 UI 信息架构 → `003-xhs-preview-ui.md`
   - **前端视觉与交互设计** → `007-frontend-design.md`
   - 数据与爆款 → `004-analytics-virality.md`
   - 真实发布 → `005-publisher-adapter.md`
   - 技术选型 → `006-tech-stack.md`
3. 遵循 `.cursor/rules/`（含强制自 CR、禁止自动推送）。
4. 需要时加载 `.cursor/skills/`：
   - `auto-code-review`：每次改码后强制自审
   - `authentic-xhs-voice`：真实可追溯素材 + 去 AI 味文案（生成/改帖必用）
   - `alibaba-java-coding-guidelines`：任何 Java 编写与审查
   - `content-curator` / `xhs-note-format` / `virality-review` / `publisher-checklist`

## 硬性约束

- **中文**与用户沟通。
- **每次改码后自 CR**：执行 `auto-code-review`，阻塞项先修。
- **禁止自动推送**：不得擅自 `git push`；仅用户明确授权。
- **禁止擅自装环境**：不得擅自 brew/Docker/`pip install`/`mvn` 装依赖/Flyway migrate；仅用户明确进入环境阶段。
- **禁止**擅自 `git commit` / 改 git config；仅用户明确要求时执行。
- **禁止** Cookie 抓包、逆向签名、非官方模拟登录发帖。
- **禁止** 提交 `.env`、密钥、token、Cookie。
- 功能变更必须先更新对应 `specs/*.md`，再改代码。

## 阶段路线图

| 阶段 | 内容 |
|------|------|
| Phase 1 | Git 隔离、Specs、Rules、Skills、Hooks、CI、凭证清单 |
| Phase 2（进行中） | FastAPI 单体 + MySQL 审阅预览（`apps/api`） |
| Phase 3 | 每日 3 候选生成 + 审阅工作流 |
| Phase 4 | 真实 Publisher + 指标回流 + 爆款评分闭环 |

## 合并前检查

- 已输出 `auto-code-review` 结论且无阻塞
- 若含 Java：已叠加阿里巴巴 Java 规范
- Spec 与实现一致；无密钥入库
- **未**自动 push；push 仅在用户授权后
