"""Rule-based moment classification from caregiver/volunteer chat text."""

from __future__ import annotations

import re
from dataclasses import dataclass

from blue_vest.constants import MOMENT_LABELS


@dataclass
class ClassificationResult:
    moment_type: str
    label: str
    confidence: float
    matched_signals: list[str]


_RULES: list[tuple[str, list[str], float]] = [
    (
        "hospice_nav",
        [
            "临终关怀",
            "安宁疗护",
            "安宁病房",
            " hospice",
            "临终",
            "沈阳",
            "病房",
            "安宁云护",
            "姑息",
        ],
        0.85,
    ),
    (
        "med_self_doubt",
        [
            "抗抑郁",
            "抑郁药",
            "说明书",
            "维持剂量",
            "药量",
            "剂量",
            "精神科",
            "安眠药",
        ],
        0.82,
    ),
    (
        "misinfo_concern",
        [
            "乔布斯",
            "于娟",
            "芋头",
            "节食",
            "偏方",
            "江湖",
            "后悔治疗",
            "不吃",
            "饿死肿瘤",
            "辟谷",
        ],
        0.84,
    ),
    (
        "comparison_anxiety",
        [
            "CR",
            "怎么做到",
            "别人",
            "羡慕",
            "自责",
            "同样",
            "人家",
            "差距",
            "转阴",
            "缓解",
        ],
        0.8,
    ),
    (
        "existential",
        [
            "死亡",
            "舍不得",
            "痛不欲生",
            "告别",
            "活着才有希望",
            "为什么是我",
            "怨",
            "老婆孩子",
            "家人",
            "活下去",
        ],
        0.83,
    ),
    (
        "caregiver_burnout",
        [
            "天天哭",
            "崩溃",
            "奔溃",
            "灾难化",
            "离不开",
            "支楞",
            "倒下",
            "化疗",
            "心慌",
            "压力太大",
            "抑郁",
            "扛不住",
        ],
        0.86,
    ),
]


def _normalize(text: str) -> str:
    return text.strip().lower()


def classify_moment(text: str) -> ClassificationResult:
    normalized = _normalize(text)
    if not normalized:
        return ClassificationResult(
            moment_type="general_support",
            label=MOMENT_LABELS["general_support"],
            confidence=0.5,
            matched_signals=[],
        )

    best_type = "general_support"
    best_score = 0.0
    best_signals: list[str] = []
    base_confidence = 0.55

    for moment_type, keywords, rule_confidence in _RULES:
        matched = [kw for kw in keywords if kw.lower() in normalized or kw in text]
        if not matched:
            continue
        score = len(matched) * rule_confidence
        if score > best_score:
            best_score = score
            best_type = moment_type
            best_signals = matched
            base_confidence = min(0.95, rule_confidence + 0.05 * (len(matched) - 1))

    if best_type == "general_support":
        # Soft signals for general emotional distress
        soft = ["难受", "害怕", "焦虑", "无助", "不知道怎么办", "谢谢", "支持"]
        soft_matched = [s for s in soft if s in text]
        if soft_matched:
            best_signals = soft_matched
            base_confidence = 0.6

    return ClassificationResult(
        moment_type=best_type,
        label=MOMENT_LABELS[best_type],
        confidence=round(base_confidence, 2),
        matched_signals=best_signals,
    )


def format_classification(result: ClassificationResult) -> str:
    signals = "、".join(result.matched_signals) if result.matched_signals else "未匹配到强特征词"
    return (
        f"情境类型：{result.label} ({result.moment_type})\n"
        f"置信度（规则估计）：{result.confidence}\n"
        f"匹配信号：{signals}\n"
        f"说明：此为文本情境标签，非临床诊断。"
    )
