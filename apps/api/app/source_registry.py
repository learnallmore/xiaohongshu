"""领域审美数据源白名单（与 specs/002 同步）。

采集 / 配图须落在白名单站；Wikimedia / Unsplash 仅作主题匹配时的授权备援。
"""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class SourceSite:
    key: str
    name: str
    base_url: str
    roles: tuple[str, ...]  # visual | fact | structure
    host_suffixes: tuple[str, ...]


DOMAIN_SOURCES: dict[str, list[SourceSite]] = {
    "cityscape": [
        SourceSite(
            "xhs",
            "小红书",
            "https://www.xiaohongshu.com",
            ("visual", "fact", "structure"),
            ("xiaohongshu.com", "xhscdn.com", "xiaohongshu.com"),
        ),
        SourceSite(
            "douyin",
            "抖音",
            "https://www.douyin.com",
            ("visual", "fact"),
            ("douyin.com", "iesdouyin.com", "tiktokcdn.com"),
        ),
        SourceSite(
            "instagram",
            "Instagram 商业摄影",
            "https://www.instagram.com",
            ("visual", "fact"),
            ("instagram.com", "cdninstagram.com", "fbcdn.net"),
        ),
    ],
    "interior": [
        SourceSite(
            "xhs",
            "小红书",
            "https://www.xiaohongshu.com",
            ("visual", "fact", "structure"),
            ("xiaohongshu.com", "xhscdn.com"),
        ),
        SourceSite(
            "douyin",
            "抖音",
            "https://www.douyin.com",
            ("visual", "fact"),
            ("douyin.com", "iesdouyin.com"),
        ),
        SourceSite(
            "design_site",
            "Dezeen",
            "https://www.dezeen.com",
            ("visual", "fact"),
            ("dezeen.com",),
        ),
        SourceSite(
            "design_site",
            "ArchDaily",
            "https://www.archdaily.com",
            ("visual", "fact"),
            ("archdaily.com", "adsttc.com"),
        ),
        SourceSite(
            "design_site",
            "Designboom",
            "https://www.designboom.com",
            ("visual", "fact"),
            ("designboom.com",),
        ),
    ],
    "music": [
        SourceSite(
            "bandcamp",
            "Bandcamp",
            "https://bandcamp.com",
            ("visual", "fact"),
            ("bandcamp.com", "bcbits.com"),
        ),
        SourceSite(
            "ra",
            "Resident Advisor",
            "https://ra.co",
            ("fact", "visual"),
            ("ra.co", "residentadvisor.net"),
        ),
        SourceSite(
            "discogs",
            "Discogs",
            "https://www.discogs.com",
            ("fact", "visual"),
            ("discogs.com",),
        ),
        SourceSite(
            "label",
            "厂牌站",
            "https://",
            ("fact", "visual"),
            (),  # 见 MUSIC_LABELS
        ),
    ],
    "board": [
        SourceSite(
            "arena",
            "Are.na",
            "https://www.are.na",
            ("visual", "structure"),
            ("are.na",),
        ),
        SourceSite(
            "pinterest",
            "Pinterest",
            "https://www.pinterest.com",
            ("visual", "structure"),
            ("pinterest.com", "pinimg.com"),
        ),
    ],
}

# 厂牌种子（可扩展）；事实核验优先走厂牌站 / Discogs / Bandcamp
MUSIC_LABELS: list[dict[str, str]] = [
    {
        "key": "anjunadeep",
        "name": "Anjunadeep",
        "url": "https://anjunadeep.com",
        "hosts": "anjunadeep.com",
    },
    {
        "key": "roche-musique",
        "name": "Roche Musique",
        "url": "https://rochemusique.com",
        "hosts": "rochemusique.com",
    },
    {
        "key": "ed-banger",
        "name": "Ed Banger Records",
        "url": "https://www.edbangerrecords.com",
        "hosts": "edbangerrecords.com",
    },
]

# 稳定可链、主题匹配时可用的授权备援宿主（非首选社交源）
FALLBACK_HOST_SUFFIXES: tuple[str, ...] = (
    "wikimedia.org",
    "wikipedia.org",
    "upload.wikimedia.org",
    "thumb.wikimedia.org",
    "unsplash.com",
    "images.unsplash.com",
)

ALL_PRIMARY_HOST_SUFFIXES: tuple[str, ...] = tuple(
    sorted(
        {
            h
            for sites in DOMAIN_SOURCES.values()
            for s in sites
            for h in s.host_suffixes
            if h
        }
        | {lab["hosts"] for lab in MUSIC_LABELS if lab.get("hosts")}
    )
)


def host_allowed(host: str) -> bool:
    h = (host or "").lower().removeprefix("www.")
    if not h:
        return False
    for suf in ALL_PRIMARY_HOST_SUFFIXES + FALLBACK_HOST_SUFFIXES:
        if h == suf or h.endswith("." + suf) or h.endswith(suf):
            return True
    return False


def url_host_allowed(url: str) -> bool:
    try:
        host = urlparse(url).hostname or ""
    except Exception:
        return False
    return host_allowed(host)


def source_text_allowed(source: str) -> bool:
    """图片 source 元数据：含白名单站名/域名/厂牌名即过。"""
    s = (source or "").strip().lower()
    if not s:
        return False
    if "http://" in s or "https://" in s:
        # 尝试抽出 URL
        for part in s.replace(",", " ").split():
            if part.startswith("http"):
                if url_host_allowed(part):
                    return True
    needles = (
        "xiaohongshu",
        "小红书",
        "douyin",
        "抖音",
        "instagram",
        "dezeen",
        "archdaily",
        "designboom",
        "bandcamp",
        "discogs",
        "resident advisor",
        "ra.co",
        "are.na",
        "arena",
        "pinterest",
        "wikimedia",
        "commons",
        "anjunadeep",
        "roche",
        "ed banger",
        "edbanger",
        "unsplash",  # 备援，须另做主题对齐
    )
    return any(n in s for n in needles)
