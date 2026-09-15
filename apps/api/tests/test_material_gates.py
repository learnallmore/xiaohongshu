"""素材入库门禁单测。"""

from app.services.material_gates import material_reject_reason


def test_reject_polar_domain():
    assert material_reject_reason(
        domain="polar",
        title="挪威极光好看",
    )


def test_reject_antarctica_topic():
    assert material_reject_reason(
        domain="cityscape",
        title="南极冰原好看",
    )


def test_reject_negative_emotion():
    assert material_reject_reason(
        domain="meta",
        title="最诡异的10段画面，至今无人能解释",
    )


def test_allow_positive_or_flat():
    assert (
        material_reject_reason(
            domain="interior",
            title="韩系包豪斯",
            body_excerpt="材质和比例都克制。",
            keyword="包豪斯室内美学",
        )
        is None
    )
