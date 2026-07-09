"""Orchestration helpers - re-exports for MCP and Gradio."""

from blue_vest.classifier import classify_moment, format_classification
from blue_vest.disclaimer import DISCLAIMER, DISCLAIMER_SHORT
from blue_vest.guides import caregiver_load_check, hospice_resource_guide
from blue_vest.responses import (
    generate_peer_response,
    route_to_assistant,
    suggest_next_step,
)
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# 初始化StepFun大模型客户端
client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL")
)
model_name = os.getenv("LLM_MODEL")


def full_support_workflow(text: str, region: str = "辽宁") -> str:
    # 拆分mcp_server传入的医学参考资料 + 用户家属原文
    if "【安宁疗护权威循证参考资料】" in text:
        medical_part, user_input = text.split("家属陪护原始描述：", 1)
        medical_ref = medical_part.strip()
        user_text = user_input.strip()
    else:
        medical_ref = "暂无检索到的医学循证资料"
        user_text = text

    # 场景分类标签识别
    result = classify_moment(user_text)

    # 重构Prompt：新增强制分行规则，保证板块边界清晰可拆分
    prompt = f"""
你是【蓝马甲安宁疗护志愿者专属AI辅助工作台】，仅服务线下安宁志愿者，禁止输出医疗诊断、用药方案、私立机构排名，所有医疗内容仅作参考，结尾必须带完整免责声明。

【硬性排版强制规则，必须严格遵守，不允许合并段落】
1. 严禁使用#、##、###等任何markdown标题标记；
2. 5个板块的标题「第一板块：xxx」「第二板块：xxx」必须**单独占一整行**；
3. 任意两个板块之间必须空一行，不能紧挨着；
4. 全文语言精简凝练，每条话术简短，杜绝冗长铺垫，整体篇幅压缩；

权威安宁疗护循证参考资料（来自专业医学知识库）
{medical_ref}

家属原始倾诉内容
{user_text}
服务属地
{region}，必须只输出当地卫健委、公立医院、医保局官方公开安宁渠道，不推荐私立机构。

按顺序输出5大板块，严格遵守上面排版规则：

第一板块：阶梯式共情对话引导（志愿者现场直接照着说）
分3条短句：浅层破冰安抚、深度共情、引导倾诉提问；
单独一段列出3条沟通禁忌，每条附带简短禁止原因。

第二板块：场景匹配循证专业参考
提炼知识库匹配的安宁疗护规范，2-4条简短要点，方便截图出示给家属。

第三板块：家属分层干预行动方案
分轻度、中度、重度三档，每一档只写现场可执行操作+对应转介渠道，文字尽量简短。

第四板块：{region}本地官方安宁资源卡片
分三类极简罗列：公立试点医院、医保报销通俗说明、24小时心理热线；标注仅官方渠道，需自行电话核实。

第五板块：志愿者自身减负疏导提示
给出1~2个5分钟快速解压小行动，简洁直白。

最后追加简洁免责声明：本工具仅志愿者同伴支持辅助，不构成医疗、心理诊疗建议，心理危机拨打全国心理援助热线400-161-9995。
"""

    # 调用StepFun大模型生成全新结构化护航卡
    resp = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6
    )
    final_content = resp.choices[0].message.content.strip()

    full_output = f"{final_content}\n\n---\n{DISCLAIMER}"
    return full_output