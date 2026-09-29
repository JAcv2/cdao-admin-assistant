---
name: cdao-google-power
description: >-
  Acceso de solo lectura a Google Workspace (Gmail + Calendar) para la gestion
  administrativa de un CDAO. Activa este Power cuando trabajes con correos,
  reuniones, solicitudes o seguimiento del equipo.
keywords: [cdao, gmail, calendar, google workspace, reunion, solicitud, seguimiento]
version: 0.1.0
license: MIT
---

# CDAO Google Power

Este Power le da a Kiro acceso de **solo lectura** a Google Workspace para apoyar la
gestion administrativa de un CDAO (Chief Data & Analytics Officer).

## Que incluye

| Archivo | Proposito |
|---------|-----------|
| `plugin.json` | Manifiesto Agent Plugins (nombre, version, skills, mcp, entry). |
| `mcp.json` | Configuracion del servidor MCP propio (stdio, python). |
| `server.py` | Servidor MCP de Google: expone tools de Gmail y Calendar. |
| `skills/seguimiento-cdao.md` | Skill: como resumir y priorizar la gestion del CDAO. |
| `README.md` | Instalacion y uso. |

## Herramientas MCP expuestas (solo lectura)

- `list_recent_emails(max_results)` — correos recientes (solicitudes) del CDAO.
- `list_upcoming_meetings(max_results)` — proximas reuniones agendadas.

Ambas redactan los correos si `REDACT_PII=true`. Con `CDAO_MCP_MOCK=1` responden con
datos ficticios (util para demos y pruebas sin credenciales).

## Onboarding

1. Instala el Power desde el panel **Powers** de Kiro (Add power from Local Path ->
   selecciona `powers/cdao-google-power`).
2. Kiro registra el servidor MCP `cdao-google` de forma namespaced.
3. Para datos reales: pon `CDAO_MCP_MOCK=0` y define `GOOGLE_CLIENT_SECRET_FILE`
   (scopes de solo lectura: `gmail.readonly`, `calendar.readonly`).

## Seguridad

- Solo lectura: nunca modifica correos ni eventos.
- Secretos en `.env`, jamas en el repositorio.
- Redaccion de PII activa por defecto.

## Metadata

- Maintainer: participante del Kiro University Challenge.
- MCP server: propio (`server.py`), reusa `src/integrations/google_client.py`.
