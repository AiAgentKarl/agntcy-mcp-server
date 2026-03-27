"""
AGNTCY MCP Server -- Brücke zwischen MCP und dem AGNTCY Multi-Agent-Netzwerk.

Ermöglicht Agent-Registrierung, Service-Discovery, ACP-Messaging
und SLIM-Kommunikation nach AGNTCY-Standard (Linux Foundation).
"""

from mcp.server.fastmcp import FastMCP

from .tools.agntcy import (
    create_acp_message,
    discover_by_capability,
    format_slim_message,
    get_agntcy_network_info,
    list_agntcy_agents,
    register_agntcy_agent,
    validate_acp_message,
)

# FastMCP Server initialisieren
mcp = FastMCP(
    "AGNTCY MCP",
    instructions=(
        "Bridges MCP with the AGNTCY multi-agent network (Linux Foundation, 65+ enterprise partners). "
        "Supports ACP (Agent Communication Protocol v1.14), SLIM secure messaging, "
        "and the AGNTCY Directory for agent discovery. "
        "Register agents, discover by capability, create ACP messages, validate protocol compliance, "
        "and format SLIM messages for secure real-time agent communication."
    ),
)


# --- Tools registrieren ---


@mcp.tool()
def tool_register_agntcy_agent(
    name: str,
    description: str,
    capabilities: list[str],
    endpoint: str,
    organization: str = "",
) -> dict:
    """Register an agent in the local AGNTCY-compatible directory.

    Creates an AGNTCY Directory Entry with ACP-compatible profile.
    The agent becomes discoverable via discover_by_capability.

    Args:
        name: Agent name (e.g. "DataAnalysisAgent")
        description: What the agent does
        capabilities: List of capabilities (e.g. ["data-analysis", "web-search"])
        endpoint: URL or address where the agent is reachable
        organization: Optional: organization behind the agent
    """
    return register_agntcy_agent(name, description, capabilities, endpoint, organization)


@mcp.tool()
def tool_discover_by_capability(capability: str, limit: int = 10) -> dict:
    """Find AGNTCY agents by capability in the local directory.

    Searches registered agents by capabilities, name and description.
    Ideal for task routing and agent selection in multi-agent systems.

    Args:
        capability: Capability to search for (e.g. "data-analysis", "translation")
        limit: Max number of results (default: 10)
    """
    return discover_by_capability(capability, limit)


@mcp.tool()
def tool_create_acp_message(
    sender_id: str,
    receiver_id: str,
    content: str,
    message_type: str = "request",
    thread_id: str = "",
) -> dict:
    """Create an ACP-compliant message (Agent Communication Protocol v1.14).

    ACP is the AGNTCY standard for structured agent-to-agent communication.
    Message types: request, response, notification, error.

    Args:
        sender_id: ID or name of the sending agent
        receiver_id: ID or name of the receiving agent
        content: Message content
        message_type: Message type: "request", "response", "notification", "error"
        thread_id: Optional thread ID for multi-turn conversations
    """
    return create_acp_message(sender_id, receiver_id, content, message_type, thread_id or None)


@mcp.tool()
def tool_validate_acp_message(message: dict) -> dict:
    """Validate an ACP message against the v1.14 specification.

    Checks required fields, types and formatting against the
    AGNTCY Agent Communication Protocol standard.

    Args:
        message: ACP message as dictionary
    """
    return validate_acp_message(message)


@mcp.tool()
def tool_format_slim_message(
    sender_id: str,
    channel: str,
    payload: str,
    encrypted: bool = True,
) -> dict:
    """Format a SLIM message (Secure Low-latency Interactive Messaging).

    SLIM is the AGNTCY protocol for secure real-time agent communication.
    Supports pub-sub, end-to-end encryption and low latency.

    Args:
        sender_id: ID of the sending agent
        channel: SLIM channel (e.g. "tasks/analysis", "alerts/security")
        payload: Message content
        encrypted: Whether to encrypt the message (default: True)
    """
    return format_slim_message(sender_id, channel, payload, encrypted)


@mcp.tool()
def tool_get_agntcy_network_info() -> dict:
    """Get information about the AGNTCY network and ecosystem.

    Shows protocol versions, member organizations, SDKs and current stats
    of the AGNTCY multi-agent network (Linux Foundation project, 65+ members).
    """
    return get_agntcy_network_info()


@mcp.tool()
def tool_list_agntcy_agents(
    filter_capability: str = "",
    filter_org: str = "",
) -> dict:
    """List all locally registered AGNTCY agents.

    Shows all agents in the local AGNTCY directory with optional
    filter by capability or organization.

    Args:
        filter_capability: Optional: only show agents with this capability
        filter_org: Optional: only show agents from this organization
    """
    return list_agntcy_agents(filter_capability, filter_org)


def main():
    """Startet den AGNTCY MCP Server."""
    mcp.run()


if __name__ == "__main__":
    main()
