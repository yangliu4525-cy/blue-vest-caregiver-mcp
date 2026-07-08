"""Orchestration helpers - re-exports for MCP and Gradio."""

from blue_vest.classifier import classify_moment, format_classification
from blue_vest.disclaimer import DISCLAIMER, DISCLAIMER_SHORT
from blue_vest.guides import caregiver_load_check, hospice_resource_guide
from blue_vest.responses import (
    generate_peer_response,
    route_to_assistant,
    suggest_next_step,
)


def full_support_workflow(text: str, region: str = "辽宁") -> str:
    result = classify_moment(text)
    parts = [
        format_classification(result),
        "",
        generate_peer_response(result.moment_type, text),
        "",
        suggest_next_step(result.moment_type, text),
        "",
        route_to_assistant(result.moment_type),
    ]
    if result.moment_type == "hospice_nav":
        parts.extend(["", hospice_resource_guide(region)])
    parts.extend(["", "---", DISCLAIMER])
    return "\n".join(parts)
