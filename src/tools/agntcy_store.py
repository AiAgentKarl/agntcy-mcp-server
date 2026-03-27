"""
AGNTCY Store — Lokaler Datenspeicher fuer AGNTCY-Agenten und Nachrichten.

Speichert registrierte Agenten und ACP-Nachrichten im Home-Verzeichnis.
"""

import json
from pathlib import Path

# Speicherort im Home-Verzeichnis
STORE_DIR = Path.home() / ".agntcy-agents"
AGENTS_FILE = STORE_DIR / "agents.json"
MESSAGES_FILE = STORE_DIR / "messages.json"


def _ensure_store():
    """Stellt sicher dass das Verzeichnis existiert."""
    STORE_DIR.mkdir(parents=True, exist_ok=True)


def load_agents() -> list:
    """Laedt alle registrierten AGNTCY-Agenten."""
    _ensure_store()
    if not AGENTS_FILE.exists():
        return []
    try:
        return json.loads(AGENTS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def save_agents(agents: list) -> None:
    """Speichert die Agenten-Liste."""
    _ensure_store()
    AGENTS_FILE.write_text(json.dumps(agents, indent=2, ensure_ascii=False), encoding="utf-8")


def load_messages() -> list:
    """Laedt alle gespeicherten ACP-Nachrichten."""
    _ensure_store()
    if not MESSAGES_FILE.exists():
        return []
    try:
        return json.loads(MESSAGES_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def save_messages(messages: list) -> None:
    """Speichert die Nachrichten-Liste."""
    _ensure_store()
    MESSAGES_FILE.write_text(json.dumps(messages, indent=2, ensure_ascii=False), encoding="utf-8")


def find_agent_by_name(name: str) -> dict | None:
    """Sucht einen Agenten nach Name (case-insensitive)."""
    agents = load_agents()
    name_lower = name.lower()
    return next((a for a in agents if a.get("name", "").lower() == name_lower), None)
