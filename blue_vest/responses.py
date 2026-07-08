"""Peer-response templates and next-step suggestions."""

from __future__ import annotations

from blue_vest.constants import DISCLAIMER_SHORT

ResponseBundle = dict[str, object]


def _bundle(
    moment_type: str,
    empathy: list[str],
    micro_action: str,
    volunteer_tip: str,
    extra: str = "",
) -> ResponseBundle:
    return {
        "moment_type": moment_type,
        "empathy_responses": empathy,
        "micro_action": micro_action,
        "volunteer_tip": volunteer_tip,
        "extra": extra,
    }


TEMPLATES: dict[str, ResponseBundle] = {
    "hospice_nav": _bundle(
        "hospice_nav",
        [
            "查临终关怀病房这件事本身就很耗心力，你愿意提前了解，是在为家人多准备一点安心。",
            "很多家属都会卡在「不知道问谁、怕信息不靠谱」——这种慌是正常的，不是你一个人这样。",
            "可以先不急着定「最好的一家」，先把「谁能官方介绍、医保怎么走、能否探视」问清楚。",
        ],
        "今天先记下 3 个问题：①主治是否可转介安宁/姑息；②属地医保对安宁疗护的报销政策；③短期探视与床位预约流程。",
        "接话时避免推荐具体机构排名，可分享「核对清单」和公开检索方向，引导联系医院社工。",
        "辽宁属地可留意病友提到的安宁云护等线索，但务必以医院社工与卫健委公开信息核对。",
    ),
    "caregiver_burnout": _bundle(
        "caregiver_burnout",
        [
            "化疗期小状况不断，你说离不开——这不是软弱，是负荷已经超了。",
            "天天哭、灾难化想象停不下来，说明你的神经系统一直在报警，需要被看见。",
            "药在吃还这么难受，值得下次复诊时把「说明书 + 最近一周感受」一起问开药医生——我们这边不能替你调药。",
        ],
        "今天能不能先做到一件小事：让另一个人盯 2 小时输液/吃饭，你只去楼下走 10 分钟或洗把脸？",
        "强调「陪护者也需要被照顾」；若对方抗拒休息，可问「谁可以替你顶 2 小时」而不是「你应该休息」。",
    ),
    "existential": _bundle(
        "existential",
        [
            "舍不得老婆孩子、不想为死亡做准备——这些话很重，也很真实，谢谢你愿意说出来。",
            "「道理都懂但控制不住」很常见，不是心理不够强大，是人在面对重大威胁时的正常反应。",
            "活着不是为了表演坚强，而是为了你爱的人——但你也值得被陪伴，不只是去陪伴别人。",
        ],
        "今晚试着写三行：①此刻最害怕的一件事；②今天一件微小但真实的好事；③明天想问医生或想对家人说的一句话。",
        "不要急于用金句覆盖痛苦；先陪伴、再邀请微小行动；必要时建议专业心理支持资源。",
    ),
    "comparison_anxiety": _bundle(
        "comparison_anxiety",
        [
            "看到别人 CR、心里又羡慕又自责——这种感受在群里太常见了，你不是「想太多」。",
            "每个人的肿瘤类型、分期、基因、治疗线数都不同，群里的「成功案例」很难直接复制。",
            "你关心家人的未来，这份在乎本身就是在用力活着。",
        ],
        "把话题轻轻拉回「我们家这一阶段医生最关心哪 1–2 个指标」，而不是「别人怎么做到的」。",
        "避免追问病友隐私细节；可分享「个体差异」科普，减少攀比氛围。",
    ),
    "misinfo_concern": _bundle(
        "misinfo_concern",
        [
            "群里聊乔布斯、于娟、节食偏方时心慌——说明你在认真为家人负责，不是「太敏感」。",
            "很多信息混合了真实个案、情绪故事和商业营销，混在一起特别难分辨。",
            "值得和主治医生核对：「我看到的这个说法，有没有公开指南或证据？」",
        ],
        "列出 1 条让你最慌的信息，下次复诊问医生：「有没有指南层面的说法？」",
        "降温式接话：「很多病友都会查这些，值得和主治一起核对」；避免在群里站队怼人。",
        "可结合 KnowS 等公开循证检索核对指南片段，但不做治疗建议。",
    ),
    "med_self_doubt": _bundle(
        "med_self_doubt",
        [
            "一边照顾化疗病人，一边担心自己药量够不够——这种分裂感非常消耗人。",
            "说明书难懂不是你的问题，焦虑状态下读医学术语会更吃力。",
            "剂量是否调整，只能由开药医生结合复诊评估决定，志愿者可以陪你去问，但不能替医生答。",
        ],
        "复诊时带：药名、当前剂量、服药时间、最近一周睡眠/情绪自评（1–10）。",
        "可建议用豆包等工具查「注意事项」作参考，但决策仍以开药医生为准。",
    ),
    "general_support": _bundle(
        "general_support",
        [
            "愿意在群里说出这些，本身就需要勇气，谢谢你。",
            "此刻不需要一下子想通所有事，被听见也是一步。",
            "你不是一个人在扛，群里有人愿意陪你慢慢说。",
        ],
        "今晚做一件最小的事：给一位信任的人发一句「我今天有点难」。",
        "保持陪伴姿态，少给结论，多问「此刻最需要什么」。",
    ),
}


