# 001 — 内容流水线

## 目标

实现闭环：`挖掘 → 生成 3 候选 → 审阅预览 → 发布/草稿 → 指标回流 → 策略调整`。

## 日更节奏

| 步骤 | 说明 |
|------|------|
| 定时生成 | 每日固定时点（默认本地 08:00）生成恰好 **3** 条候选 |
| 领域分配 | 3 条尽量覆盖不同领域或同一领域不同角度，避免同质化 |
| 审阅窗口 | 候选状态：`pending` → `approved` / `rejected` / `published` / `draft` |
| 立即发布 | 审阅通过且勾选「立即发布」→ 调用 Publisher 适配器 |
| 仅保存 | 写入草稿，可稍后发布 |

## 候选帖数据结构（逻辑）

```text
CandidatePost
  id, dateBatch, domain, status
  title, body, tags[]
  images[]          # 有序图组，含宽高与来源元数据
  coverIndex        # 封面图索引
  rationale         # AI 为何推荐（内部可见）
  nicheScore        # 小众度自评
  createdAt, reviewedAt, publishedAt
  externalNoteId    # 发布后平台笔记 ID
```

## 状态机

```text
pending ──approve──► approved ──publish──► published
   │                    │
   │                    └──save──► draft ──publish──► published
   └──reject──► rejected
```

## 生成原则

- 信息尽量基于真实、可核验的地点/风格/艺人线索；禁止捏造「假打卡攻略」误导。
- 文案服务审美与氛围，避免标题党与违规词。
- 图片必须有合法来源（见 `005` 版权策略）；生成时记录 `source` / `license`。

## 回流

- 发布后进入指标采集队列（见 `004-analytics-virality.md`）。
- 爆款评分结果写回，供下一日选题加权（已表现好的领域/结构升权，翻车结构降权）。
