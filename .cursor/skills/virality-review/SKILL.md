---
name: virality-review
description: >-
  基于账号基线与互动指标判断笔记是否像爆款。
  在解读 metrics、写 ViralityAssessment、调整选题权重时使用。
---

# 爆款评审

## 何时使用

- 定时任务产出新指标快照后
- 运营者询问某帖表现
- 调整下一日领域/模板权重

## 必读

- `specs/004-analytics-virality.md`

## 评审步骤

1. 拉取该笔记历史快照与账号近 N 条中位数基线。
2. 计算 `engagementRate`、`viewMultiple`、`earlyVelocity`。
3. 输出 `score`（0–100）与 `label`：`cold` | `normal` | `rising` | `viral_candidate`。
4. 用 2–3 句说明主因（封面、领域、发布时间、互动结构等），避免玄学表述。
5. 给出可执行的下一次选题建议（升权/降权结构）。

## 注意

- 相对基线，不与头部网红绝对量级比较。
- 无数据源时明确 `dataSource: unavailable`，不要伪造指标。
