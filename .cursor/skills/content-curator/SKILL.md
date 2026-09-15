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
- **`.cursor/skills/authentic-xhs-voice/SKILL.md`（真实可追溯 + 去 AI 味，阻塞级）**

## 策展清单

1. 领域是否落在四大主领域或已批准的扩展？
2. **城市景观是否中国可指认？** 其它领域是否可追溯？
3. **正文是否写明图源给读者看？**（仅元数据不够）
4. 熟悉度惩罚：网红机位/下沉歌手无新角度？
5. 文案是否通过 `authentic-xhs-voice` 自检（无升华腔、无假经历）？
6. 输出：`title`、`body`、`tags`、`images`（含 source/license）、`rationale`、`nicheScore`。

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
