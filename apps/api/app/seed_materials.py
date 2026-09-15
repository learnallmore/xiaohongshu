"""素材库种子：官方网页采集的小红书真实优质笔记元数据（2026-09-16）。

仅存公开可见字段；license_ok=False；禁止把他人全文当生成输出。
入库须过 material_gates（无 polar / 无南极题材 / 情感正向或平）。
"""

from __future__ import annotations

import json
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ReferenceMaterial
from app.services.material_gates import material_reject_reason


def _q(likes: int | None, title: str, bonus: int = 0) -> int:
    """互动分位 ⊕ 标题规则标定 → quality_score。"""
    likes = likes or 0
    if likes >= 50000:
        eng = 94
    elif likes >= 15000:
        eng = 91
    elif likes >= 8000:
        eng = 88
    elif likes >= 3000:
        eng = 85
    elif likes >= 1000:
        eng = 82
    elif likes >= 400:
        eng = 78
    elif likes >= 100:
        eng = 74
    else:
        eng = 68
    t = title or ""
    if any(x in t for x in ("保姆级", "必看", "攻略", "封神", "绝了", "速看")):
        eng -= 8
    if any(x in t for x in ("审美积累", "Day.", "INS", "摄影师", "艺术家")):
        eng += 3
    if any(x in t for x in ("包豪斯", "listening", "爵士", "天际线")):
        eng += 2
    return max(55, min(98, eng + bonus))


