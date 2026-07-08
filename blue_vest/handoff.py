"""Caregiver handoff brief generator for volunteer shift changes."""

from __future__ import annotations

from blue_vest.constants import DISCLAIMER_SHORT


def generate_handoff_brief(
    stage: str,
    recent_changes: str,
    communication_preference: str = "",
    follow_up_items: str = "",
) -> str:
    """Generate a markdown handoff brief for volunteer shift changes.

    Uses user-provided demo/synthetic info only. Not a medical record.
    """
    stage = stage.strip() or "未填写"
    recent = recent_changes.strip() or "无特别记录"
    pref = communication_preference.strip() or "未记录"
    follow = follow_up_items.strip() or "无"

    lines = [
        "## 蓝马甲陪护交接摘要",
        "",
        "说明：仅供志愿者同伴支持场景的信息整理，非病历、非诊疗建议。",
        "",
        "### 当前阶段",
        stage,
        "",
        "### 近期变化（家属/陪护者自报）",
        recent,
        "",
        "### 沟通偏好",
        pref,
        "",
        "### 待跟进事项",
        follow,
        "",
        "### 给下一班志愿者的提示",
        "- 先陪伴，少给结论；用药与治疗问题引导问主治医生",
        "- 若出现自伤/自杀表述，立即协助联系 120 或心理热线 400-161-9995",
        "- 情绪波谷时可使用 `generate_peer_response_card` 生成接话参考",
        "",
        DISCLAIMER_SHORT,
    ]
    return "\n".join(lines)
