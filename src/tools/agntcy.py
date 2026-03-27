"""
AGNTCY Tools -- Werkzeuge fuer das AGNTCY Multi-Agent-Netzwerk.

AGNTCY ist eine Linux Foundation Initiative (Cisco/Outshift) mit 65+ Enterprise-Partnern
fuer standardisierte Multi-Agent-Kommunikation.

Protokolle:
- ACP (Agent Communication Protocol) v1.14: Standardnachrichten zwischen Agents
- SLIM (Secure Low-latency Interactive Messaging): Sichere Echtzeit-Kommunikation
- AGNTCY Directory: Service-Registry fuer Agent-Entdeckung
"""

import uuid
from datetime import datetime, timezone
from typing import Any

from .agntcy_store import (
    load_agents,
    load_messages,
    save_agents,
    save_messages,
)

# Bekannte AGNTCY-Oekosystem-Daten (Stand Maerz 2026)
AGNTCY_ECOSYSTEM = {
    "network_name": "AGNTCY",
    "full_name": "Agent Network for Generative and Cognitive Yield",
    "foundation": "Linux Foundation",
    "founding_members": 65,
    "key_members": ["Cisco", "Dell", "Google", "Oracle", "Red Hat", "Outshift"],
    "protocols": {
        "ACP": {
            "name": "Agent Communication Protocol",
            "version": "1.14",
            "description": "Standardnachrichtenformat fuer Agent-zu-Agent-Kommunikation",
        },
        "SLIM": {
            "name": "Secure Low-latency Interactive Messaging",
            "description": "Sichere Echtzeit-Kommunikation zwischen Agents",
            "features": ["end-to-end-encryption", "low-latency", "pub-sub"],
        },
        "AGNTCY_DIR": {
            "name": "AGNTCY Directory",
            "description": "Service-Registry fuer Agent-Entdeckung und -Registrierung",
        },
    },
    "sdk": {
        "python": "acp-sdk",
        "version": "1.5.2",
        "pypi": "https://pypi.org/project/acp-sdk/",
    },
    "github": "https://github.com/agntcy",
    "website": "https://agntcy.org",
    "status": "Active Development (March 2026)",
}

# Standardisierte ACP-Capability-Typen
ACP_CAPABILITIES = [
    "text-generation", "code-generation", "data-analysis", "image-generation",
    "audio-processing", "video-processing", "web-search", "database-query",
    "file-processing", "api-integration", "translation", "summarization",
    "classification", "extraction", "reasoning", "planning", "orchestration",
    "tool-use", "memory", "workflow-automation", "monitoring", "security-audit",
]


def register_agntcy_agent(
    name: str,
    description: str,
    capabilities: list[str],
    endpoint: str,
    organization: str = "",
) -> dict[str, Any]:
    """Registriert einen Agenten im lokalen AGNTCY-kompatiblen Verzeichnis.

    Erstellt einen vollstaendigen AGNTCY Directory Entry mit ACP-kompatiblem
    Profil. Der Agent ist danach ueber discover_by_capability() auffindbar.

    Args:
        name: Agentenname (z.B. "DataAnalysisAgent")
        description: Was der Agent kann
        capabilities: Liste von Faehigkeiten (aus ACP_CAPABILITIES)
        endpoint: URL/Endpunkt des Agenten
        organization: Optional: Organisation hinter dem Agenten
    """
    if not name:
        return {"error": "Name ist Pflichtfeld"}
    if not endpoint:
        return {"error": "Endpoint ist Pflichtfeld"}

    agents = load_agents()
    now = datetime.now(timezone.utc).isoformat()

    # Pruefen ob Agent mit gleichem Namen existiert
    existing_idx = None
    for i, a in enumerate(agents):
        if a.get("name", "").lower() == name.lower():
            existing_idx = i
            break

    # AGNTCY Directory Entry Format
    agent_entry = {
        "id": str(uuid.uuid4()),
        "name": name,
        "description": description,
        "endpoint": endpoint,
        "organization": organization or "Unknown",
        "capabilities": capabilities,
        "protocol": "ACP/1.14",
        "network": "AGNTCY",
        "status": "active",
        "metadata": {
            "registeredAt": now,
            "schema": "agntcy-directory/v1",
        },
    }

    if existing_idx is not None:
        agent_entry["id"] = agents[existing_idx].get("id", str(uuid.uuid4()))
        agent_entry["metadata"]["registeredAt"] = agents[existing_idx]["metadata"].get("registeredAt", now)
        agent_entry["metadata"]["updatedAt"] = now
        agents[existing_idx] = agent_entry
        action = "updated"
    else:
        agents.append(agent_entry)
        action = "registered"

    save_agents(agents)

    return {
        "status": "success",
        "action": action,
        "agentId": agent_entry["id"],
        "name": name,
        "endpoint": endpoint,
        "capabilities": capabilities,
        "protocol": "ACP/1.14",
        "network": "AGNTCY",
        "totalAgents": len(agents),
    }


