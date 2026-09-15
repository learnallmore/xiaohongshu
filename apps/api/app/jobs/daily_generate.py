"""废弃：外部 LLM 日更已改为 Cursor Agent + 飞书提醒。

保留模块以免旧文档误调用；请改用：
  python -m app.jobs.ingest_candidates
"""

from __future__ import annotations

import sys


def main() -> int:
    print(
        "daily_generate（外部 LLM API）已废弃。\n"
        "日更流程：飞书提醒 → 指挥 Cursor Agent（Skill: daily-agent-generate）"
        " → 写入 data/agent_daily.json → python -m app.jobs.ingest_candidates\n"
        "飞书提醒作业：python -m app.jobs.feishu_remind"
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
