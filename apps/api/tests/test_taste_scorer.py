"""taste_scorer + voice_filter：负例/元叙事必须未过线；正向短帖可过。"""

from __future__ import annotations

from datetime import date

from app.models import CandidatePost, PostImage, ReferenceMaterial
from app.services.taste_scorer import domain_benchmark, score_candidate
from app.services.voice_filter import scan_voice


def _mat(db, **kw):
    row = ReferenceMaterial(
        id=kw["id"],
        domain=kw["domain"],
        keyword=kw.get("keyword", "t"),
        note_id=kw.get("note_id", kw["id"]),
        title_observed=kw["title"],
        author_hint="tester",
        likes_hint=kw.get("likes", 5000),
        structure_notes="real",
        taste_tags_json='["provenance-stated","china-place","atmosphere-title"]',
        quality_score=kw.get("quality", 88),
        source_url=f"https://www.xiaohongshu.com/explore/{kw.get('note_id', kw['id'])}",
        license_ok=False,
        body_excerpt=kw.get("excerpt", "上海 天际线 低饱和"),
    )
    db.add(row)
    return row


def _imgs(post_id: str, n: int = 3) -> list[PostImage]:
    return [
        PostImage(
            id=f"{post_id}-i{i}",
            post_id=post_id,
            sort_order=i,
            url=f"http://x/{i}",
            width=1,
            height=1,
            source=f"Unsplash/demo-{i}",
            license="Unsplash License",
        )
        for i in range(n)
    ]


def test_negative_clickbait_fails(db_session):
    db = db_session
    _mat(db, id="m1", domain="cityscape", title="深圳天际线", likes=8000, quality=90)
    _mat(db, id="m2", domain="cityscape", title="杭州钱塘江", likes=3000, quality=84)
    _mat(db, id="m3", domain="cityscape", title="陆家嘴雨后", likes=2000, quality=82)
    db.commit()

    post = CandidatePost(
        id="neg1",
        date_batch=date.today(),
        domain="cityscape",
        status="pending",
        title="必看！绝美夜景封神机位速看",
        body="氛围感拉满高级感满满，必打卡攻略。",
        tags_json='["夜景"]',
        niche_score=10,
    )
    post.images = [
        PostImage(
            id="ni1",
            post_id="neg1",
            sort_order=0,
            url="http://x",
            width=1,
            height=1,
            source="",
            license="",
        )
    ]
    db.add(post)
    db.commit()

    r = score_candidate(db, post)
    assert r.passed is False
    assert r.score < r.benchmark
    assert r.features.get("fail_reasons")


def test_benchmark_uses_p75(db_session):
    db = db_session
    for i, q in enumerate([70, 80, 90, 92]):
        _mat(db, id=f"b{i}", domain="interior", title=f"包豪斯{i}", quality=q, likes=1000 + i)
    db.commit()
    b = domain_benchmark(db, "interior")
    assert b >= 85
    assert b >= 90


def test_voice_rejects_meta_and_quotes():
    bad = scan_voice(
        "标题",
        "素材库里「deep house」那批帖只学结构，授权 Unsplash License。",
    )
    assert bad.passed is False
    assert any("元叙事" in h or "说明书" in h or "直角" in h for h in bad.hits)


def test_voice_accepts_plain_note():
    ok = scan_voice(
        "浦西蓝调，楼里还亮着灯",
        "加班走到黄浦江边那段浦西。本地人说这叫内透。",
    )
    assert ok.passed is True


def test_meta_narrative_candidate_fails_taste(db_session):
    db = db_session
    _mat(db, id="mm1", domain="music", title="listening bar", likes=2000, quality=90)
    _mat(db, id="mm2", domain="music", title="French house", likes=1500, quality=88)
    _mat(db, id="mm3", domain="music", title="deep house", likes=1200, quality=86)
    db.commit()

    post = CandidatePost(
        id="meta-bad",
        date_batch=date.today(),
        domain="music",
        status="pending",
        title="French House 慢热碟",
        body="素材库里那批帖只学结构，不搬别人封面。授权 Unsplash License。",
        tags_json='["电子","listening bar","House"]',
        niche_score=80,
    )
    post.images = _imgs("meta-bad")
    db.add(post)
    db.commit()

    r = score_candidate(db, post)
    assert r.passed is False
    assert r.features.get("voice_pass") is False


def test_good_city_seed_style_can_pass(db_session):
    db = db_session
    for i in range(4):
        _mat(
            db,
            id=f"gc{i}",
            domain="cityscape",
            title="上海浦西内透蓝调",
            likes=5000 - i * 100,
            quality=90 - i,
            excerpt="上海 浦西 内透 蓝调",
        )
    db.commit()

    post = CandidatePost(
        id="good-city",
        date_batch=date.today(),
        domain="cityscape",
        status="pending",
        title="浦西蓝调，楼里还亮着灯",
        body=(
            "加班走到黄浦江边那段浦西。"
            "玻璃幕墙里零散的办公灯还亮着，楼体本身反而成了剪影。"
            "本地人说这叫内透。"
            "蓝调那十几分钟最干净，灯全开之后信息量就太大了。"
        ),
        tags_json='["上海","浦西","内透","蓝调","城市天际线"]',
        niche_score=82,
    )
    post.images = _imgs("good-city")
    db.add(post)
    db.commit()

    r = score_candidate(db, post)
    assert r.features.get("voice_pass") is True
    assert r.passed is True
    assert r.score >= r.benchmark
