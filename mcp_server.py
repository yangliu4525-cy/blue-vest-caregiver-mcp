"""Blue Vest Caregiver Support MCP Server."""

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

mcp = FastMCP(
    "blue-vest-caregiver",
    instructions="Volunteer-facing caregiver peer-support MCP. Not medical advice.",
)


@mcp.tool()
def classify_caregiver_moment(text: str) -> str:
    """Classify caregiver chat moment type (not a clinical diagnosis)."""
    result = classify_moment(text)
    return format_classification(result) + "\n\n" + DISCLAIMER_SHORT


@mcp.tool()
def generate_peer_response_card(text: str) -> str:
    """Generate peer-support response card for volunteers."""
    result = classify_moment(text)
    return generate_peer_response(result.moment_type, text)


@mcp.tool()
def suggest_next_steps(text: str) -> str:
    """Suggest next actions and escalation guidance."""
    result = classify_moment(text)
    return suggest_next_step(result.moment_type, text)


@mcp.tool()
def caregiver_load_screening(q1: int, q2: int, q3: int, q4: int, q5: int) -> str:
    """Caregiver load quick screen. Scores 1-5 each question. Not a diagnosis."""
    return caregiver_load_check(q1, q2, q3, q4, q5)


@mcp.tool()
def hospice_resource_checklist(region: str = "辽宁") -> str:
    """Hospice resource verification checklist. No facility rankings."""
    return hospice_resource_guide(region)


@mcp.tool()
def route_community_assistant(text: str) -> str:
    """Route to community assistant tools (navigation only)."""
    result = classify_moment(text)
    return route_to_assistant(result.moment_type)


@mcp.tool()
def full_volunteer_workflow(text: str, region: str = "辽宁") -> str:
    """Full workflow: classify + response + steps + navigation + hospice checklist."""
    return full_support_workflow(text, region)


@mcp.tool()
def care_handoff_brief(
    stage: str,
    recent_changes: str,
    communication_preference: str = "",
    follow_up_items: str = "",
) -> str:
    """Generate volunteer shift handoff brief from structured demo info (not real PHI)."""
    return generate_handoff_brief(
        stage, recent_changes, communication_preference, follow_up_items
    )


if __name__ == "__main__":
    mcp.run()
