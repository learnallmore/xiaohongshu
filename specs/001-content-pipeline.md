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
  tasteScore        # 相对素材表的品味分 0–100
  tastePass         # 是否达到同领域素材中位线
  tasteFeatures     # 打分明细 JSON
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
- **品味门槛**：生成后必须跑 `taste_score`（见下）；未过同领域素材中位线的候选不得标为可发。

## 参照素材表（ReferenceMaterial）

调研小红书「审美积累」及四大领域优质笔记时，只落**结构与审美特征**，禁止未授权全文/原图入库。

```text
ReferenceMaterial
  id, domain, keyword
  title_observed      # 公开标题（短文本）
  author_hint         # 可选
  likes_hint          # 可选互动量级提示
  structure_notes     # 封面节奏、系列标题、图组逻辑等
  taste_tags[]        # 如 collage / low-sat / series-day / china-place
  quality_score       # 策展标定 0–100（品味标尺）
  source_url          # 可选公开搜索/笔记链接
  license_ok          # 第三方内容默认 false
  collected_at, notes
```

- 入库方式：人工/Agent 浏览器观察后写入；**禁止** Cookie 抓包、逆向签名、Selenium 非官方模拟登录爬取。
- 用途：生成 few-shot 结构参照 + `taste_score` 标尺；**不得**把他人正文当生成输出。

## 品味打分（taste_score，发布前）

与 `004` 爆款分（发布后、相对账号基线）分离：

```text
taste_score  = 加权(可追溯图源, 诚实人设, 领域特异, 标题克制, 标签卫生,
                    图组完整, 去AI味, 与同领域高分素材 taste_tags 对齐)
benchmark    = max(72, median(quality_score | same domain))
taste_pass   = taste_score >= benchmark
```

- 写入 `CandidatePost.taste_score` / `taste_features` / `taste_pass`。
- `nicheScore` 仍表示小众度；`taste_score` 表示「够不够得上素材表品味」。

## 回流

- 发布后进入指标采集队列（见 `004-analytics-virality.md`）。
- 爆款评分结果写回，供下一日选题加权（已表现好的领域/结构升权，翻车结构降权）。
- 审阅拒绝原因若含品味问题，可回写素材负例标签（后续迭代）。
