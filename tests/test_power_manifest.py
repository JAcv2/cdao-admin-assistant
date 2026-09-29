"""Valida el manifiesto del Power propio (Bonus 2), formato Agent Plugins v1."""

from __future__ import annotations

import json
from pathlib import Path

_POWER_DIR = Path(__file__).resolve().parents[1] / "powers" / "cdao-google-power"


def test_plugin_json_valido_y_completo():
    """plugin.json cumple el nucleo portable de Agent Plugins v1 (schema cerrado)."""
    manifest = json.loads((_POWER_DIR / "plugin.json").read_text(encoding="utf-8"))
    # Campos requeridos/recomendados por el estandar.
    for campo in ("$schema", "name", "version", "description", "author", "keywords"):
        assert campo in manifest, f"Falta el campo '{campo}' en plugin.json"
    assert manifest["name"] == "cdao-google-power"
    assert "agent-plugins.org" in manifest["$schema"]
    # El schema es cerrado: no deben aparecer campos no portables en el nivel superior.
    for prohibido in ("mcp", "entry", "mcpServers", "hooks", "agents", "commands"):
        assert prohibido not in manifest, f"Campo no permitido '{prohibido}' en plugin.json"


def test_skill_existe_en_estructura_estandar():
    """La skill vive en skills/<nombre>/SKILL.md."""
    skill = _POWER_DIR / "skills" / "seguimiento-cdao" / "SKILL.md"
    assert skill.exists()
    assert "seguimiento" in skill.read_text(encoding="utf-8").lower()


def test_mcp_config_del_power_es_valida():
    """mcp.json declara el servidor cdao-google como stdio."""
    cfg = json.loads((_POWER_DIR / "mcp.json").read_text(encoding="utf-8"))
    assert "cdao-google" in cfg["mcpServers"]
    server = cfg["mcpServers"]["cdao-google"]
    assert server["type"] == "stdio"
    assert "server.py" in server["args"]


def test_server_py_existe():
    assert (_POWER_DIR / "server.py").exists()
