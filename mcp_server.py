"""Blue Vest Caregiver Support MCP Server."""

import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

from mcp.server.fastmcp import FastMCP

from blue_vest.classifier import classify_moment, format_classification
from blue_vest.constants import DISCLAIMER_SHORT
from blue_vest.core import full_support_workflow
from blue_vest.guides import caregiver_load_check, hospice_resource_guide
from blue_vest.handoff import generate_handoff_brief
from blue_vest.responses import (
    generate_peer_response,
    route_to_assistant,
    suggest_next_step,
)


# ================= 独立的大模型调用工具 =================
def call_llm_chat(prompt: str) -> str:
    """纯粹调用大模型生成内容，专门绕过5大板块的强制输出"""
    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL")
    model = os.getenv("LLM_MODEL")

    if not api_key:
        return "⚠️ 错误：LLM_API_KEY 未配置，请检查 .env 文件。"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [
            {"role": "system",
             "content": "你是一个优秀的公众号编辑。你严格遵循用户的格式要求，不输出多余的格式框架，只输出纯文章内容。"},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        # 拼接出正确的 StepFun API 地址 (OpenAI 兼容格式)
        resp = requests.post(f"{base_url}/chat/completions", json=data, headers=headers, timeout=30)
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
        else:
            return f"⚠️ 大模型生成失败，状态码：{resp.status_code}。错误信息：{resp.text}"
    except Exception as e:
        return f"⚠️ 调用大模型时发生网络异常：{str(e)}"


def search_hospice_knowledge(user_text):
    """对接 KnowS 医学知识库（带 403 错误中文人性化提示）"""
    api_key = os.getenv("KNOWS_API_KEY")
    base_url = os.getenv("KNOWS_BASE_URL")

    if not api_key or not base_url:
        return "⚠️ 环境配置缺失：未检测到 KNOWS_API_KEY。"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {"query": user_text, "domain": "hospice"}
    request_url = f"{base_url}/v1/search"

    print(f"\n【MCP 调试】请求地址: {request_url}")
    print(f"【MCP 调试】请求数据: {data}")

    try:
        resp = requests.post(request_url, json=data, headers=headers, timeout=10)
        print(f"【MCP 调试】状态码: {resp.status_code}")

        if resp.status_code == 200:
            return json.dumps(resp.json(), ensure_ascii=False)
        elif resp.status_code == 403:
            return f"⚠️ 知识库 API 访问被拒绝（403）。\n建议：请将此电脑的公网 IP 添加到 KnowS 开发者后台(developers.nullht.com)的「IP 白名单」中。"
        else:
            return f"⚠️ 知识库请求异常，状态码：{resp.status_code}"
    except Exception as e:
        return f"⚠️ 知识库网络连接失败：{str(e)}"


mcp = FastMCP("blue-vest-caregiver", instructions="Volunteer-facing caregiver peer-support MCP.")


@mcp.tool()
def classify_caregiver_moment(text: str) -> str:
    result = classify_moment(text)
    return format_classification(result) + "\n\n" + DISCLAIMER_SHORT


@mcp.tool()
def generate_peer_response_card(text: str) -> str:
    result = classify_moment(text)
    return generate_peer_response(result.moment_type, text)


@mcp.tool()
def suggest_next_steps(text: str) -> str:
    result = classify_moment(text)
    return suggest_next_step(result.moment_type, text)


@mcp.tool()
def caregiver_load_screening(q1: int, q2: int, q3: int, q4: int, q5: int) -> str:
    return caregiver_load_check(q1, q2, q3, q4, q5)


@mcp.tool()
def hospice_resource_checklist(region: str = "辽宁") -> str:
    return hospice_resource_guide(region)


@mcp.tool()
def route_community_assistant(text: str) -> str:
    result = classify_moment(text)
    return route_to_assistant(result.moment_type)


@mcp.tool()
def full_volunteer_workflow(text: str, region: str = "辽宁") -> str:
    medical_ref = search_hospice_knowledge(text)
    full_input = f"""【安宁疗护权威循证参考资料】
{medical_ref}

家属陪护原始描述：
{text}
"""
    return full_support_workflow(full_input, region)


@mcp.tool()
def care_handoff_brief(
        stage: str, recent_changes: str, communication_preference: str = "", follow_up_items: str = ""
) -> str:
    return generate_handoff_brief(stage, recent_changes, communication_preference, follow_up_items)


# ===== 增强版：真实调用大模型的公众号生成器 =====
@mcp.tool()
def generate_wechat_draft(text: str) -> str:
    """将志愿者群聊记录/笔记草稿，提炼为符合公众号风格的治愈推文，并附带排版建议。"""
    prompt = f"""你是一位安宁疗护和心理支持领域的公众号资深编辑。
请将以下群聊精粹或服务笔记，提炼成一篇适合在微信公众号发布的暖文。

要求：
1. 请直接提供正文，开头不要有“好的”、“明白”、“根据”等废话，直接抛出标题。
2. 提炼出一个吸引人的主标题，使用 `### ` 做标题，例如 `### 真正的平静，往往来自接纳`。
3. 结构清晰，段落分明。可以包含 `引言`、`💬 群友金句节选`、`📖 心灵感悟` 等小节。
4. 善用 Emoji 情感呼应，例如 📖 ✨ ❤️ 🌸 🌟。
5. 绝对不要出现“第一板块”、“第二板块”、“第三板块”等词汇，这是一篇纯正的自然语言公众号推文。
6. 必须保留原汁原味的群友金句，并用 **加粗** 突出，让其他读者读完有共鸣、被治愈。
7. 在文章最末尾，单独空出一段，用 `💡 配图与排版建议：` 开头，给出 1-2 条封面图风格建议和 1-2 条排版小贴士。

原始对话/笔记内容：
{text}
"""
    # 这里不再调用 full_support_workflow，而是直接调用刚才新增的真实 LLM 接口！
    return call_llm_chat(prompt)

# ===== 新增：【百事通】智能行动指南 =====
@mcp.tool()
def quick_volunteer_guide(query_text: str) -> str:
    """针对志愿者的一句话难题，直接生成 4 张结构化行动卡片（话术、行动、警示、资源）。"""
    prompt = f"""你是一位资深安宁疗护志愿者培训师。
志愿者收到家属这样一句话求助："{query_text}"
请基于此，输出一段结构化的 Markdown 文本。不要用“第一板块”，用 Emoji 和加粗标题。

要求输出 4 个部分：
1. 💬 【接话话术】：给志愿者 3 句可以直接回复的共情话术。
2. ✅ 【行动建议】：给出 2 个立即可以做的微小行动。
3. 🚨 【危机警报】：如果涉及极端情绪，标明要打 400-161-9995。
4. 🏥 【资源链接】：如果有属地资源需求，引导去“本地安宁资源”查询。
"""
    return call_llm_chat(prompt)
if __name__ == "__main__":
    mcp.run()