def discover_by_capability(capability: str, limit: int = 10) -> dict[str, Any]:
    """Sucht AGNTCY-Agenten nach Faehigkeit im lokalen Verzeichnis.

    Durchsucht registrierte Agents nach passenden Capabilities, Namen
    und Beschreibungen. Ideal fuer Task-Routing und Agent-Selektion.

    Args:
        capability: Gesuchte Faehigkeit (z.B. "data-analysis", "translation")
        limit: Max. Anzahl Ergebnisse (Standard: 10)
    """
    agents = load_agents()
    cap_lower = capability.lower()
    matches = []

    for agent in agents:
        score = 0
        matched_caps = []
        for cap in agent.get("capabilities", []):
            if cap_lower in cap.lower():
                score += 2
                matched_caps.append(cap)
        if cap_lower in agent.get("name", "").lower():
            score += 1
        if cap_lower in agent.get("description", "").lower():
            score += 1
        if score > 0:
            matches.append({
                "agentId": agent.get("id"),
                "name": agent.get("name"),
                "description": agent.get("description"),
                "endpoint": agent.get("endpoint"),
                "organization": agent.get("organization"),
                "matchedCapabilities": matched_caps,
                "allCapabilities": agent.get("capabilities", []),
                "relevanceScore": score,
                "protocol": agent.get("protocol", "ACP/1.14"),
            })

    matches.sort(key=lambda x: x["relevanceScore"], reverse=True)
    return {
        "query": capability,
        "found": len(matches),
        "agents": matches[:limit],
        "totalInDirectory": len(agents),
        "network": "AGNTCY",
    }


def create_acp_message(
    sender_id: str,
    receiver_id: str,
    content: str,
    message_type: str = "request",
    thread_id: str | None = None,
) -> dict[str, Any]:
    """Erstellt eine ACP-konforme Nachricht (Agent Communication Protocol v1.14).

    ACP ist der AGNTCY-Standard fuer strukturierte Agent-zu-Agent-Kommunikation.

    Args:
        sender_id: ID oder Name des sendenden Agenten
        receiver_id: ID oder Name des empfangenden Agenten
        content: Nachrichteninhalt
        message_type: Nachrichtentyp: "request", "response", "notification", "error"
        thread_id: Optional: Thread-ID fuer mehrteilige Konversationen
    """
    valid_types = ["request", "response", "notification", "error"]
    if message_type not in valid_types:
        return {"error": "Ungueltiger message_type", "validTypes": valid_types}

    message_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    # ACP Nachrichtenformat nach Spezifikation v1.14
    acp_message = {
        "acp_version": "1.14",
        "message_id": message_id,
        "thread_id": thread_id or str(uuid.uuid4()),
        "timestamp": now,
        "type": message_type,
        "sender": {"id": sender_id, "network": "AGNTCY"},
        "receiver": {"id": receiver_id, "network": "AGNTCY"},
        "payload": {"content": content, "content_type": "text/plain"},
        "metadata": {"protocol": "ACP", "schema_url": "https://agntcy.org/acp/schema/v1.14"},
    }

    messages = load_messages()
    messages.append(acp_message)
    save_messages(messages)

    return {
        "status": "created",
        "messageId": message_id,
        "threadId": acp_message["thread_id"],
        "type": message_type,
        "sender": sender_id,
        "receiver": receiver_id,
        "protocol": "ACP/1.14",
        "message": acp_message,
    }


def validate_acp_message(message: dict) -> dict[str, Any]:
    """Validiert eine ACP-Nachricht gegen die Spezifikation v1.14.

    Prueft Pflichtfelder, Typen und Formatierung nach dem
    AGNTCY Agent Communication Protocol Standard.

    Args:
        message: ACP-Nachricht als Dictionary
    """
    errors = []
    warnings = []
    required_fields = ["acp_version", "message_id", "timestamp", "type", "sender", "receiver", "payload"]

    for field in required_fields:
        if field not in message:
            errors.append(f"Pflichtfeld fehlt: {field!r}")

    if "acp_version" in message:
        supported = ["1.14", "1.13", "1.12", "1.0"]
        if message["acp_version"] not in supported:
            warnings.append(f"ACP-Version unbekannt. Unterstuetzt: {supported}")

    if "type" in message:
        valid_types = ["request", "response", "notification", "error"]
        if message["type"] not in valid_types:
            errors.append(f"Ungueltiger Typ. Erlaubt: {valid_types}")

    for field in ["sender", "receiver"]:
        if field in message:
            if isinstance(message[field], dict):
                if "id" not in message[field]:
                    errors.append(f"{field!r} braucht ein id-Feld")
            else:
                errors.append(f"{field!r} muss ein Dictionary sein")

    if "payload" in message:
        if isinstance(message["payload"], dict):
            if "content" not in message["payload"]:
                errors.append("payload braucht ein content-Feld")
        else:
            errors.append("payload muss ein Dictionary sein")

    if "thread_id" not in message:
        warnings.append("thread_id fehlt -- empfohlen fuer Konversations-Tracking")

    is_valid = len(errors) == 0
    return {
        "valid": is_valid,
        "errors": errors,
        "warnings": warnings,
        "errorCount": len(errors),
        "warningCount": len(warnings),
        "protocol": "ACP/1.14",
        "summary": "Valide ACP-Nachricht" if is_valid else f"{len(errors)} Fehler gefunden",
    }


