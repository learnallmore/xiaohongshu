"""人声/去 AI 味硬过滤：检出元叙事、说明书腔、直角引号等即打掉。"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# 元叙事：读者不需要知道运营/素材库/学习结构
META_NARRATIVE = (
    "素材库",
    "只学结构",
    "学习结构",
    "不搬别人",
    "不搬封面",
    "不搬运",
    "参照素材",
    "对齐素材",
    "参考那批帖",
    "那批帖",
    "写进正文",
    "图源写",
    "审阅侧栏",
)

# 说明书式图源/版权腔（合法来源应进图片元数据，不进读者正文）
LICENSE_MANUAL = (
    "Unsplash License",
    "Unsplash 授权",
    "授权 Unsplash",
    "摄影师见原页",
    "摄影师见各图原页",
    "图源与授权",
    "来源授权",
    "图1–3来源",
    "图1-3来源",
    "图 1–3：",
    "图1–3：",
    "图1-3：",
    "图 1-3：",
    "License",
)

# 升华腔 / 假编辑腔（命中即扣；多命中硬失败）
SUBLIME_PHRASES = (
    "负空间",
    "呼吸感",
    "材质对话",
    "生活方式号",
    "适合作为",
    "见证了",
    "彰显了",
    "不可或缺",
    "氛围感拉满",
    "高级感满满",
)

CORNER_QUOTE_RE = re.compile(r"[「」]")


@dataclass
class VoiceResult:
    passed: bool
    hits: list[str] = field(default_factory=list)
    corner_quote_count: int = 0

    def as_features(self) -> dict:
        return {
            "voice_pass": self.passed,
            "voice_hits": self.hits[:12],
            "corner_quote_count": self.corner_quote_count,
        }


def scan_voice(title: str, body: str) -> VoiceResult:
    """扫描标题+正文；任一硬规则命中 → passed=False。"""
    blob = f"{title or ''}\n{body or ''}"
    hits: list[str] = []

    for p in META_NARRATIVE:
        if p in blob:
            hits.append(f"元叙事:{p}")

    for p in LICENSE_MANUAL:
        if p in blob:
            hits.append(f"说明书腔:{p}")

    sublime = [p for p in SUBLIME_PHRASES if p in blob]
    for p in sublime:
        hits.append(f"升华腔:{p}")

    quotes = CORNER_QUOTE_RE.findall(blob)
    n_quotes = len(quotes)
    if n_quotes > 0:
        hits.append(f"直角引号×{n_quotes}")

    # 硬失败：元叙事 / 说明书腔 / 任意「」 / 任一升华腔
    hard = bool(hits)
    return VoiceResult(passed=not hard, hits=hits, corner_quote_count=n_quotes)
