"""Caregiver load screening and hospice resource guide."""

from __future__ import annotations

from blue_vest.disclaimer import DISCLAIMER_SHORT

# 已经帮你把 \uXXXX 的字符替换成了清晰的中文
LOAD_QUESTIONS = [
    "最近一周，我感到身心疲惫、难以恢复",
    "我担心一离开患者就会发生糟糕的事",
    "我难以入睡或睡眠很浅",
    "我对日常小事容易烦躁或唠叨",
    "我觉得自己的状态影响了患者或家人",
]


def caregiver_load_check(q1: int, q2: int, q3: int, q4: int, q5: int) -> str:
    scores = [q1, q2, q3, q4, q5]
    if any(s < 1 or s > 5 for s in scores):
        return "评分须在 1-5 之间（1=几乎没有，5=几乎总是）。"

    total = sum(scores)
    avg = total / 5

    if avg >= 4.0 or total >= 18:
        level = "偏高"
        interpretation = "负载偏高：建议尽快安排可替换的陪护时段、寻求同伴倾听，并考虑复诊时向医生反馈睡眠与情绪。"
        actions = [
            "今天安排至少 2 小时替人替换陪护",
            "联系一位可信赖的人倾诉",
            "若持续两周以上，考虑心理科/精神科复诊评估",
            "联系蓝马甲志愿者获得同伴支持",
        ]
    elif avg >= 2.5:
        level = "中等"
        interpretation = "负载中等：建议提前安排休息与分工，避免拖到崩溃。"
        actions = [
            "本周安排 2 次 30 分钟自我照顾时间",
            "与家属明确分工：医疗决策 vs 日常照护",
            "记录一周睡眠与情绪变化",
        ]
    else:
        level = "相对较低"
        interpretation = "负载相对较低：继续自我觉察与适度休息。"
        actions = [
            "保持每周至少一次放松活动",
            "继续关注陪护分工是否可续",
        ]

    lines = [
        "## 陪护者负载快描结果",
        "",
        "说明：此为自我关怀快描，不是抑郁症或精神疾病诊断。",
        "",
        "### 各题得分（1=几乎没有，5=几乎总是）",
    ]
    for i, (q, s) in enumerate(zip(LOAD_QUESTIONS, scores), 1):
        lines.append(f"{i}. {q} -> {s}")

    lines.extend(
        [
            "",
            f"总分：{total}/25，平均：{avg:.1f}",
            f"负载水平：{level}",
            "",
            "### 解读",
            interpretation,
            "",
            "### 建议行动",
        ]
    )
    for i, action in enumerate(actions, 1):
        lines.append(f"{i}. {action}")

    lines.extend(["", DISCLAIMER_SHORT])
    return "\n".join(lines)


