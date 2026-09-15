"""OpenAI 兼容 Chat Completions 客户端。"""

from __future__ import annotations

import json
import re
from typing import Any

import httpx

from app.config import get_settings


class LlmError(RuntimeError):
    pass


def llm_configured() -> bool:
    return bool(get_settings().llm_api_key.strip())


def chat_json(system: str, user: str, *, temperature: float = 0.7) -> dict[str, Any]:
    """调用 LLM，要求返回 JSON object。"""
    settings = get_settings()
    if not settings.llm_api_key.strip():
        raise LlmError("LLM_API_KEY 未配置")

    url = settings.llm_base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": settings.llm_model,
        "temperature": temperature,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    headers = {
        "Authorization": f"Bearer {settings.llm_api_key}",
        "Content-Type": "application/json",
    }
    with httpx.Client(timeout=90.0) as client:
        resp = client.post(url, headers=headers, json=payload)
        if resp.status_code >= 400:
            raise LlmError(f"LLM HTTP {resp.status_code}: {resp.text[:400]}")
        data = resp.json()
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as e:
        raise LlmError(f"LLM 响应结构异常: {data!r}") from e

    content = (content or "").strip()
    if content.startswith("```"):
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as e:
        raise LlmError(f"LLM 未返回合法 JSON: {content[:300]}") from e
    if not isinstance(parsed, dict):
        raise LlmError("LLM JSON 根节点必须是 object")
    return parsed
