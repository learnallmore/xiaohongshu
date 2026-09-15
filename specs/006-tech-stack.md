# 006 — 技术栈与工程约定

## 选定栈（Phase 2 起落地）

| 层 | 选型 |
|----|------|
| Web | Next.js（App Router）+ TypeScript |
| UI | React + CSS Modules 或 Tailwind（实现时二选一并写死） |
| DB | PostgreSQL |
| ORM | Prisma 或 Drizzle（实现时二选一并写死） |
| 任务 | 服务端 Cron（如 `node-cron` / 平台 Cron）或队列 Worker |
| AI | 通过服务端调用 LLM API（密钥仅环境变量） |
| 包管理 | pnpm |

## 目录预告（尚未创建应用代码）

```text
apps/web/           # Next.js 应用（Phase 2）
packages/…          # 若需 monorepo 再拆
specs/              # 本目录（已存在）
.cursor/            # Rules / Skills / Hooks
.github/workflows/  # CI
```

Phase 1 **不**创建 `apps/web`。

## 环境

- Node.js LTS（20+）
- Docker Compose 可选提供本地 Postgres（Phase 2）

## 质量门禁

- TypeScript strict
- CI：密钥扫描占位、Spec 存在性检查；应用出现后启用 lint / typecheck / test
- Agent 收工 Hook：变更摘要 + Spec 一致性清单

## 废弃

- 原 IntelliJ Java `Main.java` 空壳已移除，不再作为技术方向。
