---
name: content-curator
description: >-
  小众审美内容策展：城市景观、室内设计、小众电子/爵士/R&B、极地风景。
  在生成候选帖、扩展领域、评审 niche 度时使用。
---

# Content Curator

## 何时使用

- 生成或评审每日候选帖
- 判断主题是否足够小众
- 扩展邻近生活方式领域

## 必读

- `specs/002-domains.md`
- `specs/001-content-pipeline.md`

## 策展清单

1. 领域是否落在四大主领域或已批准的扩展？
2. 熟悉度惩罚：是否网红机位/下沉歌手无新角度？
3. 真实可核验线索（地点、风格流派、厂牌/制作人）是否站得住？
4. 图文是否服务氛围而非资讯堆砌？
5. 输出候选时包含：`title`、`body`、`tags`、`images` 意图、`rationale`、`nicheScore`（0–100）。

## 输出格式

对每条候选使用结构化块，便于后续入库：

```yaml
domain: cityscape|interior|music|polar|extended:<name>
title: ...
body: |
  ...
tags: []
image_plan: []
rationale: ...
nicheScore: 0-100
```
