# cdao-google-power

Power propio (Bonus 2 del Kiro University Challenge) que empaqueta acceso de **solo
lectura** a Google Workspace (Gmail + Calendar) para la gestion administrativa de un
CDAO.

## Estructura

```
cdao-google-power/
├── plugin.json                 # Manifiesto (Agent Plugins)
├── POWER.md                    # Entry point que Kiro lee al activar
├── mcp.json                    # Config del servidor MCP propio
├── server.py                   # Servidor MCP (Gmail + Calendar)
├── skills/
│   └── seguimiento-cdao.md     # Skill de dominio
└── README.md
```

## Instalacion en Kiro

1. Panel **Powers** -> **Add power from Local Path**.
2. Selecciona la carpeta `powers/cdao-google-power`.
3. Kiro registra el servidor MCP `cdao-google` (namespaced) y carga la skill.

## Herramientas (solo lectura)

- `list_recent_emails(max_results=10)`
- `list_upcoming_meetings(max_results=10)`

## Modo de datos

- `CDAO_MCP_MOCK=1` (por defecto en la config): datos ficticios, ideal para demo.
- `CDAO_MCP_MOCK=0`: datos reales; requiere `GOOGLE_CLIENT_SECRET_FILE` y scopes
  `gmail.readonly` + `calendar.readonly`.

## Prueba rapida (standalone)

```bash
# Lista las tools y ejecuta una en modo mock
python -m pytest tests/test_mcp_server.py -q
```

## Seguridad

Solo lectura, secretos en `.env` (nunca en el repo), redaccion de PII activa por
defecto (`REDACT_PII=true`).
