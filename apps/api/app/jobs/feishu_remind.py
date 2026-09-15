"""CLI / 被 GHA 调用：向飞书群发日更提醒（不调用 LLM）。"""

from __future__ import annotations

import os
import sys

import httpx


DEFAULT_TEXT = (
    "【棱镜日更】该指挥 Cursor Agent 生成今日 3 条候选了。\n"
    "对 Agent 说：按 daily-agent-generate 生成今日候选并落库。\n"
    "审阅：http://127.0.0.1:8000/review"
)


def main() -> int:
    url = (os.environ.get("FEISHU_WEBHOOK_URL") or "").strip()
    if not url:
        print("未配置 FEISHU_WEBHOOK_URL（飞书自定义机器人 Webhook）")
        return 1
    text = (os.environ.get("FEISHU_REMIND_TEXT") or DEFAULT_TEXT).strip()
    payload = {"msg_type": "text", "content": {"text": text}}
    with httpx.Client(timeout=30.0) as client:
        resp = client.post(url, json=payload)
        print("status", resp.status_code, resp.text[:300])
        return 0 if resp.status_code < 300 else 1


if __name__ == "__main__":
    sys.exit(main())
