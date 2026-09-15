"""Theme packs：同主题事实 + 同主题图组（图文同源输入）。

图优先 Wikimedia Commons CC（稳定外链备援）；事实链自白名单站
（小红书关键词 / Discogs·厂牌 / 设计语境）。禁止通用库存拼凑。
"""

from __future__ import annotations

THEME_PACKS: dict[str, dict] = {
    "city:shanghai-puxi-neitou": {
        "domain": "cityscape",
        "domain_label": "顶级城市景观 · 上海浦西",
        "entities": ["上海", "浦西", "内透", "黄浦江", "蓝调", "外滩"],
        "facts": {
            "place": "上海浦西 · 黄浦江沿岸",
            "angle": "蓝调内透：楼体剪影 + 窗内办公灯",
            "source_chain": "xhs关键词「上海浦西内透」+ Wikimedia Commons 浦西/外滩夜景 CC",
        },
        "title": "浦西蓝调，楼里还亮着灯",
        "body": (
            "加班走到黄浦江边那段浦西。\n"
            "玻璃幕墙里零散的办公灯还亮着，楼体本身反而成了剪影。"
            "本地人说这叫内透。\n"
            "蓝调那十几分钟最干净，灯全开之后信息量就太大了。"
        ),
        "tags": ["上海", "浦西", "内透", "蓝调", "城市天际线"],
        "rationale": "theme city:shanghai-puxi-neitou；图为 Commons 浦西/蓝调夜景，与正文同主题。",
        "niche_score": 82,
        "images": [
            {
                "id": "img-c1-1",
                "sort_order": 0,
                "url": (
                    "https://thumb.wikimedia.org/wikipedia/commons/thumb/8/86/"
                    "Blue_hour_view_of_the_Bund_from_the_Shanghai_World_Financial_Center_dllu.jpg/"
                    "1280px-Blue_hour_view_of_the_Bund_from_the_Shanghai_World_Financial_Center_dllu.jpg"
                ),
                "width": 1280,
                "height": 846,
                "source": "Wikimedia Commons / Blue hour Bund from SWFC (Dllu) CC BY-SA 4.0 · theme 上海蓝调",
                "license": "CC BY-SA 4.0",
            },
            {
                "id": "img-c1-2",
                "sort_order": 1,
                "url": "https://upload.wikimedia.org/wikipedia/commons/6/66/Shanghai_Puxi_at_Night.jpg",
                "width": 1200,
                "height": 800,
                "source": "Wikimedia Commons / Shanghai Puxi at Night · theme 浦西夜景内透",
                "license": "CC (see file page)",
            },
            {
                "id": "img-c1-3",
                "sort_order": 2,
                "url": (
                    "https://thumb.wikimedia.org/wikipedia/commons/thumb/7/79/"
                    "Puxi_Shanghai_November_2017.jpg/1280px-Puxi_Shanghai_November_2017.jpg"
                ),
                "width": 1280,
                "height": 853,
                "source": "Wikimedia Commons / Puxi Shanghai November 2017 · theme 浦西天际线",
                "license": "CC (see file page)",
            },
        ],
    },
    "interior:eclectic-linework": {
        "domain": "interior",
        "domain_label": "室内设计 · 折衷主义参考",
        "entities": ["折衷", "线脚", "中古", "室内", "比例"],
        "facts": {
            "style": "折衷主义 / 古典线脚 + 现代家具并置",
            "source_chain": "xhs关键词「折衷主义室内设计」+ Commons Art Deco / 折衷室内 CC",
        },
        "title": "折衷一点，乱也能稳",
        "body": (
            "古典线脚、现代沙发、中间一盏中古灯，居然不打架。\n"
            "比例对了，乱一点反而稳；比例错了，再贵也像样板间堆货。\n"
            "参考图，不是我家。层高和采光才是落地关键。"
        ),
        "tags": ["折衷主义", "室内设计", "中古", "线脚"],
        "rationale": "theme interior:eclectic-linework；图为同风格室内实景 CC，非无关软装拼贴。",
        "niche_score": 84,
        "images": [
            {
                "id": "img-i1-1",
                "sort_order": 0,
                "url": (
                    "https://thumb.wikimedia.org/wikipedia/commons/thumb/5/50/"
                    "5_Strada_Tache_Ionescu%2C_Bucharest_%2801%29.jpg/"
                    "1280px-5_Strada_Tache_Ionescu%2C_Bucharest_%2801%29.jpg"
                ),
                "width": 1280,
                "height": 960,
                "source": "Wikimedia Commons / Strada Tache Ionescu (01) · theme 折衷线脚",
                "license": "CC (see file page)",
            },
            {
                "id": "img-i1-2",
                "sort_order": 1,
                "url": (
                    "https://thumb.wikimedia.org/wikipedia/commons/thumb/9/92/"
                    "5_Strada_Tache_Ionescu%2C_Bucharest_%2802%29.jpg/"
                    "1280px-5_Strada_Tache_Ionescu%2C_Bucharest_%2802%29.jpg"
                ),
                "width": 1280,
                "height": 960,
                "source": "Wikimedia Commons / Strada Tache Ionescu (02) · theme 折衷室内",
                "license": "CC (see file page)",
            },
            {
                "id": "img-i1-3",
                "sort_order": 2,
                "url": (
                    "https://thumb.wikimedia.org/wikipedia/commons/thumb/2/2e/"
                    "14A_Strada_Popa_Soare%2C_Bucharest_%2802%29.jpg/"
                    "1280px-14A_Strada_Popa_Soare%2C_Bucharest_%2802%29.jpg"
                ),
                "width": 1280,
                "height": 960,
                "source": "Wikimedia Commons / Strada Popa Soare interior · theme 折衷比例",
                "license": "CC (see file page)",
            },
        ],
    },
    "music:edbanger-breakbot": {
        "domain": "music",
        "domain_label": "电子音乐 · French House / Ed Banger",
        "entities": [
            "Breakbot",
            "Ed Banger",
            "French",
            "house",
            "By Your Side",
            "listening bar",
        ],
        "facts": {
            "artist": "Breakbot",
            "track": "By Your Side",
            "label_context": "French electro / Ed Banger 语境；可用 Discogs/厂牌页核验",
            "source_chain": "关键词 deep house 法国 → Breakbot；图为 Commons Breakbot/Ed Banger 现场与厂牌视觉",
        },
        "title": "今晚循环 Breakbot",
        "body": (
            "这周听 Breakbot 的 By Your Side。\n"
            "鼓点不冲，人声很薄，像 listening bar 里会播的慢热碟。\n"
            "French house 这一路，关灯听比刷热歌合集舒服。"
        ),
        "tags": ["Breakbot", "Ed Banger", "French House", "deep house", "listening bar"],
        "rationale": "theme music:edbanger-breakbot；图为 Breakbot/Ed Banger 同源视觉，非耳机库存图。",
        "niche_score": 86,
        "images": [
            {
                "id": "img-m1-1",
                "sort_order": 0,
                "url": "https://upload.wikimedia.org/wikipedia/commons/2/2f/Breakbot_%28cropped%29.jpg",
                "width": 800,
                "height": 1000,
                "source": "Wikimedia Commons / Breakbot (cropped) · theme Breakbot",
                "license": "CC (see file page)",
            },
            {
                "id": "img-m1-2",
                "sort_order": 1,
                "url": (
                    "https://thumb.wikimedia.org/wikipedia/commons/thumb/c/ca/"
                    "Breakbot_Revolution_Fest_2013.jpg/1280px-Breakbot_Revolution_Fest_2013.jpg"
                ),
                "width": 1280,
                "height": 853,
                "source": "Wikimedia Commons / Breakbot Revolution Fest 2013 · theme Breakbot live",
                "license": "CC (see file page)",
            },
            {
                "id": "img-m1-3",
                "sort_order": 2,
                "url": "https://upload.wikimedia.org/wikipedia/commons/1/17/Ed_Banger_Records.jpg",
                "width": 800,
                "height": 800,
                "source": "Wikimedia Commons / Ed Banger Records · theme 厂牌视觉",
                "license": "CC (see file page)",
            },
        ],
    },
}


def pack_to_seed_item(theme_key: str, post_id: str) -> dict:
    pack = THEME_PACKS[theme_key]
    return {
        "id": post_id,
        "theme_key": theme_key,
        "domain": pack["domain"],
        "domain_label": pack["domain_label"],
        "title": pack["title"],
        "body": pack["body"],
        "tags": pack["tags"],
        "rationale": pack["rationale"],
        "niche_score": pack["niche_score"],
        "images": pack["images"],
        "entities": pack["entities"],
    }