# 真实笔记（浏览器搜索/详情公开字段）；id 用 note_id 便于核验
MATERIALS: list[dict] = [
    # —— meta / 审美积累 ——
    {
        "id": "xhs-6a01dc6b000000003601aa5a",
        "domain": "meta",
        "keyword": "审美积累",
        "note_id": "6a01dc6b000000003601aa5a",
        "title_observed": "𝓶𝓲𝓼𝓽𝔂 𝓯𝓸𝓻𝓮𝓼𝓽",
        "author_hint": "Externalsunshine:)",
        "likes_hint": 17000,
        "collects_hint": 4887,
        "comments_hint": 215,
        "cover_url": (
            "https://sns-webpic-qc.xhscdn.com/202609160018/"
            "347417cdc540dabf622133b394cfd828/"
            "notes_pre_post/1040g3k83201g5bn7ig305q4tuqj6aii8b03fpuo!nc_n_webp_mw_1"
        ),
        "images": [
            "https://sns-webpic-qc.xhscdn.com/202609160020/"
            "b3e73b40eabfd14b17710f1540be51f6/"
            "notes_pre_post/1040g3k83201g5bn7ig7g5q4tuqj6aii8kvblmm0!nd_dft_wlteh_webp_3",
            "https://sns-webpic-qc.xhscdn.com/202609160020/"
            "44cad83980ad40623ca5b3b98975b47d/"
            "notes_pre_post/1040g3k83201g5bn7ig305q4tuqj6aii8b03fpuo!nd_dft_wlteh_webp_3",
        ],
        "body_excerpt": "#pinterest #审美积累",
        "taste_tags": ["collage", "low-sat", "atmosphere-title", "visual-board"],
        "source_url": "https://www.xiaohongshu.com/explore/6a01dc6b000000003601aa5a",
        "notes": "搜索「审美积累」高互动拼贴板；详情互动约 1.7万赞/4887藏。",
    },
    {
        "id": "xhs-6aa5080b000000000b03598f",
        "domain": "meta",
        "keyword": "审美积累",
        "note_id": "6aa5080b000000000b03598f",
        "title_observed": "Hey, it’s been a while since we last met",
        "author_hint": "羅dull",
        "likes_hint": 54000,
        "cover_url": (
            "https://sns-webpic-qc.xhscdn.com/202609160018/"
            "bfaa8b18a8ea9c951d075750ce1c3337/"
            "1040g0083250qe15a36005og6vnmoc39ggfnhv70!nc_n_webp_mw_1"
        ),
        "body_excerpt": "审美积累搜索高赞氛围人像/静物板（公开卡片）。",
        "taste_tags": ["atmosphere-title", "low-sat", "visual-board"],
        "source_url": "https://www.xiaohongshu.com/explore/6aa5080b000000000b03598f",
        "notes": "卡片 5.4万赞；公开标题/作者/封面。",
    },
    {
        "id": "xhs-6a16977f000000003701d077",
        "domain": "meta",
        "keyword": "审美积累",
        "note_id": "6a16977f000000003701d077",
        "title_observed": "📷「INS值得收藏的摄影师」 | 审美积累",
        "author_hint": "📷Mr.飯忒稀",
        "likes_hint": 10000,
        "cover_url": (
            "https://sns-webpic-qc.xhscdn.com/202609160018/"
            "4375ce39d7aab16d3758ece3716dab4d/"
            "notes_pre_post/1040g3k0320lo2baulm6g5nmr946g8smpuie8cto!nc_n_webp_mw_1"
        ),
        "body_excerpt": "策展口吻点名外部摄影师；栏目「审美积累」。",
        "taste_tags": ["curator-voice", "named-artist", "provenance-stated", "series-day"],
        "source_url": "https://www.xiaohongshu.com/explore/6a16977f000000003701d077",
        "notes": "卡片约 1万赞。",
    },
    {
        "id": "xhs-6a6dd54b000000003300a7f0",
        "domain": "meta",
        "keyword": "审美积累",
        "note_id": "6a6dd54b000000003300a7f0",
        "title_observed": "审美提升|Day.744|Ezgi Polat",
        "author_hint": "nRs（审美分享）",
        "likes_hint": 2631,
        "cover_url": (
            "https://sns-webpic-qc.xhscdn.com/202609160018/"
            "a59e77a121c930204fcd86cabd8fb67c/"
            "spectrum/1040g34o323auecq9ms005p4hf4h9evupbbq9j2g!nc_n_webp_mw_1"
        ),
        "body_excerpt": "连载 Day.N + 具名作品；审美连载结构。",
        "taste_tags": ["series-day", "named-artist", "provenance-stated"],
        "source_url": "https://www.xiaohongshu.com/explore/6a6dd54b000000003300a7f0",
        "notes": "卡片 2631 赞。",
    },
    {
        "id": "xhs-6a962f930000000026017025",
        "domain": "meta",
        "keyword": "审美积累",
        "note_id": "6a962f930000000026017025",
        "title_observed": "📷「INS值得收藏的艺术家」 | 审美积累",
        "author_hint": "📷Mr.飯忒稀",
        "likes_hint": 5514,
        "cover_url": (
            "https://sns-webpic-qc.xhscdn.com/202609160018/"
            "344d6b2cb3ea6c6266e7f8eb920559ff/"
            "1040g2sg324ibfkcanue05nmr946g8smpht2b7h0!nc_n_webp_mw_1"
        ),
        "body_excerpt": "艺术家策展合集；标签审美积累。",
        "taste_tags": ["curator-voice", "named-artist", "visual-board"],
        "source_url": "https://www.xiaohongshu.com/explore/6a962f930000000026017025",
        "notes": "卡片 5514 赞。",
    },
    # —— cityscape ——
    {
        "id": "xhs-6a8914660000000033022147",
        "domain": "cityscape",
        "keyword": "中国城市天际线",
        "note_id": "6a8914660000000033022147",
        "title_observed": "没想到深圳被评选为世界最佳城市天际线",
        "author_hint": "Liang_hhh",
        "likes_hint": 1439,
        "collects_hint": 395,
        "comments_hint": 287,
        "cover_url": (
            "https://sns-webpic-qc.xhscdn.com/202609160020/"
            "5a9b493f73c12fe9270ed5719ac4ba96/"
            "notes_pre_post/1040g3k03245hbjl4ga204bgk00rpajb9bbiag4o!nc_n_webp_mw_1"
        ),
        "images": [
            "https://sns-webpic-qc.xhscdn.com/202609160021/"
            "784fe100599aa701b03155ef359d914b/"
            "notes_pre_post/1040g3k03245hnio6nu204bgk00rpajb9pjj2ie0!nd_dft_wlteh_webp_3",
            "https://sns-webpic-qc.xhscdn.com/202609160021/"
            "13d62d46a7e94b56687e7a48ab3b93b5/"
            "notes_pre_post/1040g3k03245hbjl4ga204bgk00rpajb9bbiag4o!nd_dft_wlteh_webp_3",
        ],
        "body_excerpt": (
            "根据 Radical Storage 2026 城市天际线排名，深圳位居榜首；"
            "提及摩天楼数量/夜间可见度/密度等因素；"
            "前十含深圳、香港、武汉、广州、上海、重庆等中国城市。"
            "标签：#城市天际线 #深圳 #高密度城市"
        ),
        "taste_tags": ["china-place", "architecture", "skyline", "provenance-stated"],
        "source_url": "https://www.xiaohongshu.com/explore/6a8914660000000033022147",
        "notes": "详情已读：1439赞/395藏/287评；可核验深圳天际线。",
    },
    {
        "id": "xhs-6a211680000000003601b9a9",
        "domain": "cityscape",
        "keyword": "中国城市天际线",
        "note_id": "6a211680000000003601b9a9",
        "title_observed": "钱塘江边的杭州天际线合集",
        "author_hint": "拍片的Eon",
        "likes_hint": 344,
        "cover_url": (
            "https://sns-webpic-qc.xhscdn.com/202609160020/"
            "703a525f90fe9559fbe59f751cdfe79a/"
            "notes_pre_post/1040g3k83210056p87aa05ok32bt41rnhggbj8a0!nc_n_webp_mw_1"
        ),
        "body_excerpt": "杭州钱塘江滨水天际线合集（公开卡片）。",
        "taste_tags": ["china-place", "waterfront", "skyline", "multi-distance"],
        "source_url": "https://www.xiaohongshu.com/explore/6a211680000000003601b9a9",
        "notes": "卡片 344 赞。",
    },
    {
        "id": "xhs-6900abc6000000000400764a",
        "domain": "cityscape",
        "keyword": "中国城市天际线",
        "note_id": "6900abc6000000000400764a",
        "title_observed": "全屏封神挑战｜请全屏观看深圳的钢铁森林🌃",
        "author_hint": "鲸鱼蚀刻",
        "likes_hint": 513,
        "cover_url": (
            "https://sns-webpic-qc.xhscdn.com/202609160020/"
            "5808a93fba00bf95812ae3167cd54e70/"
            "1040g00831o6b4gb7mg005o1f6u108nrs0rlt6b8!nc_n_webp_mw_1"
        ),
        "body_excerpt": "深圳高密度立面/钢铁森林视角（公开卡片）。",
        "taste_tags": ["china-place", "architecture", "skyline"],
        "source_url": "https://www.xiaohongshu.com/explore/6900abc6000000000400764a",
        "notes": "标题含「封神」会在 quality 标定中扣分；仍作真实样本。",
    },
    {
        "id": "xhs-6a1ae43c0000000008026969",
        "domain": "cityscape",
        "keyword": "中国城市天际线",
        "note_id": "6a1ae43c0000000008026969",
        "title_observed": "杭州城市CBD风光",
        "author_hint": "青山夕照水悠悠",
        "likes_hint": 444,
        "cover_url": (
            "https://sns-webpic-qc.xhscdn.com/202609160020/"
            "51c2aae594b17eb6e5983ec5895527d0/"
            "notes_pre_post/1040g3k8320puj9rulm005o7f1hcg8bm79u8lp98!nc_n_webp_mw_1"
        ),
        "body_excerpt": "杭州 CBD 城市风光（公开卡片）。",
        "taste_tags": ["china-place", "architecture", "skyline"],
        "source_url": "https://www.xiaohongshu.com/explore/6a1ae43c0000000008026969",
        "notes": "卡片 444 赞。",
    },
    # —— interior ——
    {
        "id": "xhs-6a76c4310000000032023670",
        "domain": "interior",
        "keyword": "室内美学 包豪斯",
        "note_id": "6a76c4310000000032023670",
        "title_observed": "新创🔵 韩系包豪斯",
        "author_hint": "全案设计橙橙",
        "likes_hint": 5159,
        "cover_url": (
            "https://sns-webpic-qc.xhscdn.com/202609160020/"
            "af4cec0cdb49f197575abb098902c300/"
            "1040g2sg323jlkt7470705opc1s28sil6adt2dbo!nc_n_webp_mw_1"
        ),
        "body_excerpt": "韩系包豪斯室内案例（公开卡片标题点名流派）。",
        "taste_tags": ["style-named", "material-talk", "honest-framing"],
        "source_url": "https://www.xiaohongshu.com/explore/6a76c4310000000032023670",
        "notes": "卡片 5159 赞。",
    },
    {
        "id": "xhs-69cdebd60000000021007948",
        "domain": "interior",
        "keyword": "室内美学 包豪斯",
        "note_id": "69cdebd60000000021007948",
        "title_observed": "包豪斯风格｜极简主义的功能美学",
        "author_hint": "JSU Designs |軟裝美學",
        "likes_hint": 590,
        "cover_url": (
            "https://sns-webpic-qc.xhscdn.com/202609160020/"
            "de05cd43783efb508fbdece8bbd8e5ba/"
            "notes_pre_post/1040g3k031uep7crj1m005ob0d2agjh1ph65shlg!nc_n_webp_mw_1"
        ),
        "body_excerpt": "包豪斯×极简功能美学（公开卡片）。",
        "taste_tags": ["style-named", "material-talk", "provenance-stated"],
        "source_url": "https://www.xiaohongshu.com/explore/69cdebd60000000021007948",
        "notes": "卡片 590 赞。",
    },
    {
        "id": "xhs-6a19b0d00000000035024b5e",
        "domain": "interior",
        "keyword": "室内美学 包豪斯",
        "note_id": "6a19b0d00000000035024b5e",
        "title_observed": "超喜欢这种极简高级的包豪斯",
        "author_hint": "Joey的室介",
        "likes_hint": 945,
        "cover_url": (
            "https://sns-webpic-qc.xhscdn.com/202609160020/"
            "d9bc2dd11fff5b475c66f8d94df0bfc8/"
            "note_pre_post_uhdr/1040g3r8320oothvhmqe05piiglv2u04790bf338!nc_n_webp_mw_1"
        ),
        "body_excerpt": "极简包豪斯室内（公开卡片）。",
        "taste_tags": ["style-named", "material-talk"],
        "source_url": "https://www.xiaohongshu.com/explore/6a19b0d00000000035024b5e",
        "notes": "卡片 945 赞。",
    },
    {
        "id": "xhs-6a2b831a000000001c026026",
        "domain": "interior",
        "keyword": "室内美学 包豪斯",
        "note_id": "6a2b831a000000001c026026",
        "title_observed": "中古包豪斯的家，太有腔调了",
        "author_hint": "独立设计师魔术手",
        "likes_hint": 213,
        "cover_url": (
            "https://sns-webpic-qc.xhscdn.com/202609160020/"
            "5412b6ee5ef6343c542bcdf8e70268aa/"
            "1040g008321a5s9hb7e505pq2o4l080h1rv81ifo!nc_n_webp_mw_1"
        ),
        "body_excerpt": "中古包豪斯住宅腔调（公开卡片）。",
        "taste_tags": ["style-named", "honest-framing", "contrast"],
        "source_url": "https://www.xiaohongshu.com/explore/6a2b831a000000001c026026",
        "notes": "卡片 213 赞。",
    },
    # —— music ——
    {
        "id": "xhs-6a70a0a00000000025014c05",
        "domain": "music",
        "keyword": "小众爵士listening bar",
        "note_id": "6a70a0a00000000025014c05",
        "title_observed": "亚洲 6 家 Listening Bar 地图",
        "author_hint": "星辰氣象",
        "likes_hint": 280,
        "cover_url": (
            "https://sns-webpic-qc.xhscdn.com/202609160020/"
            "020967ea62fe1787ee16f760fc34c178/"
            "spectrum/1040g0k0323de756070005qbj7ng7b4o2g4d77l8!nc_n_webp_mw_1"
        ),
        "body_excerpt": "亚洲 Listening Bar 地图策展（公开卡片）。",
        "taste_tags": ["listening-space", "curator-voice", "niche-label"],
        "source_url": "https://www.xiaohongshu.com/explore/6a70a0a00000000025014c05",
        "notes": "卡片 280 赞；听音空间硬特征。",
    },
    {
        "id": "xhs-6a7175ad000000002203039d",
        "domain": "music",
        "keyword": "小众爵士listening bar",
        "note_id": "6a7175ad000000002203039d",
        "title_observed": "Purple rain🎵｜Jazz night in HZ🎷",
        "author_hint": "人间体验第n天",
        "likes_hint": 37,
        "cover_url": (
            "https://sns-webpic-qc.xhscdn.com/202609160020/"
            "7c28f91d1afd3dd292114c728f1f5fbf/"
            "1040g2sg323efhpa0g2l04a4ifljmv9ugoekgtio!nc_n_webp_mw_1"
        ),
        "body_excerpt": "杭州爵士夜场现场（公开卡片）。",
        "taste_tags": ["named-artist", "listening-space", "niche-label"],
        "source_url": "https://www.xiaohongshu.com/explore/6a7175ad000000002203039d",
        "notes": "小众互动偏低但领域贴合。",
    },
    {
        "id": "xhs-688a1aaa000000002302a513",
        "domain": "music",
        "keyword": "小众爵士listening bar",
        "note_id": "688a1aaa000000002302a513",
        "title_observed": "成都。。东湖公园。。爵士bar真的好chill🥺",
        "author_hint": "望春山",
        "likes_hint": 172,
        "cover_url": (
            "https://sns-webpic-qc.xhscdn.com/202609160020/"
            "dff24dd6bad6c0a46c9d59fdd81b521a/"
            "1040g2sg31kihvlebiol05pi5no5gu9dn7u0e68g!nc_n_webp_mw_1"
        ),
        "body_excerpt": "成都东湖公园爵士 bar（公开卡片，可指认地点）。",
        "taste_tags": ["listening-space", "china-place", "curator-voice"],
        "source_url": "https://www.xiaohongshu.com/explore/688a1aaa000000002302a513",
        "notes": "卡片 172 赞。",
    },
    {
        "id": "xhs-68f215e1000000000703979e",
        "domain": "music",
        "keyword": "小众爵士listening bar",
        "note_id": "68f215e1000000000703979e",
        "title_observed": "墨尔本｜大隐隐于市 黑胶唱片listening bar",
        "author_hint": "方乙久Fiona",
        "likes_hint": 186,
        "cover_url": (
            "https://sns-webpic-qc.xhscdn.com/202609160020/"
            "470162feea9716de34a235ec40265e4c/"
            "note_pre_post_uhdr/1040g3r831no2uufd4s8g5o2en7708i57kc92lv8!nc_n_webp_mw_1"
        ),
        "body_excerpt": "墨尔本黑胶 listening bar（公开卡片）。",
        "taste_tags": ["listening-space", "niche-label", "cover-aesthetic"],
        "source_url": "https://www.xiaohongshu.com/explore/68f215e1000000000703979e",
        "notes": "卡片 186 赞。",
    },
    # —— 本轮浏览器扩采（2026-09-16）——
    {
        "id": "xhs-681adb3d0000000021019472",
        "domain": "music",
        "keyword": "deep house 法国",
        "note_id": "681adb3d0000000021019472",
        "title_observed": "巴黎techno|半夜勇闯3家techno俱乐部",
        "author_hint": "查理君",
        "likes_hint": 401,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160033/d3facb34a2a0858f28e5bc1751a7451e/1040g00831h5tfvrjji00494kmihtn2ggfa4nl08!nc_n_webp_mw_1",
        "body_excerpt": "巴黎techno|半夜勇闯3家techno俱乐部（搜索卡片公开字段）",
        "taste_tags": ["listening-space", "named-artist", "curator-voice", "atmosphere-title"],
        "source_url": "https://www.xiaohongshu.com/explore/681adb3d0000000021019472",
        "notes": "浏览器搜索「deep house 法国」公开卡片；401赞。",
    },
    {
        "id": "xhs-66f8f777000000001a021312",
        "domain": "music",
        "keyword": "deep house 法国",
        "note_id": "66f8f777000000001a021312",
        "title_observed": "🇫🇷巴黎蹦迪哪家强 四层夜店🪩魔幻现实💃",
        "author_hint": "杨羊羊的巴黎日记",
        "likes_hint": 333,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160033/49cb2672f530d32b8dd005184e113551/1040g008318aqed2f0o0041pqaeies77t1jhqeu0!nc_n_webp_mw_1",
        "body_excerpt": "🇫🇷巴黎蹦迪哪家强 四层夜店🪩魔幻现实💃（搜索卡片公开字段）",
        "taste_tags": ["listening-space", "named-artist", "curator-voice", "atmosphere-title"],
        "source_url": "https://www.xiaohongshu.com/explore/66f8f777000000001a021312",
        "notes": "浏览器搜索「deep house 法国」公开卡片；333赞。",
    },
    {
        "id": "xhs-68bb9014000000001b037937",
        "domain": "music",
        "keyword": "deep house 法国",
        "note_id": "68bb9014000000001b037937",
        "title_observed": "[RYM榜单]House Music排名1-30",
        "author_hint": "摇滚的苏格拉没有底",
        "likes_hint": 137,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160033/a92ae4a51ae17f577e590d39c624d93f/notes_pre_post/1040g3k031m2rij2c586g5ol5ul4ocf9k1m5ja7g!nc_n_webp_mw_1",
        "body_excerpt": "[RYM榜单]House Music排名1-30（搜索卡片公开字段）",
        "taste_tags": ["listening-space", "named-artist", "curator-voice", "atmosphere-title"],
        "source_url": "https://www.xiaohongshu.com/explore/68bb9014000000001b037937",
        "notes": "浏览器搜索「deep house 法国」公开卡片；137赞。",
    },
    {
        "id": "xhs-684266c00000000012006630",
        "domain": "music",
        "keyword": "deep house 法国",
        "note_id": "684266c00000000012006630",
        "title_observed": "𝑻𝒐𝒏𝒊𝒈𝒉𝒕｜法国浩室音乐律动🍷",
        "author_hint": "Yuna Room",
        "likes_hint": 149,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160033/d1b8d0b6272a4662686342824bdcc0d0/1040g00831id8344n7q7048sh8mnkai8udoip830!nc_n_webp_mw_1",
        "body_excerpt": "𝑻𝒐𝒏𝒊𝒈𝒉𝒕｜法国浩室音乐律动🍷（搜索卡片公开字段）",
        "taste_tags": ["listening-space", "named-artist", "curator-voice", "atmosphere-title"],
        "source_url": "https://www.xiaohongshu.com/explore/684266c00000000012006630",
        "notes": "浏览器搜索「deep house 法国」公开卡片；149赞。",
    },
    {
        "id": "xhs-688b14bb00000000050043a8",
        "domain": "music",
        "keyword": "deep house 法国",
        "note_id": "688b14bb00000000050043a8",
        "title_observed": "🇫🇷一些工作｜在巴黎做声音后期的日常",
        "author_hint": "burger",
        "likes_hint": 66,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160033/6ae7fda2330ff2090917f197bf80e2b9/notes_pre_post/1040g3k031kjge2i22o105nurpmlgbopase2qhf8!nc_n_webp_mw_1",
        "body_excerpt": "🇫🇷一些工作｜在巴黎做声音后期的日常（搜索卡片公开字段）",
        "taste_tags": ["listening-space", "named-artist", "curator-voice", "atmosphere-title"],
        "source_url": "https://www.xiaohongshu.com/explore/688b14bb00000000050043a8",
        "notes": "浏览器搜索「deep house 法国」公开卡片；66赞。",
    },
    {
        "id": "xhs-68b84875000000001d00971e",
        "domain": "music",
        "keyword": "deep house 法国",
        "note_id": "68b84875000000001d00971e",
        "title_observed": "听完开心一整天～🌞法式House自带多巴胺！🥰",
        "author_hint": "小雨是DJ Rain Kuang",
        "likes_hint": 48,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160033/089f91bb53d4bc405c38d3e388c3b021/1040g00831lvjj2ia4s0g5n48rark1243pa026pg!nc_n_webp_mw_1",
        "body_excerpt": "听完开心一整天～🌞法式House自带多巴胺！🥰（搜索卡片公开字段）",
        "taste_tags": ["listening-space", "named-artist", "curator-voice", "atmosphere-title"],
        "source_url": "https://www.xiaohongshu.com/explore/68b84875000000001d00971e",
        "notes": "浏览器搜索「deep house 法国」公开卡片；48赞。",
    },
    {
        "id": "xhs-6aa30e6700000000110394f1",
        "domain": "music",
        "keyword": "deep house 法国",
        "note_id": "6aa30e6700000000110394f1",
        "title_observed": "巴黎9月也太热闹了吧😭 这阵容让我怎么选",
        "author_hint": "aK",
        "likes_hint": 48,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160033/45ea6464b3a0886d19a56bb5998074f0/1040g2sg324utnm6rj2705odkd8s40sp9bugsml0!nc_n_webp_mw_1",
        "body_excerpt": "巴黎9月也太热闹了吧😭 这阵容让我怎么选（搜索卡片公开字段）",
        "taste_tags": ["listening-space", "named-artist", "curator-voice", "atmosphere-title"],
        "source_url": "https://www.xiaohongshu.com/explore/6aa30e6700000000110394f1",
        "notes": "浏览器搜索「deep house 法国」公开卡片；48赞。",
    },
    {
        "id": "xhs-6a43a84d000000002200b061",
        "domain": "music",
        "keyword": "deep house 法国",
        "note_id": "6a43a84d000000002200b061",
        "title_observed": "水浪交融，正反相拥，轻盈的浪漫，深沉的悸动",
        "author_hint": "狮子尾",
        "likes_hint": 41,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160033/1d6490e8446ae0539a3221ccaf030544/1040g2sg3221o9g1qnkf05n727f6lvaorouoqi8g!nc_n_webp_mw_1",
        "body_excerpt": "水浪交融，正反相拥，轻盈的浪漫，深沉的悸动（搜索卡片公开字段）",
        "taste_tags": ["listening-space", "named-artist", "curator-voice", "atmosphere-title"],
        "source_url": "https://www.xiaohongshu.com/explore/6a43a84d000000002200b061",
        "notes": "浏览器搜索「deep house 法国」公开卡片；41赞。",
    },
    {
        "id": "xhs-6a03286f0000000008030562",
        "domain": "interior",
        "keyword": "折衷主义室内设计",
        "note_id": "6a03286f0000000008030562",
        "title_observed": "改了八九遍 就这样吧 没有风格的设计",
        "author_hint": "糯糯婉（装修版）",
        "likes_hint": 2828,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160031/c185f11e347fd2870206a8798b9f4d50/notes_pre_post/1040g3k83202ok8h32a605n22mnlhekmkikosqmg!nc_n_webp_mw_1",
        "body_excerpt": "改了八九遍 就这样吧 没有风格的设计（搜索卡片公开字段）",
        "taste_tags": ["style-named", "curator-voice", "honest-framing", "visual-board"],
        "source_url": "https://www.xiaohongshu.com/explore/6a03286f0000000008030562",
        "notes": "浏览器搜索「折衷主义室内设计」公开卡片；2828赞。",
    },
    {
        "id": "xhs-6a072dd600000000350281ad",
        "domain": "interior",
        "keyword": "折衷主义室内设计",
        "note_id": "6a072dd600000000350281ad",
        "title_observed": "审美累积｜自然折中主义",
        "author_hint": "Xiu Xiu美宅",
        "likes_hint": 771,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160031/7a05b8b7052aebd18d662ae45f16420c/notes_pre_post/1040g3k03206m2kub5e005q1ah1i391omdj0hua8!nc_n_webp_mw_1",
        "body_excerpt": "审美累积｜自然折中主义（搜索卡片公开字段）",
        "taste_tags": ["style-named", "curator-voice", "honest-framing", "visual-board"],
        "source_url": "https://www.xiaohongshu.com/explore/6a072dd600000000350281ad",
        "notes": "浏览器搜索「折衷主义室内设计」公开卡片；771赞。",
    },
    {
        "id": "xhs-6a41fd30000000000702ca19",
        "domain": "interior",
        "keyword": "折衷主义室内设计",
        "note_id": "6a41fd30000000000702ca19",
        "title_observed": "精装房里的“折衷主义”",
        "author_hint": "漂亮拖鞋",
        "likes_hint": 705,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160031/767f8d499b750c626e567279bd8fb391/spectrum/1040g34o32203ulj0ms1048ug9f7i6fpcukvh3kg!nc_n_webp_mw_1",
        "body_excerpt": "精装房里的“折衷主义”（搜索卡片公开字段）",
        "taste_tags": ["style-named", "curator-voice", "honest-framing", "visual-board"],
        "source_url": "https://www.xiaohongshu.com/explore/6a41fd30000000000702ca19",
        "notes": "浏览器搜索「折衷主义室内设计」公开卡片；705赞。",
    },
    {
        "id": "xhs-6a31f8ae0000000008025646",
        "domain": "interior",
        "keyword": "折衷主义室内设计",
        "note_id": "6a31f8ae0000000008025646",
        "title_observed": "自然折衷主义～",
        "author_hint": "小北",
        "likes_hint": 479,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160031/cb36628050b72554070c54c3730606a2/1040g2sg321gfqmuf7uk05nshkdugbt3lm6v5ce0!nc_n_webp_mw_1",
        "body_excerpt": "自然折衷主义～（搜索卡片公开字段）",
        "taste_tags": ["style-named", "curator-voice", "honest-framing", "visual-board"],
        "source_url": "https://www.xiaohongshu.com/explore/6a31f8ae0000000008025646",
        "notes": "浏览器搜索「折衷主义室内设计」公开卡片；479赞。",
    },
    {
        "id": "xhs-6968c0c0000000002200b328",
        "domain": "interior",
        "keyword": "折衷主义室内设计",
        "note_id": "6968c0c0000000002200b328",
        "title_observed": "美图分享",
        "author_hint": "木子",
        "likes_hint": 286,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160031/42685f41bc8b36aa0d1a860ef87a56ac/notes_pre_post/1040g3k031rbvn6g0ng1049m575kl2ucatg2atpo!nc_n_webp_mw_1",
        "body_excerpt": "美图分享（搜索卡片公开字段）",
        "taste_tags": ["style-named", "curator-voice", "honest-framing", "visual-board"],
        "source_url": "https://www.xiaohongshu.com/explore/6968c0c0000000002200b328",
        "notes": "浏览器搜索「折衷主义室内设计」公开卡片；286赞。",
    },
    {
        "id": "xhs-6968c0f6000000002202c7fb",
        "domain": "interior",
        "keyword": "折衷主义室内设计",
        "note_id": "6968c0f6000000002202c7fb",
        "title_observed": "折衷主义美学空间",
        "author_hint": "木子",
        "likes_hint": 270,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160031/b8b9749f31e50541ed80dd85db9fddf6/notes_pre_post/1040g3k831rbvpe297oa049m575kl2uca6rua2mg!nc_n_webp_mw_1",
        "body_excerpt": "折衷主义美学空间（搜索卡片公开字段）",
        "taste_tags": ["style-named", "curator-voice", "honest-framing", "visual-board"],
        "source_url": "https://www.xiaohongshu.com/explore/6968c0f6000000002202c7fb",
        "notes": "浏览器搜索「折衷主义室内设计」公开卡片；270赞。",
    },
    {
        "id": "xhs-6a4a1dda00000000110135fe",
        "domain": "interior",
        "keyword": "折衷主义室内设计",
        "note_id": "6a4a1dda00000000110135fe",
        "title_observed": "折衷主义艺术感之家，每一帧都尽显质感！",
        "author_hint": "San 0 叁零設计",
        "likes_hint": 254,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160031/d9acfd6454b6f99461304b7b2d1e2238/notes_pre_post/1040g3k83227qr7he6u1g5pa1mqbhgu2irmjjct0!nc_n_webp_mw_1",
        "body_excerpt": "折衷主义艺术感之家，每一帧都尽显质感！（搜索卡片公开字段）",
        "taste_tags": ["style-named", "curator-voice", "honest-framing", "visual-board"],
        "source_url": "https://www.xiaohongshu.com/explore/6a4a1dda00000000110135fe",
        "notes": "浏览器搜索「折衷主义室内设计」公开卡片；254赞。",
    },
    {
        "id": "xhs-6968b415000000000d0093e9",
        "domain": "interior",
        "keyword": "折衷主义室内设计",
        "note_id": "6968b415000000000d0093e9",
        "title_observed": "INS. 折衷主义 | 容乱的底气 14",
        "author_hint": "结庐Lab",
        "likes_hint": 223,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160031/82eaf9b2b076361f8d929ba5dfb9e37d/spectrum/1040g0k031rbtto8374a04a8ondph7mnevcr1ih0!nc_n_webp_mw_1",
        "body_excerpt": "INS. 折衷主义 | 容乱的底气 14（搜索卡片公开字段）",
        "taste_tags": ["style-named", "curator-voice", "honest-framing", "visual-board"],
        "source_url": "https://www.xiaohongshu.com/explore/6968b415000000000d0093e9",
        "notes": "浏览器搜索「折衷主义室内设计」公开卡片；223赞。",
    },
    {
        "id": "xhs-6a07f230000000000802563c",
        "domain": "cityscape",
        "keyword": "上海浦西内透",
        "note_id": "6a07f230000000000802563c",
        "title_observed": "每个来上海的朋友，都会被我带来这里！",
        "author_hint": "梵克Frankkie",
        "likes_hint": 5863,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160032/863d7d782bbf2128d0ceb8f1b5f9bc26/c/notes_pre_post/1040g3k03207e85mv628g5oqd5k163jrjngo6rq0!nc_n_webp_mw_1",
        "body_excerpt": "每个来上海的朋友，都会被我带来这里！（搜索卡片公开字段）",
        "taste_tags": ["china-place", "atmosphere-title", "provenance-stated", "low-sat"],
        "source_url": "https://www.xiaohongshu.com/explore/6a07f230000000000802563c",
        "notes": "浏览器搜索「上海浦西内透」公开卡片；5863赞。",
    },
    {
        "id": "xhs-6a72fbc8000000002403d9e7",
        "domain": "cityscape",
        "keyword": "上海浦西内透",
        "note_id": "6a72fbc8000000002403d9e7",
        "title_observed": "原来上海一半的美在🔷Blue Hour",
        "author_hint": "GX",
        "likes_hint": 2832,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160032/eed73b44569fb38e8650c5cdffee8666/notes_pre_post/1040g3k0323fvdk2e7a6049g8ufh3o1sud9ufl6g!nc_n_webp_mw_1",
        "body_excerpt": "原来上海一半的美在🔷Blue Hour（搜索卡片公开字段）",
        "taste_tags": ["china-place", "atmosphere-title", "provenance-stated", "low-sat"],
        "source_url": "https://www.xiaohongshu.com/explore/6a72fbc8000000002403d9e7",
        "notes": "浏览器搜索「上海浦西内透」公开卡片；2832赞。",
    },
    {
        "id": "xhs-6a8ecc880000000025010526",
        "domain": "cityscape",
        "keyword": "上海浦西内透",
        "note_id": "6a8ecc880000000025010526",
        "title_observed": "上海的密度已经大到高楼名字都写不下了",
        "author_hint": "RX-105柯西",
        "likes_hint": 1544,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160032/bfbddc018a6c9a1b5cdf94a1811e5f48/c/1040g2sg324b4ic5n7a6g5n91enr5m0qi8nb5r5o!nc_n_webp_mw_1",
        "body_excerpt": "上海的密度已经大到高楼名字都写不下了（搜索卡片公开字段）",
        "taste_tags": ["china-place", "atmosphere-title", "provenance-stated", "low-sat"],
        "source_url": "https://www.xiaohongshu.com/explore/6a8ecc880000000025010526",
        "notes": "浏览器搜索「上海浦西内透」公开卡片；1544赞。",
    },
    {
        "id": "xhs-6a672a07000000000f031c0e",
        "domain": "cityscape",
        "keyword": "上海浦西内透",
        "note_id": "6a672a07000000000f031c0e",
        "title_observed": "凌晨4点|我镜头里的乍浦路桥",
        "author_hint": "Ar_ww",
        "likes_hint": 863,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160032/9f39d205640821d58dd44990ebda53e8/notes_pre_post/1040g3k03234dop9d6u40493bijsr2362stm0hco!nc_n_webp_mw_1",
        "body_excerpt": "凌晨4点|我镜头里的乍浦路桥（搜索卡片公开字段）",
        "taste_tags": ["china-place", "atmosphere-title", "provenance-stated", "low-sat"],
        "source_url": "https://www.xiaohongshu.com/explore/6a672a07000000000f031c0e",
        "notes": "浏览器搜索「上海浦西内透」公开卡片；863赞。",
    },
    {
        "id": "xhs-6a6776bb0000000006012cf6",
        "domain": "cityscape",
        "keyword": "上海浦西内透",
        "note_id": "6a6776bb0000000006012cf6",
        "title_observed": "▪️上海气质 不可复制",
        "author_hint": "拆腻思空腹",
        "likes_hint": 710,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160032/02688a061c6ef915d08273b348ee1d49/note_pre_post_uhdr/1040g3r83234neods7a705o9f0pf0kcauuerlm6g!nc_n_webp_mw_1",
        "body_excerpt": "▪️上海气质 不可复制（搜索卡片公开字段）",
        "taste_tags": ["china-place", "atmosphere-title", "provenance-stated", "low-sat"],
        "source_url": "https://www.xiaohongshu.com/explore/6a6776bb0000000006012cf6",
        "notes": "浏览器搜索「上海浦西内透」公开卡片；710赞。",
    },
    {
        "id": "xhs-6a8337570000000008011f70",
        "domain": "cityscape",
        "keyword": "上海浦西内透",
        "note_id": "6a8337570000000008011f70",
        "title_observed": "我今天拍的外滩，跟你们交换一下",
        "author_hint": "HxMooh",
        "likes_hint": 508,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160032/fa4fb08f8dde6918a5c0fa4f19f9b54b/note_pre_post_uhdr/1040g3r0323vqktq2go005noss7tg87h3eu3mg0g!nc_n_webp_mw_1",
        "body_excerpt": "我今天拍的外滩，跟你们交换一下（搜索卡片公开字段）",
        "taste_tags": ["china-place", "atmosphere-title", "provenance-stated", "low-sat"],
        "source_url": "https://www.xiaohongshu.com/explore/6a8337570000000008011f70",
        "notes": "浏览器搜索「上海浦西内透」公开卡片；508赞。",
    },
    {
        "id": "xhs-6a8bf7ec000000001602227a",
        "domain": "cityscape",
        "keyword": "上海浦西内透",
        "note_id": "6a8bf7ec000000001602227a",
        "title_observed": "上海·北外滩江景，2km不用挤，傍晚很好拍🌆",
        "author_hint": "半片馨光",
        "likes_hint": 301,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160032/1c1a6b457431db7101a84e68b0bbe484/note_pre_post_uhdr/1040g3r83248c64rknu704a5t3utpei05j3j3op0!nc_n_webp_mw_1",
        "body_excerpt": "上海·北外滩江景，2km不用挤，傍晚很好拍🌆（搜索卡片公开字段）",
        "taste_tags": ["china-place", "atmosphere-title", "provenance-stated", "low-sat"],
        "source_url": "https://www.xiaohongshu.com/explore/6a8bf7ec000000001602227a",
        "notes": "浏览器搜索「上海浦西内透」公开卡片；301赞。",
    },
    {
        "id": "xhs-69b0f477000000001b0170a4",
        "domain": "cityscape",
        "keyword": "上海浦西内透",
        "note_id": "69b0f477000000001b0170a4",
        "title_observed": "在静安寺旁，我拍到了上海钻石般的夜景",
        "author_hint": "RX-105柯西",
        "likes_hint": 137,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160032/005754358b20f79676ceaba86a598245/1040g2sg31tiftk5bm88g5n91enr5m0qi33o0deg!nc_n_webp_mw_1",
        "body_excerpt": "在静安寺旁，我拍到了上海钻石般的夜景（搜索卡片公开字段）",
        "taste_tags": ["china-place", "atmosphere-title", "provenance-stated", "low-sat"],
        "source_url": "https://www.xiaohongshu.com/explore/69b0f477000000001b0170a4",
        "notes": "浏览器搜索「上海浦西内透」公开卡片；137赞。",
    },
    {
        "id": "xhs-6a7ff9c6000000003300a9fb",
        "domain": "meta",
        "keyword": "审美积累",
        "note_id": "6a7ff9c6000000003300a9fb",
        "title_observed": "“在等一个喜欢我照片的人”",
        "author_hint": "chenchenchenrr",
        "likes_hint": 205000,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160035/a1206c681308f017d1b2a0331dcb4bc1/1040g2sg323sl7u0b0ae04ach5spao1u86u4hq20!nc_n_webp_mw_1",
        "body_excerpt": "“在等一个喜欢我照片的人”（搜索卡片公开字段）",
        "taste_tags": ["visual-board", "collage", "atmosphere-title", "low-sat", "series-day"],
        "source_url": "https://www.xiaohongshu.com/explore/6a7ff9c6000000003300a9fb",
        "notes": "浏览器搜索「审美积累」公开卡片；205000赞。",
    },
    {
        "id": "xhs-6a32b9f0000000000e038400",
        "domain": "meta",
        "keyword": "审美积累",
        "note_id": "6a32b9f0000000000e038400",
        "title_observed": "GUWEIZ",
        "author_hint": "",
        "likes_hint": 85000,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160035/0c3b96e30168f3bcdd6ea8b8f4b40063/oss-sg/notes_pre_post/1040g3mo321h71r2l7k2g5ogbhgmk0guskf65288!nc_n_webp_mw_1",
        "body_excerpt": "GUWEIZ（搜索卡片公开字段）",
        "taste_tags": ["visual-board", "collage", "atmosphere-title", "low-sat", "series-day"],
        "source_url": "https://www.xiaohongshu.com/explore/6a32b9f0000000000e038400",
        "notes": "浏览器搜索「审美积累」公开卡片；85000赞。",
    },
    {
        "id": "xhs-69f3255c0000000023014227",
        "domain": "meta",
        "keyword": "审美积累",
        "note_id": "69f3255c0000000023014227",
        "title_observed": "Mixed Media Assemblage",
        "author_hint": "Flora",
        "likes_hint": 23000,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160035/bf8fd9edb4f607a0f134f4fec055d154/spectrum/1040g0k031vj41r37jm0g5n80u3bk52rdsdc2td8!nc_n_webp_mw_1",
        "body_excerpt": "Mixed Media Assemblage（搜索卡片公开字段）",
        "taste_tags": ["visual-board", "collage", "atmosphere-title", "low-sat", "series-day"],
        "source_url": "https://www.xiaohongshu.com/explore/69f3255c0000000023014227",
        "notes": "浏览器搜索「审美积累」公开卡片；23000赞。",
    },
    {
        "id": "xhs-69e63171000000001a02a829",
        "domain": "meta",
        "keyword": "审美积累",
        "note_id": "69e63171000000001a02a829",
        "title_observed": "：QQ日志里的唯美女头",
        "author_hint": "泡泡Oo",
        "likes_hint": 16000,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160035/aebe850acd1f521c1196abcde8c0f0d5/notes_pre_post/1040g3k831v6fhueviqa05o8sgsmg8hqsi28g480!nc_n_webp_mw_1",
        "body_excerpt": "：QQ日志里的唯美女头（搜索卡片公开字段）",
        "taste_tags": ["visual-board", "collage", "atmosphere-title", "low-sat", "series-day"],
        "source_url": "https://www.xiaohongshu.com/explore/69e63171000000001a02a829",
        "notes": "浏览器搜索「审美积累」公开卡片；16000赞。",
    },
    {
        "id": "xhs-6a3cc3e40000000008024e29",
        "domain": "interior",
        "keyword": "包豪斯室内美学",
        "note_id": "6a3cc3e40000000008024e29",
        "title_observed": "我的复古未来主义之家",
        "author_hint": "茶武",
        "likes_hint": 10000,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160034/be8ad2aaa25fdb231ac57e8537567e3f/note_pre_post_uhdr/1040g3r0321r108h3na7048h25oa32t6n9562kkg!nc_n_webp_mw_1",
        "body_excerpt": "我的复古未来主义之家（搜索卡片公开字段）",
        "taste_tags": ["style-named", "curator-voice", "honest-framing", "visual-board"],
        "source_url": "https://www.xiaohongshu.com/explore/6a3cc3e40000000008024e29",
        "notes": "浏览器搜索「包豪斯室内美学」公开卡片；10000赞。",
    },
    {
        "id": "xhs-6a429709000000001100730d",
        "domain": "meta",
        "keyword": "审美积累",
        "note_id": "6a429709000000001100730d",
        "title_observed": "y̶o̶u̶r̶ e̶y̶e̶s̶…（10/100）",
        "author_hint": "DVDiiian",
        "likes_hint": 9113,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160035/9a94f5cedf0fc325327650435546ef0d/1040g0083220n0mbm6s005ppk4jln34lcdjovn3o!nc_n_webp_mw_1",
        "body_excerpt": "y̶o̶u̶r̶ e̶y̶e̶s̶…（10/100）（搜索卡片公开字段）",
        "taste_tags": ["visual-board", "collage", "atmosphere-title", "low-sat", "series-day"],
        "source_url": "https://www.xiaohongshu.com/explore/6a429709000000001100730d",
        "notes": "浏览器搜索「审美积累」公开卡片；9113赞。",
    },
    {
        "id": "xhs-6a09677a0000000007028e49",
        "domain": "meta",
        "keyword": "审美积累",
        "note_id": "6a09677a0000000007028e49",
        "title_observed": "13张",
        "author_hint": "只对我凶的猫",
        "likes_hint": 6177,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160035/e4c85f5470d1fb85958d6847582b3d85/notes_pre_post/1040g3k83208s3pa9me005o9ba44gaq16oq8hvb0!nc_n_webp_mw_1",
        "body_excerpt": "13张（搜索卡片公开字段）",
        "taste_tags": ["visual-board", "collage", "atmosphere-title", "low-sat", "series-day"],
        "source_url": "https://www.xiaohongshu.com/explore/6a09677a0000000007028e49",
        "notes": "浏览器搜索「审美积累」公开卡片；6177赞。",
    },
    {
        "id": "xhs-6a044229000000003601c6b7",
        "domain": "meta",
        "keyword": "审美积累",
        "note_id": "6a044229000000003601c6b7",
        "title_observed": "审美积累",
        "author_hint": "恋殓",
        "likes_hint": 5982,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160035/90bc1e51756045246d04b7dff5e231a0/1040g2sg3203ra7mp3qjg5qelpl2spjtpav397n0!nc_n_webp_mw_1",
        "body_excerpt": "审美积累（搜索卡片公开字段）",
        "taste_tags": ["visual-board", "collage", "atmosphere-title", "low-sat", "series-day"],
        "source_url": "https://www.xiaohongshu.com/explore/6a044229000000003601c6b7",
        "notes": "浏览器搜索「审美积累」公开卡片；5982赞。",
    },
    {
        "id": "xhs-6a7aaf5d0000000024025030",
        "domain": "meta",
        "keyword": "审美积累",
        "note_id": "6a7aaf5d0000000024025030",
        "title_observed": "无意义の审美积累",
        "author_hint": "暨雨",
        "likes_hint": 5449,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160035/12d0128970d6d80150dd7cc80bae90fc/notes_pre_post/1040g3k8323ng4hgp0m005nvlkgu0bsmet3iijno!nc_n_webp_mw_1",
        "body_excerpt": "无意义の审美积累（搜索卡片公开字段）",
        "taste_tags": ["visual-board", "collage", "atmosphere-title", "low-sat", "series-day"],
        "source_url": "https://www.xiaohongshu.com/explore/6a7aaf5d0000000024025030",
        "notes": "浏览器搜索「审美积累」公开卡片；5449赞。",
    },
    {
        "id": "xhs-6a253c240000000008001096",
        "domain": "music",
        "keyword": "listening bar 爵士",
        "note_id": "6a253c240000000008001096",
        "title_observed": "足够勇敢 就能在香港最老的jazz bar里唱歌",
        "author_hint": "Stelbell🦁",
        "likes_hint": 3412,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160035/8e0a265106741cfad4416d839ba06b68/1040g008321413b687a0048c4kiucf3q5tttafg0!nc_n_webp_mw_1",
        "body_excerpt": "足够勇敢 就能在香港最老的jazz bar里唱歌（搜索卡片公开字段）",
        "taste_tags": ["listening-space", "named-artist", "curator-voice", "atmosphere-title"],
        "source_url": "https://www.xiaohongshu.com/explore/6a253c240000000008001096",
        "notes": "浏览器搜索「listening bar 爵士」公开卡片；3412赞。",
    },
    {
        "id": "xhs-6a574a2600000000210085ad",
        "domain": "interior",
        "keyword": "包豪斯室内美学",
        "note_id": "6a574a2600000000210085ad",
        "title_observed": "没想到吧，这是30岁小朋友的家🟠🔵🟡⚫️",
        "author_hint": "一支白菜",
        "likes_hint": 3034,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160034/8d64997a6646cc6816df5191561fc749/notes_pre_post/1040g3k8322ku18oi7as05qecgpmsmoa4r5p79eg!nc_n_webp_mw_1",
        "body_excerpt": "没想到吧，这是30岁小朋友的家🟠🔵🟡⚫️（搜索卡片公开字段）",
        "taste_tags": ["style-named", "curator-voice", "honest-framing", "visual-board"],
        "source_url": "https://www.xiaohongshu.com/explore/6a574a2600000000210085ad",
        "notes": "浏览器搜索「包豪斯室内美学」公开卡片；3034赞。",
    },
    {
        "id": "xhs-6a54ed5a000000001702e4d4",
        "domain": "cityscape",
        "keyword": "重庆夜景天际线",
        "note_id": "6a54ed5a000000001702e4d4",
        "title_observed": "重庆！！真有种不在国内的vibe。。。",
        "author_hint": "泡芙味的女孩子",
        "likes_hint": 2471,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160036/83984c61be72355e0878ec3e5d6a9e04/notes_uhdr/1040g3qo322ik5s45ne7048fvc0c322v3362f9gg!nc_n_webp_mw_1",
        "body_excerpt": "重庆！！真有种不在国内的vibe。。。（搜索卡片公开字段）",
        "taste_tags": ["china-place", "atmosphere-title", "provenance-stated", "low-sat"],
        "source_url": "https://www.xiaohongshu.com/explore/6a54ed5a000000001702e4d4",
        "notes": "浏览器搜索「重庆夜景天际线」公开卡片；2471赞。",
    },
    {
        "id": "xhs-6926b60d000000001f00cda4",
        "domain": "interior",
        "keyword": "包豪斯室内美学",
        "note_id": "6926b60d000000001f00cda4",
        "title_observed": "🔴🟡🔵包豪斯装修风格！",
        "author_hint": "汉堡大王的家装日记",
        "likes_hint": 2184,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160034/66dfb4587e4f9825409babbf95d61ea2/spectrum/1040g34o31pbfn3ubi40g5o0bvu50bppnung68rg!nc_n_webp_mw_1",
        "body_excerpt": "🔴🟡🔵包豪斯装修风格！（搜索卡片公开字段）",
        "taste_tags": ["style-named", "curator-voice", "honest-framing", "visual-board"],
        "source_url": "https://www.xiaohongshu.com/explore/6926b60d000000001f00cda4",
        "notes": "浏览器搜索「包豪斯室内美学」公开卡片；2184赞。",
    },
    {
        "id": "xhs-6a759f20000000003302d16d",
        "domain": "interior",
        "keyword": "包豪斯室内美学",
        "note_id": "6a759f20000000003302d16d",
        "title_observed": "抱歉，我家真的不接受剧组上门拍戏😂",
        "author_hint": "一支白菜",
        "likes_hint": 2032,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160034/b74410f2578129aa07fecbe0ddc44485/1040g2sg323iht8q47ueg5qecgpmsmoa4j49s30o!nc_n_webp_mw_1",
        "body_excerpt": "抱歉，我家真的不接受剧组上门拍戏😂（搜索卡片公开字段）",
        "taste_tags": ["style-named", "curator-voice", "honest-framing", "visual-board"],
        "source_url": "https://www.xiaohongshu.com/explore/6a759f20000000003302d16d",
        "notes": "浏览器搜索「包豪斯室内美学」公开卡片；2032赞。",
    },
    {
        "id": "xhs-6a32a741000000000f01fdce",
        "domain": "cityscape",
        "keyword": "重庆夜景天际线",
        "note_id": "6a32a741000000000f01fdce",
        "title_observed": "重庆洪崖洞3个机位📸 +路线攻略",
        "author_hint": "绮景是氟西汀",
        "likes_hint": 1913,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160036/e2c179f01e95a5569c45155f162441b1/note_pre_post_uhdr/1040g3r0321h52in370005qaa8pgtud4kej8217o!nc_n_webp_mw_1",
        "body_excerpt": "重庆洪崖洞3个机位📸 +路线攻略（搜索卡片公开字段）",
        "taste_tags": ["china-place", "atmosphere-title", "provenance-stated", "low-sat"],
        "source_url": "https://www.xiaohongshu.com/explore/6a32a741000000000f01fdce",
        "notes": "浏览器搜索「重庆夜景天际线」公开卡片；1913赞。",
    },
    {
        "id": "xhs-6a0d8b05000000003700c197",
        "domain": "cityscape",
        "keyword": "重庆夜景天际线",
        "note_id": "6a0d8b05000000003700c197",
        "title_observed": "谁懂啊！重庆的夜景🌃也太美了吧！",
        "author_hint": "航拍摄影家Shawn Wang",
        "likes_hint": 1865,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160036/95f99ae8b9a077c5d8de6a8435a6c609/1040g2sg320cte23f5m005n959pk4243tfqesgno!nc_n_webp_mw_1",
        "body_excerpt": "谁懂啊！重庆的夜景🌃也太美了吧！（搜索卡片公开字段）",
        "taste_tags": ["china-place", "atmosphere-title", "provenance-stated", "low-sat"],
        "source_url": "https://www.xiaohongshu.com/explore/6a0d8b05000000003700c197",
        "notes": "浏览器搜索「重庆夜景天际线」公开卡片；1865赞。",
    },
    {
        "id": "xhs-6960cb5f000000000a029ca0",
        "domain": "music",
        "keyword": "listening bar 爵士",
        "note_id": "6960cb5f000000000a029ca0",
        "title_observed": "我们为什么要在北京开一家 listening bar",
        "author_hint": "黑月BlackMoon",
        "likes_hint": 1687,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160035/6354a2ffb5271fab6b39ee869fe9ecf7/notes_pre_post/1040g3k831r46vrof72005p6psagg9i45lsfo7ko!nc_n_webp_mw_1",
        "body_excerpt": "我们为什么要在北京开一家 listening bar（搜索卡片公开字段）",
        "taste_tags": ["listening-space", "named-artist", "curator-voice", "atmosphere-title"],
        "source_url": "https://www.xiaohongshu.com/explore/6960cb5f000000000a029ca0",
        "notes": "浏览器搜索「listening bar 爵士」公开卡片；1687赞。",
    },
    {
        "id": "xhs-690736cf00000000070319b7",
        "domain": "cityscape",
        "keyword": "重庆夜景天际线",
        "note_id": "690736cf00000000070319b7",
        "title_observed": "拍到这组夜景，重庆没有白来",
        "author_hint": "明天放假啦",
        "likes_hint": 1368,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160036/741e292aa49e1a5b5796d574276b187c/notes_pre_post/1040g3k831ocn5k6jl0d05nmgdqm08n48v5t33s8!nc_n_webp_mw_1",
        "body_excerpt": "拍到这组夜景，重庆没有白来（搜索卡片公开字段）",
        "taste_tags": ["china-place", "atmosphere-title", "provenance-stated", "low-sat"],
        "source_url": "https://www.xiaohongshu.com/explore/690736cf00000000070319b7",
        "notes": "浏览器搜索「重庆夜景天际线」公开卡片；1368赞。",
    },
    {
        "id": "xhs-6692366b000000000a027a7c",
        "domain": "music",
        "keyword": "listening bar 爵士",
        "note_id": "6692366b000000000a027a7c",
        "title_observed": "🇩🇪柏林另一家有灵魂的listening bar",
        "author_hint": "Ranny冉妮",
        "likes_hint": 328,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160035/9c2a806e21d5239dc85148af8a89a926/1040g0083156fc61p0u0049ghsvou43k42c217a8!nc_n_webp_mw_1",
        "body_excerpt": "🇩🇪柏林另一家有灵魂的listening bar（搜索卡片公开字段）",
        "taste_tags": ["listening-space", "named-artist", "curator-voice", "atmosphere-title"],
        "source_url": "https://www.xiaohongshu.com/explore/6692366b000000000a027a7c",
        "notes": "浏览器搜索「listening bar 爵士」公开卡片；328赞。",
    },
    {
        "id": "xhs-6864e7ec000000002001a484",
        "domain": "music",
        "keyword": "listening bar 爵士",
        "note_id": "6864e7ec000000002001a484",
        "title_observed": "神户旅行🎵花一晚上在这家听爵士绝对很值得",
        "author_hint": "💝燕老板💖",
        "likes_hint": 249,
        "cover_url": "https://sns-webpic-qc.xhscdn.com/202609160035/bf9b42043534029880038e29a51f2f24/notes_pre_post/1040g3k831je5m1fj30004a4n4kb4tm9te4mn8jo!nc_n_webp_mw_1",
        "body_excerpt": "神户旅行🎵花一晚上在这家听爵士绝对很值得（搜索卡片公开字段）",
        "taste_tags": ["listening-space", "named-artist", "curator-voice", "atmosphere-title"],
        "source_url": "https://www.xiaohongshu.com/explore/6864e7ec000000002001a484",
        "notes": "浏览器搜索「listening bar 爵士」公开卡片；249赞。",
    },

]


