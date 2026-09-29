"""Servidor MCP propio de Google Workspace (Lesson 6 + Bonus 2).

Expone a Kiro herramientas de SOLO LECTURA sobre Gmail y Calendar, reusando la capa
`src.integrations.google_client`. No duplica logica de acceso: es un consumidor mas
de la capa unica de integraciones.

Herramientas expuestas:
- list_recent_emails: solicitudes recientes (correos) del CDAO.
- list_upcoming_meetings: proximas reuniones agendadas.

Ejecutar (stdio): `python powers/cdao-google-power/server.py`
Requiere DATA_PROVIDER-independiente: usa credenciales Google reales via .env.
Si defines CDAO_MCP_MOCK=1, responde con datos ficticios (util para pruebas).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Permite importar `src` cuando el servidor se lanza desde el directorio del Power.
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from mcp.server.mcpserver import MCPServer  # noqa: E402

from src.security import redact_email, redaction_enabled  # noqa: E402

mcp = MCPServer("cdao-google")


def _mock_mode() -> bool:
    return os.getenv("CDAO_MCP_MOCK", "0") == "1"


def _fmt(email: str) -> str:
    return redact_email(email) if redaction_enabled() else email


@mcp.tool()
def list_recent_emails(max_results: int = 10) -> list[dict]:
    """Lista correos recientes (solicitudes) del CDAO. Solo lectura.

    Devuelve id, asunto, remitente (redactado si REDACT_PII) y fecha ISO.
    """
    if _mock_mode():
        from src.integrations.mock_provider import MockProvider

        solicitudes = MockProvider().get_solicitudes()[:max_results]
    else:
        from src.integrations import google_client

        solicitudes = google_client.fetch_solicitudes(max_results)

    return [
        {
            "id": s.id,
            "asunto": s.asunto,
            "remitente": _fmt(s.remitente.email),
            "fecha": s.fecha.isoformat(),
        }
        for s in solicitudes
    ]


@mcp.tool()
def list_upcoming_meetings(max_results: int = 10) -> list[dict]:
    """Lista proximas reuniones del calendario del CDAO. Solo lectura."""
    if _mock_mode():
        from src.integrations.mock_provider import MockProvider

        reuniones = MockProvider().get_reuniones()[:max_results]
    else:
        from src.integrations import google_client

        reuniones = google_client.fetch_reuniones(max_results)

    return [
        {
            "id": r.id,
            "titulo": r.titulo,
            "inicio": r.inicio.isoformat(),
            "fin": r.fin.isoformat(),
            "organizador": _fmt(r.organizador.email),
            "asistentes": len(r.asistentes),
        }
        for r in reuniones
    ]


if __name__ == "__main__":
    mcp.run()