NEXT_STEPS: dict[str, list[str]] = {
    "hospice_nav": [
        "联系主治医生或医院社工，询问安宁疗护/姑息治疗转介",
        "查询属地卫健委或医保局公开的安宁疗护政策说明",
        "使用资源核对清单核对机构资质、探视与费用信息",
        "如需人工陪伴，联系蓝马甲志愿者继续陪同梳理",
    ],
    "caregiver_burnout": [
        "安排 2 小时可替换的陪护时段，优先保证基本睡眠与进食",
        "复诊时向开药医生反馈近一周情绪与躯体症状（非自行调药）",
        "若持续每日哭泣超过两周或出现自伤念头，联系心理热线或精神科复诊",
        "联系蓝马甲志愿者获得同伴倾听（非心理治疗）",
    ],
    "existential": [
        "允许自己暂时「不必想通」，减少自我批判",
        "写简短情绪日记或「三行记录」帮助外化焦虑",
        "考虑医院社工、肿瘤心理专科或正规心理咨询资源",
        "危机时拨打 120 或心理援助热线 400-161-9995",
    ],
    "comparison_anxiety": [
        "与主治确认本阶段关键随访指标与治疗目标",
        "减少在群内追问他人隐私性疗效细节",
        "阅读公开科普了解「个体差异」而非个案对比",
        "需要陪伴时联系志愿者，避免独自消化比较焦虑",
    ],
    "misinfo_concern": [
        "整理 1–2 条最担忧的信息，复诊时请医生从指南角度说明",
        "使用公开循证检索（如 KnowS）核对文献/指南片段",
        "避免自行尝试节食、偏方或未验证疗法",
        "在群内以「一起核对」而非「对错站队」方式讨论",
    ],
    "med_self_doubt": [
        "复诊时携带药品说明书与服药记录",
        "向开药医生明确提问：当前剂量是否需评估调整",
        "记录睡眠、食欲、情绪评分供医生参考",
        "勿根据网络信息自行增减药量",
    ],
    "general_support": [
        "与信任的人简短交流当前感受",
        "做一件 10 分钟内的自我照顾小事",
        "症状加重或出现危机信号时联系专业资源",
        "联系蓝马甲志愿者获得同伴支持",
    ],
}


