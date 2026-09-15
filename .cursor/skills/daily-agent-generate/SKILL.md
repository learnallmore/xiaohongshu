---
name: daily-agent-generate
description: >-
  飞书提醒后的日更：用 Cursor Agent 自身能力写 3 条候选并落库。
  用户说「生成今日候选 / 日更 / 按 daily-agent-generate」时使用。不调用外部 LLM API。
---

# 日更：Agent 写稿并落库

## 目标

产出今日恰好 **3** 条 `CandidatePost` 到 MySQL，供 `/review` 审阅。  
**文案由本 Agent 直接写**，不要调用 `LLM_API_KEY` / `daily_generate`。

## 步骤（强制顺序）

1. 读 `specs/002-domains.md`、`authentic-xhs-voice`、`source_registry` / `research_keywords`。
2. 从 DB 或 `GET /api/materials` 取同域高质量素材（有封面、高赞）；跳过已拒绝指纹主题。
3. 选定 3 个不同领域（优先 cityscape / interior / music），每条绑定 `theme_key`。
4. **图文同源**：图 URL 来自同主题素材封面或白名单/授权备援链；禁止耳机/无关库存图。
5. 写 `title` / `body` / `tags`：禁直角引号「」、禁元叙事、禁说明书图源腔。
6. 写入 [`apps/api/data/agent_daily.json`](../../apps/api/data/agent_daily.json)（格式见下）。
7. 执行：
   ```bash
   cd apps/api && .venv/bin/python -m app.jobs.ingest_candidates
   ```
8. 打开 `/review` 确认 3 条；向用户汇报标题与 `taste_pass`。

## JSON 格式

```json
{
  "candidates": [
    {
      "domain": "cityscape",
      "domain_label": "顶级城市景观 · 上海",
      "theme_key": "cityscape:上海浦西内透",
      "title": "...",
      "body": "...",
      "tags": ["上海", "浦西"],
      "rationale": "内部备注",
      "niche_score": 82,
      "images": [
        {
          "url": "https://...",
          "source": "xhs/关键词/note_id · 标题摘要",
          "license": "third-party-preview; license_ok=false",
          "width": 1080,
          "height": 1440
        }
      ]
    }
  ]
}
```

必须恰好 3 条；每条至少 1 张图（建议 3 张）。

## 禁止

- 改 `seed.py` 当今日更
- 调用外部付费 LLM 生成正文
- 未授权搬运他人全文原图当输出