def upsert_materials(db: Session) -> int:
    """写入真实素材，并清除旧假条目 / polar / 负向 / 低互动素材。"""
    from app.config import get_settings

    settings = get_settings()
    now = datetime.utcnow()
    allowed: list[dict] = []
    for item in MATERIALS:
        # 先算质量分再过门槛
        q = _q(
            item.get("likes_hint"),
            item["title_observed"],
            bonus=item.get("quality_bonus", 0),
        )
        reason = material_reject_reason(
            domain=item["domain"],
            title=item["title_observed"],
            body_excerpt=item.get("body_excerpt"),
            keyword=item.get("keyword"),
            notes=item.get("notes"),
            likes_hint=item.get("likes_hint"),
            quality_score=q,
            min_likes=settings.material_min_likes,
            min_quality=settings.material_min_quality,
        )
        if reason:
            continue
        if not item.get("cover_url"):
            continue
        item = {**item, "_quality": q}
        allowed.append(item)

    keep_ids = {item["id"] for item in allowed}

    for row in db.scalars(select(ReferenceMaterial)).all():
        if row.id not in keep_ids:
            db.delete(row)

    for item in allowed:
        row = db.get(ReferenceMaterial, item["id"])
        if row is None:
            row = ReferenceMaterial(id=item["id"])
            db.add(row)
        row.domain = item["domain"]
        row.keyword = item["keyword"]
        row.note_id = item.get("note_id")
        row.title_observed = item["title_observed"]
        row.author_hint = item.get("author_hint")
        row.likes_hint = item.get("likes_hint")
        row.collects_hint = item.get("collects_hint")
        row.comments_hint = item.get("comments_hint")
        row.cover_url = item.get("cover_url")
        images = item.get("images") or ([item["cover_url"]] if item.get("cover_url") else [])
        row.images_json = json.dumps(images, ensure_ascii=False) if images else None
        row.body_excerpt = item.get("body_excerpt")
        row.structure_notes = item.get("notes") or (
            f"真实笔记 {item.get('note_id')}；关键词「{item['keyword']}」"
        )
        row.taste_tags_json = json.dumps(item["taste_tags"], ensure_ascii=False)
        row.quality_score = item["_quality"]
        row.source_url = item.get("source_url")
        row.source_site = item.get("source_site") or "xhs"
        row.theme_key = item.get("theme_key") or f"{item['domain']}:{item['keyword']}"
        row.license_ok = False
        row.notes = item.get("notes")
        row.collected_at = now
    db.commit()
    return len(allowed)
