# 001 — 内容流水线

## 目标

实现闭环：`挖掘 → 生成 3 候选 → 审阅预览 → 发布/草稿 → 指标回流 → 策略调整`。

## 日更节奏

| 步骤 | 说明 |
|------|------|
| 飞书提醒 | GitHub Action 每天发一条飞书机器人消息，提醒运营指挥 Cursor Agent |
| Agent 生成 | **Cursor Agent 用自身能力**写 3 条候选（对照素材库 + `authentic-xhs-voice`），**不**调用外部付费 LLM API |
| 落库 | Agent 写入 `apps/api/data/agent_daily.json` 后执行 `python -m app.jobs.ingest_candidates`（或 `POST /api/jobs/ingest-candidates`） |
| 领域分配 | 3 条尽量覆盖不同领域；跳过 `RejectedFingerprint` |
| 审阅窗口 | `pending` → `published` / `draft`；**拒绝 = 物理删除** + 指纹 |
| 立即发布 / 草稿 | 同前 |

禁止：把「今日 3 候选」永久硬编码进仓库代码当日更；禁止依赖 `LLM_API_KEY` 跑日更。

## 候选帖数据结构（逻辑）

```text
CandidatePost
  id, dateBatch, domain, status, themeKey
  title, body, tags[]
  images[]
  coverIndex, rationale
  nicheScore, tasteScore, tastePass, tasteFeatures
  createdAt, reviewedAt, publishedAt
  externalNoteId
```

## 状态机

```text
pending ──publish──► published
   │
   └──draft──► draft ──publish──► published
   └──reject──► (DELETE row) + RejectedFingerprint
```

## 生成原则

- **起号系统**：飞书提醒人 → Cursor Agent 写稿 → ingest 落库 → `/review` 只读 DB。
- 信息基于素材库 + 白名单数据源；图文同源；遵守 `authentic-xhs-voice`。
- **品味门槛**：以 `taste_scorer` **规则门禁**为主（voice / 白名单 / 图文对齐 / P75）；不强制外部 LLM 打分。
- Agent 操作手册：`.cursor/skills/daily-agent-generate/SKILL.md`。

## 拒绝指纹（RejectedFingerprint）

```text
kind: theme_key | title_hash | note_id
value, reason, createdAt
```

## 飞书提醒（GitHub Actions）

- Workflow：`.github/workflows/daily-feishu-remind.yml`（`schedule` + `workflow_dispatch`）。
- Secrets：仅需 `FEISHU_WEBHOOK_URL`（群自定义机器人 Webhook）。
- 不连 MySQL、不调 LLM，几乎零成本。

## 素材库（ReferenceMaterial）= 真实优质帖 / 白名单站记录

素材库存的是白名单站上**可核验的真实优质内容元数据**（小红书为主；亦可来自抖音 / IG 商业摄影 / 设计站 / Bandcamp·RA·Discogs·厂牌站 / Are.na·Pinterest 看板信号），不是「结构参照：xxx」假条目。**不含**已下线的极地（polar）域。小红书同时是**结构参照**与**正式数据源**。

```text
ReferenceMaterial
  id, domain, keyword          # keyword 如「审美积累」/领域检索词；domain ∈ cityscape|interior|music|meta|extended|board
  source_site                  # xhs|douyin|instagram|bandcamp|ra|discogs|arena|pinterest|design_site|label|wikimedia|…
  theme_key                    # 同主题打包键，如 city:shanghai-puxi-neitou
  note_id                      # 平台笔记 ID（可核验；非 xhs 可空）
  title_observed               # 公开标题
  author_hint                  # 作者昵称（公开可见）
  likes_hint / collects_hint / comments_hint  # 互动量级（公开可见）
  cover_url / images_json      # 封面或图组公开 URL（若可得）
  body_excerpt                 # 正文摘要（短摘，非全文搬运）
  taste_tags[]                 # 从真实帖推断的审美标签
  quality_score                # 互动分位 + 人工/规则标定 0–100
  source_url                   # 公开链接
  license_ok                   # 第三方内容默认 false（不可当己方输出）
  collected_at, notes
```

- 入库方式：官方网页（已登录会话或公开可见字段）由人工/Agent 采集元数据落库；密钥/Cookie 不入库、不提交 `.env`。
- **入库门禁**（阻塞）：禁止 `domain=polar`；禁止标题/摘要含南极等已禁题材；情感须**正向或平**；`source_site` 须在白名单；实现见 `material_gates.py` / `source_registry.py`。
- 用途：`taste_score` 标尺 + theme pack 输入；**不得**把他人正文/原图当生成输出（见 `authentic-xhs-voice`）。
- **日更生成**：先组 theme pack（事实 + 同主题图）再写文案；检索词见 `research_keywords.py`；站点见 `source_registry.py`。
- **审阅展示**：`/review` 展示当日恰好 3 条正向候选；`cand-neg-*` 等负例可保留在库供 taste 回归，但不计入「今日 3 候选」。

## 品味打分（taste_score，发布前）

与 `004` 爆款分分离：

```text
benchmark    = max(85, percentile_75(quality_score | same domain))
taste_score  = taste_scorer 规则启发分（voice / 白名单 / 图文对齐等）
taste_pass   = taste_score >= benchmark AND voice_pass AND 白名单 AND 图文对齐
```

- 日更主路径不依赖外部 `LLM_API_KEY`；Agent 写稿时已按 Skill 自检。
- `taste_features` 含对照素材样本与失败原因。

## 回流

- 发布后进入指标采集队列（见 `004-analytics-virality.md`）。
- 爆款评分结果写回，供下一日选题加权（已表现好的领域/结构升权，翻车结构降权）。
- 审阅拒绝原因若含品味问题，可回写素材负例标签（后续迭代）。
