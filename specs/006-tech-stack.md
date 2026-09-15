# 006 — 技术栈与工程约定

## 选定栈（当前）

| 层 | 选型 |
|----|------|
| 应用 | **FastAPI 单体**（Python）：页面 + API + 业务 |
| UI | Jinja2 模板 + 静态 CSS（见 `007-frontend-design.md`） |
| DB | **MySQL**（本机 TablePlus：`127.0.0.1:3306` / `root` / 空密码） |
| ORM | SQLAlchemy + PyMySQL |
| 包管理 | `apps/api` 内 venv + pip |
| 运行 | `uvicorn` → `http://127.0.0.1:8000` |

## 职责

```text
浏览器 ──► FastAPI（:8000）──► MySQL（库 xiaohongshumoney）
```

## 目录

```text
apps/api/          # 唯一运行入口（当前）
apps/web/          # 废弃：原 Next.js 实验，不再维护
specs/
.cursor/
```

## 环境

- 本地 `.env`：`DATABASE_URL=mysql+pymysql://root@127.0.0.1:3306/xiaohongshumoney`（勿提交）
- 建库：`CREATE DATABASE IF NOT EXISTS xiaohongshumoney`
- 本阶段用 SQLAlchemy `create_all`，暂不引入 Alembic

## 废弃

- Next.js / Prisma 运行路径
- Docker Compose / PostgreSQL
- Spring Boot（若文档曾提及，以本文为准：不做）

## 质量门禁

- 每次改码强制 `auto-code-review`
- 禁止自动 push；密钥不上库

## 质量门禁

- 每次改码强制 `auto-code-review`
- 禁止自动 push；密钥不上库

## 日更作业

- 飞书提醒：`.github/workflows/daily-feishu-remind.yml`（Secret：`FEISHU_WEBHOOK_URL`）
- Agent 落库：`python -m app.jobs.ingest_candidates`（读 `data/agent_daily.json`）
- **已废弃**：外部 LLM `daily_generate` 日更主路径
