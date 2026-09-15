---
name: content-curator
description: >-
  小众审美内容策展：城市景观、室内设计、小众电子/爵士/R&B。
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

1. 领域是否落在三大主领域（城市 / 室内 / 音乐）或已批准的扩展？**禁止 polar / 南极 / 极地题材。**
2. **城市景观是否中国可指认？** 其它领域是否可追溯？
3. **情感是否正向或平？** 拒猎奇、惊悚、灾难消融等负向主导。
4. **图源口径**：以 `authentic-xhs-voice` 为准（元数据为主，正文禁说明书腔）。
5. 熟悉度惩罚：网红机位/下沉歌手无新角度？
6. 文案是否通过 `authentic-xhs-voice` 自检（无升华腔、无假经历）？
7. 输出：`title`、`body`、`tags`、`images`（含 source/license）、`rationale`、`nicheScore`、`tasteScore`（须过同领域素材品味线，见 `001`）。

## 输出格式

对每条候选使用结构化块，便于后续入库：

```yaml
domain: cityscape|interior|music|extended:<name>
title: ...
body: |
  ...
tags: []
image_plan: []
rationale: ...
nicheScore: 0-100
```
