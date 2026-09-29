# Lesson 6 - Servidores MCP registrados

`.kiro/mcp.json` registra dos servidores MCP (evidencia de la Lesson 6). Este archivo
documenta cada uno, ya que el JSON no admite comentarios estandar.

## 1. `azure-devops` (existente, de Microsoft)

- Comando: `npx -y @azure-devops/mcp <tu-organizacion>`
- Estado: `disabled: true`.
- Motivo: el MCP oficial de Azure DevOps requiere **Azure CLI** (`az login`) para
  autenticarse, y el entorno actual no tiene permisos de administrador para instalar
  Azure CLI.
- Como activarlo: instala Azure CLI, ejecuta `az login`, reemplaza `tu-organizacion`
  por tu organizacion real y pon `disabled: false`.
- Alternativa en uso: la app Python lee Azure DevOps via **PAT de solo lectura**
  (`src/integrations/azure_client.py`, variables `AZDO_*` en `.env`). Verificado en
  live (50 work items leidos).

## 2. `cdao-google` (propio)

- Comando: Python del venv del proyecto ejecutando
  `powers/cdao-google-power/server.py`.
- Estado: `disabled: false`.
- Herramientas (solo lectura): `list_recent_emails`, `list_upcoming_meetings`.
- Datos: `CDAO_MCP_MOCK=1` usa fixtures ficticios (demo estable). Ponlo en `0` y
  configura `GOOGLE_CLIENT_SECRET_FILE` para datos reales (OAuth readonly, verificado
  en live).
- Este mismo servidor se empaqueta como Power propio en `powers/cdao-google-power/`
  (Bonus 2).

## Nota sobre la carga del servidor propio

El servidor `cdao-google` necesita el interprete de Python del **venv** (que tiene
las dependencias `mcp` y las de Google). Por eso el `command` apunta a
`${workspaceFolder}/.venv/Scripts/python.exe`. Si Kiro no lo levanta automaticamente,
reconecta el servidor desde la vista **MCP Servers** del Feature Panel.