ESCALATION: dict[str, str] = {
    "hospice_nav": "继续陪伴 + 引导官方资源核实（非紧急）",
    "caregiver_burnout": "若出现自伤/自杀念头 → 立即心理热线/急诊；否则复诊+同伴支持",
    "existential": "若表达立即自伤计划 → 危机干预；否则社工/心理专科转介",
    "comparison_anxiety": "继续陪伴，无需紧急升级（除非伴随急性精神症状）",
    "misinfo_concern": "引导医生核对，避免紧急升级",
    "med_self_doubt": "复诊提问，禁止志愿者建议调药",
    "general_support": "根据是否出现危机关键词判断",
}


CRISIS_KEYWORDS = [
    "不想活",
    "自杀",
    "自伤",
    "割",
    "跳楼",
    "结束生命",
    "活着没意思",
]


ASSISTANT_ROUTES: dict[str, str] = {
    "hospice_nav": "安宁疗护线索：安宁云护小程序 + 医院社工转介；心理议题可了解小馨宝",
    "existential": "小馨宝（肿瘤心理健康助手）— 患者/家属自助心理支持",
    "caregiver_burnout": "小馨宝 + 蓝马甲人工陪伴；用药问题问开药医生",
    "comparison_anxiety": "对应癌种专科助手（如小胰宝/小肺宝等）了解随访指标",
    "misinfo_concern": "专科助手 + KnowS 循证检索 + 主治医生核对",
    "med_self_doubt": "开药医生复诊；可参考药品说明书与注意事项",
    "general_support": "小馨宝或蓝马甲志愿者同伴支持",
}


def _check_crisis(text: str) -> bool:
    return any(kw in text for kw in CRISIS_KEYWORDS)


def generate_peer_response(moment_type: str, source_text: str = "") -> str:
    template = TEMPLATES.get(moment_type, TEMPLATES["general_support"])
    lines = [
        f"## 志愿者接话卡 · {template['moment_type']}",
        "",
        "### 共情接话示例",
    ]
    for i, line in enumerate(template["empathy_responses"], 1):
        lines.append(f"{i}. {line}")

    lines.extend(
        [
            "",
            "### 自助微行动",
            str(template["micro_action"]),
            "",
            "### 志愿者提示",
            str(template["volunteer_tip"]),
        ]
    )

    extra = template.get("extra")
    if extra:
        lines.extend(["", "### 补充说明", str(extra)])

    if _check_crisis(source_text):
        lines.extend(
            [
                "",
                "### ⚠️ 危机提示",
                "检测到可能的危机表达。请优先确认安全，建议立即联系心理援助热线 400-161-9995 或 120。",
                "志愿者接话以陪伴与转介为主，勿独自处理危机。",
            ]
        )

    lines.extend(["", DISCLAIMER_SHORT])
    return "\n".join(lines)


def suggest_next_step(moment_type: str, source_text: str = "") -> str:
    steps = NEXT_STEPS.get(moment_type, NEXT_STEPS["general_support"])
    escalation = ESCALATION.get(moment_type, "继续陪伴")

    lines = [
        "## 下一步行动建议",
        "",
        "### 建议步骤",
    ]
    for i, step in enumerate(steps, 1):
        lines.append(f"{i}. {step}")

    lines.extend(
        [
            "",
            "### 升级/转介指引",
            escalation,
            "",
            "### 社区助手导航",
            ASSISTANT_ROUTES.get(moment_type, ASSISTANT_ROUTES["general_support"]),
        ]
    )

    if _check_crisis(source_text):
        lines.extend(
            [
                "",
                "### ⚠️ 紧急",
                "检测到危机关键词：请立即协助联系 120 / 心理援助热线，并通知群管理员。",
            ]
        )

    lines.extend(["", DISCLAIMER_SHORT])
    return "\n".join(lines)


def route_to_assistant(moment_type: str) -> str:
    route = ASSISTANT_ROUTES.get(moment_type, ASSISTANT_ROUTES["general_support"])
    return (
        f"## 社区助手导航建议\n\n"
        f"情境：{moment_type}\n\n"
        f"建议参考：{route}\n\n"
        f"说明：仅为社区内工具导航，不构成诊疗推荐。\n\n"
        f"{DISCLAIMER_SHORT}"
    )
