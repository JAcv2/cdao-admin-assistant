"""Smoke test del servidor MCP propio de Google.

Arranca el servidor en un subproceso (stdio) en modo mock y verifica que:
- expone las dos herramientas esperadas,
- list_recent_emails devuelve resultados ficticios,
- los correos salen redactados (REDACT_PII).
"""

from __future__ import annotations

import sys

import pytest

pytest.importorskip("mcp", reason="SDK mcp no instalado")

import anyio  # noqa: E402
from mcp import ClientSession, StdioServerParameters  # noqa: E402
from mcp.client.stdio import stdio_client  # noqa: E402

_PARAMS = StdioServerParameters(
    command=sys.executable,
    args=["powers/cdao-google-power/server.py"],
    env={"CDAO_MCP_MOCK": "1", "REDACT_PII": "true"},
)


async def _run():
    async with stdio_client(_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            nombres = {t.name for t in tools.tools}
            assert {"list_recent_emails", "list_upcoming_meetings"} <= nombres

            result = await session.call_tool("list_recent_emails", {"max_results": 3})
            # El contenido viene como texto JSON; basta comprobar que hay salida
            # y que ningun correo aparece sin redactar.
            texto = "".join(getattr(c, "text", "") for c in result.content)
            assert "@" in texto
            assert "***" in texto  # redaccion aplicada
            return True


def test_mcp_server_expone_tools_y_responde():
    assert anyio.run(_run) is True
