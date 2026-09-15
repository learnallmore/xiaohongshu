# 004 — 访问量采集与爆款判定

## 目标

对已发布笔记定时拉取平台数据，结合账号基线判断内容是否具备爆款特征，并反馈到选题策略。

## 采集指标（最小集）

| 指标 | 用途 |
|------|------|
| views（浏览） | 主信号 |
| likes | 互动率 |
| collects（收藏） | 深度兴趣 |
| comments | 讨论度 |
| shares（若可得） | 传播 |

快照表按 `(noteId, capturedAt)` 存历史，便于画增长曲线。

## 定时任务

- 默认频率：发布后 1h、6h、24h、72h 各采一次；之后每日一次（可配置）。
- 失败重试：指数退避，告警进日志。
- 凭证：使用 Publisher/Analytics 同一官方 token 体系刷新。

## 爆款潜力评分（逻辑草案）

相对 **账号自身基线**（近 N 条中位数），而非绝对网红量级：

```text
engagementRate = (likes + collects * 1.5 + comments * 2) / max(views, 1)
viewMultiple   = views / max(baselineViewsMedian, 1)
score          = normalize(viewMultiple, engagementRate, earlyVelocity)
```

- `earlyVelocity`：前 6h 浏览相对历史同窗。
- 输出：`score`（0–100）+ `label`：`cold` / `normal` / `rising` / `viral_candidate`。
- 存 `ViralityAssessment`：score、label、features JSON、modelVersion、assessedAt。

## 策略回流

- `rising` / `viral_candidate`：同领域/同结构模板升权。
- `cold`：记录失败模式（标题党、图组过乱、领域错配等）供生成负例。

## 依赖

- 需要官方或合规第三方提供的 **笔记数据查询** 接口（见 README 凭证清单）。
- 无数据接口时：评分模块保持接口，标记 `dataSource: unavailable`。