def format_slim_message(
    sender_id: str,
    channel: str,
    payload: str,
    encrypted: bool = True,
) -> dict[str, Any]:
    """Formatiert eine SLIM-konforme Nachricht (Secure Low-latency Interactive Messaging).

    SLIM ist das AGNTCY-Protokoll fuer sichere Echtzeit-Kommunikation zwischen Agents.

    Args:
        sender_id: ID des sendenden Agenten
        channel: SLIM-Kanal (z.B. "tasks/analysis", "alerts/security")
        payload: Nachrichteninhalt
        encrypted: Ob die Nachricht verschluesselt werden soll (Standard: True)
    """
    message_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    channel_clean = channel.strip("/").lower().replace(" ", "-")

    slim_message = {
        "slim_version": "1.0",
        "message_id": message_id,
        "timestamp": now,
        "channel": channel_clean,
        "sender": sender_id,
        "encrypted": encrypted,
        "payload": {
            "data": payload if not encrypted else f"[ENCRYPTED:{len(payload)} chars]",
            "original_size": len(payload),
            "encoding": "utf-8",
        },
        "delivery": {"mode": "pub-sub", "qos": "at-least-once", "ttl_seconds": 300},
        "metadata": {"protocol": "SLIM", "network": "AGNTCY", "schema": "agntcy-slim/v1"},
    }

    return {
        "status": "formatted",
        "messageId": message_id,
        "channel": channel_clean,
        "sender": sender_id,
        "encrypted": encrypted,
        "protocol": "SLIM/1.0",
        "message": slim_message,
    }


def get_agntcy_network_info() -> dict[str, Any]:
    """Gibt Informationen ueber das AGNTCY-Netzwerk und Oekosystem zurueck.

    Zeigt Protokollversionen, Mitglieder, SDKs und aktuelle Statistiken
    des AGNTCY Multi-Agent-Netzwerks (Linux Foundation Projekt).
    """
    agents = load_agents()
    messages = load_messages()
    info = {**AGNTCY_ECOSYSTEM}
    info["local_directory"] = {
        "registeredAgents": len(agents),
        "storedMessages": len(messages),
        "status": "active",
    }
    info["available_capabilities"] = ACP_CAPABILITIES
    info["mcp_bridge"] = {
        "server": "agntcy-mcp-server",
        "version": "0.1.0",
        "tools": [
            "register_agntcy_agent",
            "discover_by_capability",
            "create_acp_message",
            "validate_acp_message",
            "format_slim_message",
            "list_agntcy_agents",
            "get_agntcy_network_info",
        ],
    }
    return info


def list_agntcy_agents(
    filter_capability: str = "",
    filter_org: str = "",
) -> dict[str, Any]:
    """Listet alle lokal registrierten AGNTCY-Agenten auf.

    Args:
        filter_capability: Optional: Nur Agenten mit dieser Capability anzeigen
        filter_org: Optional: Nur Agenten dieser Organisation anzeigen
    """
    agents = load_agents()
    result = []
    for agent in agents:
        if filter_capability:
            caps = [c.lower() for c in agent.get("capabilities", [])]
            if not any(filter_capability.lower() in c for c in caps):
                continue
        if filter_org:
            if filter_org.lower() not in agent.get("organization", "").lower():
                continue
        result.append({
            "agentId": agent.get("id"),
            "name": agent.get("name"),
            "description": agent.get("description"),
            "endpoint": agent.get("endpoint"),
            "organization": agent.get("organization"),
            "capabilities": agent.get("capabilities", []),
            "protocol": agent.get("protocol", "ACP/1.14"),
            "status": agent.get("status", "unknown"),
            "registeredAt": agent.get("metadata", {}).get("registeredAt"),
        })
    return {
        "totalAgents": len(result),
        "allAgents": len(agents),
        "filter": {
            "capability": filter_capability or None,
            "organization": filter_org or None,
        },
        "agents": result,
        "network": "AGNTCY",
    }
