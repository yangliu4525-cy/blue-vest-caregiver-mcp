"""Gradio Studio Demo for Blue Vest Caregiver Support MCP."""

import json
from pathlib import Path

import gradio as gr

from blue_vest.core import full_support_workflow
from blue_vest.guides import caregiver_load_check, hospice_resource_guide
from blue_vest.classifier import classify_moment, format_classification
from blue_vest.responses import generate_peer_response, suggest_next_step

ROOT = Path(__file__).parent
DEMO_CASES = json.loads((ROOT / "demo_cases.json").read_text(encoding="utf-8"))

DISCLAIMER_BANNER = (
    "【声明】本 Demo 仅供志愿者同伴支持辅助，不构成医疗诊断、心理咨询或治疗建议。"
    "请勿上传真实患者隐私信息。用药与治疗方案请咨询主治医生。"
)


def load_demo_case(index: int) -> str:
    if 0 <= index < len(DEMO_CASES):
        return DEMO_CASES[index]["text"]
    return ""


def run_workflow(text: str, region: str) -> str:
    if not text.strip():
        return "请输入或选择一段群聊文本。"
    return full_support_workflow(text, region)


def run_classify(text: str) -> str:
    if not text.strip():
        return "请输入文本。"
    result = classify_moment(text)
    return format_classification(result)


def run_response_only(text: str) -> str:
    if not text.strip():
        return "请输入文本。"
    result = classify_moment(text)
    return generate_peer_response(result.moment_type, text)


def run_load_check(q1, q2, q3, q4, q5) -> str:
    return caregiver_load_check(int(q1), int(q2), int(q3), int(q4), int(q5))


def build_ui() -> gr.Blocks:
    demo_labels = [
        f"{c['id']} | {c.get('title', '')}" for c in DEMO_CASES
    ]

    with gr.Blocks(title="蓝马甲陪护者护航 MCP") as demo:
        gr.Markdown(
            "# 蓝马甲陪护者护航 MCP\n"
            "面向小X宝社区志愿者的接话副驾驶 · 2026 小X宝黑客松 MVP Demo"
        )
        gr.Markdown(DISCLAIMER_BANNER)

        with gr.Tab("完整工作流"):
            demo_dd = gr.Dropdown(
                choices=demo_labels,
                label="Demo 场景（来自两群匿名改写）",
                value=demo_labels[0] if demo_labels else None,
            )
            text_in = gr.Textbox(
                label="群聊/家属表述",
                lines=6,
                placeholder="粘贴群聊内容或自行输入...",
                value=load_demo_case(0),
            )
            region_in = gr.Textbox(label="属地（安宁场景）", value="辽宁")
            workflow_btn = gr.Button("生成完整护航卡", variant="primary")
            workflow_out = gr.Textbox(label="输出", lines=24)

            def on_demo_select(label: str) -> str:
                if not label:
                    return ""
                idx = demo_labels.index(label)
                return load_demo_case(idx)

            demo_dd.change(on_demo_select, demo_dd, text_in)
            workflow_btn.click(run_workflow, [text_in, region_in], workflow_out)

        with gr.Tab("仅接话卡"):
            text2 = gr.Textbox(label="输入", lines=5, value=load_demo_case(1))
            btn2 = gr.Button("生成接话卡")
            out2 = gr.Textbox(label="接话卡", lines=16)
            btn2.click(run_response_only, text2, out2)

        with gr.Tab("陪护者负荷快筛"):
            gr.Markdown("1=几乎没有，5=几乎总是。此为自我关怀筛查，非诊断。")
            q1 = gr.Slider(1, 5, value=3, step=1, label="身心疲惫难以恢复")
            q2 = gr.Slider(1, 5, value=3, step=1, label="担心离开患者")
            q3 = gr.Slider(1, 5, value=3, step=1, label="睡眠问题")
            q4 = gr.Slider(1, 5, value=3, step=1, label="烦躁或哭泣")
            q5 = gr.Slider(1, 5, value=3, step=1, label="影响患者/家人")
            btn3 = gr.Button("评估负荷")
            out3 = gr.Textbox(label="结果", lines=12)
            btn3.click(run_load_check, [q1, q2, q3, q4, q5], out3)

        with gr.Tab("安宁资源核对清单"):
            region2 = gr.Textbox(label="属地", value="辽宁")
            btn4 = gr.Button("生成核对清单")
            out4 = gr.Textbox(label="清单", lines=16)
            btn4.click(hospice_resource_guide, region2, out4)

    return demo


if __name__ == "__main__":
    app = build_ui()
    app.launch(server_name="0.0.0.0", server_port=7860)
