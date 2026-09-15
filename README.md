# 小红书起号系统（棱镜）

AI Native 运营台：每日 3 条小众审美候选 → 模拟小红书预览审阅 → 合规发布 → 数据回流。

> **当前阶段：Phase 2 — FastAPI 单体审阅页**  
> 运行目录：[`apps/api`](apps/api)。原 [`apps/web`](apps/web)（Next.js）已废弃，勿再作为运行路径。

## 本地访问

服务启动后打开：**http://127.0.0.1:8000/review**

```bash
cd apps/api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# 确保 MySQL 可连：127.0.0.1:3306 root 空密码，库 xiaohongshumoney
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## 文档

| 文档 | 用途 |
|------|------|
| [AGENTS.md](AGENTS.md) | Agent 入口 |
| [specs/006-tech-stack.md](specs/006-tech-stack.md) | FastAPI + MySQL |
| [specs/007-frontend-design.md](specs/007-frontend-design.md) | 棱镜 UI |
| [auto-code-review](.cursor/skills/auto-code-review/SKILL.md) | 强制自审 CR |

## 规范要点

- 先 Spec 后代码；每次改码自 CR；**禁止自动 push**
- MySQL 连接对齐 TablePlus 本地；密码仅 `.env`