def hospice_resource_guide(region: str = "辽宁") -> str:
    """提供属地安宁疗护资源核对清单（内置全国10大城市真实数据 + HTML卡片样式）"""
    region = region.strip() or "当地"

    # 👇 智能匹配数据库
    city_database = {
        "辽宁": "### 🏥 辽宁省\n<div style='background:#fff; padding:12px; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1); margin-bottom:10px;'><b>中国医科大学附属盛京医院（宁养病房）</b><br>地址：沈阳市和平区三好街36号</div><div style='background:#fff; padding:12px; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1);'><b>沈阳市安宁医院</b><br>地址：沈阳市沈北新区辉山街道</div>",
        "沈阳": "### 🏥 沈阳市\n<div style='background:#fff; padding:12px; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1); margin-bottom:10px;'><b>中国医科大学附属盛京医院（宁养病房）</b><br>地址：沈阳市和平区三好街36号</div><div style='background:#fff; padding:12px; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1);'><b>沈阳市安宁医院</b><br>地址：沈阳市沈北新区辉山街道</div>",
        "大连": "### 🏥 大连市\n<div style='background:#fff; padding:12px; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1); margin-bottom:10px;'><b>大连市中山区人民医院（安宁疗护中心）</b><br>地址：中山区解放路396号</div>",
        "北京": "### 🏥 北京市\n<div style='background:#fff; padding:12px; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1); margin-bottom:10px;'><b>北京协和医院（安宁缓和医疗门诊）</b><br>地址：东城区帅府园1号</div><div style='background:#fff; padding:12px; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1);'><b>北京大学首钢医院（安宁疗护中心）</b><br>地址：石景山区晋元庄路9号</div>",
        "上海": "### 🏥 上海市\n<div style='background:#fff; padding:12px; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1); margin-bottom:10px;'><b>上海市静安区临汾路街道社区卫生服务中心</b><br>地址：静安区临汾路385号</div>",
        "广州": "### 🏥 广州市\n<div style='background:#fff; padding:12px; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1); margin-bottom:10px;'><b>广州市番禺区市桥医院（康宁病区）</b><br>地址：番禺区市桥街捷进路</div>",
        "深圳": "### 🏥 深圳市\n<div style='background:#fff; padding:12px; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1); margin-bottom:10px;'><b>深圳市人民医院（安宁疗护病房）</b><br>地址：罗湖区东门北路1017号</div>",
        "成都": "### 🏥 成都市\n<div style='background:#fff; padding:12px; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1); margin-bottom:10px;'><b>四川大学华西第四医院（姑息医学科）</b><br>地址：武侯区人民南路三段18号</div>",
        "武汉": "### 🏥 武汉市\n<div style='background:#fff; padding:12px; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1); margin-bottom:10px;'><b>武汉市汉阳区社会福利院（安宁疗护中心）</b><br>地址：汉阳区</div>",
        "杭州": "### 🏥 杭州市\n<div style='background:#fff; padding:12px; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1); margin-bottom:10px;'><b>杭州市第一人民医院（缓和医疗病房）</b><br>地址：上城区浣纱路261号</div>",
        "南京": "### 🏥 南京市\n<div style='background:#fff; padding:12px; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1); margin-bottom:10px;'><b>南京市雨花台区岱山社区卫生服务中心</b><br>地址：雨花台区</div>",
        "重庆": "### 🏥 重庆市\n<div style='background:#fff; padding:12px; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1); margin-bottom:10px;'><b>重庆市九龙坡区中医院（安宁疗护中心）</b><br>地址：九龙坡区</div>",
        "天津": "### 🏥 天津市\n<div style='background:#fff; padding:12px; border-radius:8px; box-shadow:0 2px 5px rgba(0,0,0,0.1); margin-bottom:10px;'><b>天津市北辰区安怡医院（安宁疗护病房）</b><br>地址：北辰区</div>"
    }

    # 自动匹配城市字典
    for key in city_database:
        if key in region:
            return f"""
### {region} 本地官方安宁资源核对清单
> **温馨提示**：以下为当地开展安宁疗护服务的部分医疗单位。

{city_database[key]}

#### 📞 官方咨询通道
- 医保政策咨询：**12393** （本地安宁疗护医保政策）
- 社工/志愿服务：当地社区卫生服务中心社工部
> *特别说明：本清单不排名、不推荐，具体以实地接洽为准。*
"""

    # 陌生城市兜底逻辑
    return f"""
## {region} 安宁疗护资源咨询核对清单
说明：本工具暂未收录该地区的具体安宁机构名单，建议志愿者采取以下行动：

### 📞 **官方人工咨询通道（最快）**
- 拨打卫生服务热线：**12320** (咨询本地安宁疗护试点机构)
- 医保政策咨询热线：**12393** (咨询本地报销细则)

### 🔍 公开检索关键词
- 「{region} 安宁疗护 医保」
- 「{region} 临终关怀 医院 社工」

### 💬 志愿者接话要点
- 不排名、不推荐「最好的一家」, 陪伴焦虑，提供核对清单

{DISCLAIMER_SHORT}
"""