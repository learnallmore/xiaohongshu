# 小红书起号系统

AI Native 运营台：每日生成 3 条小众审美生活方式候选帖，模拟小红书预览审阅，合规发布到真实账号，并回流访问量做爆款判断。

> **当前阶段：Phase 1 — 仅 AI 工作流基建**（Spec / Rules / Skills / Hooks / CI）。业务应用从 Phase 2 开始。

## 快速导航

| 文档 | 用途 |
|------|------|
| [AGENTS.md](AGENTS.md) | Agent 开工入口 |
| [specs/](specs/) | 产品与技术 Spec |
| [.cursor/rules/](.cursor/rules/) | 持久规则 |
| [.cursor/skills/](.cursor/skills/) | 领域 Skills |
| [.cursor/hooks.json](.cursor/hooks.json) | 危险 git 拦截 + 收工审查 |

## AI Native 开发流程

1. **先 Spec 后代码**：改行为先更新 `specs/00x-*.md`。
2. **Agent 遵守** `AGENTS.md` 与 `.cursor/rules/`。
3. **本地 Hook**：`beforeShellExecution` 拦截 force push / `git config` / `reset --hard` / `--no-verify`；`stop` 触发收工 Spec 一致性审查。
4. **CI**：PR/push 检查必需 Spec 文件存在，并拒绝疑似密钥入库。
5. **合并前建议**：对 branch changes 使用 Cursor Bugbot / Security Review。

手动跑 Spec 清单：

```bash
bash .cursor/hooks/spec-checklist.sh
```

## 路线图

- **Phase 1（当前）**：Git 隔离、Specs、Cursor 工作流、CI、凭证清单
- **Phase 2**：Next.js + Postgres 骨架、模拟小红书预览
- **Phase 3**：每日 3 候选生成 + 审阅状态机
- **Phase 4**：真实 Publisher + 指标回流 + 爆款评分

技术选型见 [specs/006-tech-stack.md](specs/006-tech-stack.md)。发布契约见 [specs/005-publisher-adapter.md](specs/005-publisher-adapter.md)。

## 你需要准备的材料

### A. 远程推送（现在）

| 项 | 说明 | 状态 |
|----|------|------|
| GitHub 账号 | `gh auth status` 成功，或已配置 SSH | 待你确认 |
| 仓库可见性 | **建议 private**（含运营策略） | 待你指定 |
| 仓库名 | 默认 `xiaohongshu` | 待你确认 |
| 授权 Agent | 明确说「执行：首 commit + 创建远程并 push」后才会推送 | 未授权则只留本地仓库 |

本机已在项目目录初始化独立 `main` 分支（**不再**使用家目录误挂的 git）。

建议你本地确认：

```bash
cd /Users/shijiacheng/IdeaProjects/xiaohongshu
git rev-parse --show-toplevel   # 应输出本项目路径
gh auth status                  # 推远程前需要
```

### B. 真实发帖 2C（进入 Phase 4 前）

| 项 | 说明 |
|----|------|
| 接入方式 | 官方开放平台 App，或你选定的**合规**第三方 |
| `app_id` / `app_secret` | 只放本地 `.env`，永不提交 |
| OAuth / Device Grant | Web 服务端换 token 的文档链接 |
| **笔记发布** API | method、字段、图片上传流程；确认个人创作者权限是否开放 |
| **笔记数据** API | 浏览 / 点赞 / 收藏 / 评论（供定时任务） |
| 测试账号 | 干跑用，避免直接打正式号 |
| 图片版权策略 | AI 生成 / 自有拍摄 / 授权图库（禁止未授权转载） |

合规底线：若官方未开放发笔记权限，产品会停在适配器缺口提示，**不会**改走 Cookie/逆向方案。

环境变量占位（Phase 2+ 使用，可先建 `.env` 本地文件）：

```bash
PUBLISHER_DRIVER=noop
XHS_APP_ID=
XHS_APP_SECRET=
XHS_ACCESS_TOKEN=
XHS_REFRESH_TOKEN=
THIRD_PARTY_PUBLISH_URL=
THIRD_PARTY_API_KEY=
```

## 许可证与内容

运营内容与图片版权由账号所有者负责；仓库代码默认仅供私有使用，除非你另行声明开源协议。
