"""领域 → 搜索关键词列表（供素材采集 / 下次自动采）。

用户指定 + 自扩；与 specs/002 同步。站点白名单见 source_registry.py。
不含已下线 polar。
"""

from __future__ import annotations

# domain key → keywords（小红书等白名单站搜索用）
RESEARCH_KEYWORDS: dict[str, list[str]] = {
    "interior": [
        "折衷主义室内设计",  # 用户指定
        "包豪斯室内美学",
        "巴洛克室内设计",
        "野兽派混凝土室内",
        "日式现代室内",
    ],
    "cityscape": [
        "上海浦西内透",  # 用户指定
        "重庆夜景天际线",
        "深圳湾天际线",
        "广州珠江新城夜景",
        "香港维多利亚港夜景",
    ],
    "music": [
        "deep house 法国",  # 用户指定
        "listening bar 爵士",
        "小众电子厂牌",
        "ambient jazz 黑胶",
        "法式浩室 French House",
    ],
    "meta": [
        "审美积累",
        "视觉审美板",
        "INS 摄影师 审美",
    ],
}


def all_keywords() -> list[tuple[str, str]]:
    """[(domain, keyword), ...] 扁平列表，便于采集脚本遍历。"""
    rows: list[tuple[str, str]] = []
    for domain, kws in RESEARCH_KEYWORDS.items():
        for kw in kws:
            rows.append((domain, kw))
    return rows
