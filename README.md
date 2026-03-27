# agntcy-mcp-server

MCP bridge for the **AGNTCY multi-agent network** — agent registry, ACP messaging, SLIM protocol, and capability discovery.

[![PyPI version](https://badge.fury.io/py/agntcy-mcp-server.svg)](https://pypi.org/project/agntcy-mcp-server/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What is AGNTCY?

**AGNTCY** (Agent Network for Generative and Cognitive Yield) is a Linux Foundation initiative with 65+ enterprise partners (Cisco, Dell, Google, Oracle, Red Hat) for standardized multi-agent communication.

Key protocols:
- **ACP** (Agent Communication Protocol v1.14): Standard message format for agent-to-agent communication
- **SLIM** (Secure Low-latency Interactive Messaging): Secure real-time communication with pub-sub and encryption
- **AGNTCY Directory**: Service registry for agent discovery

## Features (7 Tools)

| Tool | Description |
|------|-------------|
| `register_agntcy_agent` | Register an agent in the local AGNTCY directory |
| `discover_by_capability` | Find agents by capability (ranked by relevance) |
| `create_acp_message` | Create ACP v1.14 compliant messages |
| `validate_acp_message` | Validate ACP message against spec |
| `format_slim_message` | Format SLIM secure messages |
| `get_agntcy_network_info` | AGNTCY ecosystem info (protocols, members, SDKs) |
| `list_agntcy_agents` | List registered agents with filters |

## Installation

```bash
pip install agntcy-mcp-server
```

## Usage with Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "agntcy": {
      "command": "agntcy-server"
    }
  }
}
```

## Example Usage

**Register an agent:**
```
register_agntcy_agent("DataBot", "Analyzes datasets", ["data-analysis", "summarization"], "https://databot.example.com")
```

**Discover agents by capability:**
```
discover_by_capability("data-analysis")
```

**Create an ACP message:**
```
create_acp_message("agent-1", "agent-2", "Please analyze this dataset", "request")
```

**Format a SLIM message:**
```
format_slim_message("agent-1", "tasks/analysis", "dataset payload", encrypted=True)
```

## Related Servers

- [a2a-protocol-mcp-server](https://pypi.org/project/a2a-protocol-mcp-server/) — Google A2A Protocol bridge
- [anp-bridge-mcp-server](https://pypi.org/project/anp-bridge-mcp-server/) — Agent Network Protocol (ANP) bridge
- [agent-directory-mcp-server](https://pypi.org/project/agent-directory-mcp-server/) — General agent service registry

## Links

- [AGNTCY Website](https://agntcy.org)
- [AGNTCY GitHub](https://github.com/agntcy)
- [ACP SDK on PyPI](https://pypi.org/project/acp-sdk/)
- [Linux Foundation Announcement](https://www.linuxfoundation.org/press/linux-foundation-welcomes-the-agntcy-project-to-standardize-open-multi-agent-system-infrastructure-and-break-down-ai-agent-silos)

## License

MIT
