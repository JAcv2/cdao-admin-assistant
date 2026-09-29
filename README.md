# CDAO Admin Assistant

Agente asistente de gestion administrativa para un **CDAO** (Chief Data & Analytics
Officer). Consolida en un solo lugar:

- **Correos** (Gmail) como solicitudes que requieren seguimiento.
- **Reuniones** (Google Calendar) agendadas con el equipo.
- **Tareas / work items** (Azure DevOps) de los proyectos de datos y analitica.

Agrupa los items por **tema** con un motor de reglas determinista, calcula un resumen
ejecutivo (totales, personas top) y lo presenta en un **dashboard**. Todo el acceso a
las fuentes es de **solo lectura**.

> Proyecto del **Kiro University Challenge**: evidencia las 7 lecciones + Bonus 2 en la
> carpeta [`.kiro/`](.kiro) y un Power propio en [`powers/`](powers).

## Arquitectura

```
Gmail / Calendar / Azure DevOps
        │  (solo lectura)
        ▼
src/integrations  ──►  DataProvider ──►  MockProvider (fixtures)  /  LiveProvider (APIs)
        │
        ▼
src/clustering  (funcion pura, determinista)  ──►  temas + resumen
        │
        ├──►  src/api.py       (FastAPI REST)
        └──►  src/dashboard.py (Streamlit)

powers/cdao-google-power/server.py  ──►  MCP propio (Gmail/Calendar) que reusa integrations
```

La logica de acceso se escribe **una sola vez** en `src/integrations/` y la reusan la
app, el servidor MCP y el Power.

## Requisitos

- Python 3.10+ (probado con 3.14)
- Node.js 18+ (solo si usas el MCP de Azure DevOps via `npx`)

## Instalacion

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

## Ejecutar (modo mock, sin credenciales)

```bash
# API REST
uvicorn src.api:app --reload
# Dashboard
streamlit run src/dashboard.py
```

El modo por defecto es `mock` (datos ficticios), ideal para la demo. Endpoints:
`/health`, `/solicitudes`, `/reuniones`, `/workitems`, `/temas`, `/resumen`.

## Ejecutar (modo live, datos reales)

1. Copia `.env.example` a `.env` y completa los valores.
2. Google: descarga el `client_secret.json` desde Google Cloud Console (scopes de solo
   lectura `gmail.readonly`, `calendar.readonly`) y apunta `GOOGLE_CLIENT_SECRET_FILE`.
3. Azure DevOps: define `AZDO_ORG_URL`, `AZDO_PROJECT` y `AZDO_PAT` (PAT con permiso
   *Work Items - Read*).
4. Cambia `DATA_PROVIDER=live`.

> Seguridad: `.env`, tokens y `client_secret*.json` estan en `.gitignore` y **nunca**
> se suben al repositorio.

## Tests

```bash
python -m pytest -q
```

Incluye **property-based testing** (Hypothesis) sobre el motor de clustering.

## Las 9 lecciones del Challenge → donde estan

| Leccion | Evidencia |
|---------|-----------|
| **L1** Spec-driven | [`.kiro/specs/cdao-assistant/`](.kiro/specs/cdao-assistant) (requirements EARS, design, tasks) |
| **L2** Steering | [`.kiro/steering/`](.kiro/steering) (product, tech, structure, python-conventions, testing, security) |
| **L3** Hooks | [`.kiro/hooks/`](.kiro/hooks) (format-on-save, test-on-save) |
| **L4** Property-based testing | [`tests/test_clustering_properties.py`](tests/test_clustering_properties.py) + `src/clustering.py` |
| **L5** Powers | [`.kiro/POWERS.md`](.kiro/POWERS.md) (Power oficial) |
| **L6** MCP | [`.kiro/mcp.json`](.kiro/mcp.json) (Azure DevOps existente + Google propio) |
| **L7** Custom agent | [`.kiro/agents/cdao-assistant.json`](.kiro/agents/cdao-assistant.json) |
| **Bonus 1** Cloud | [`.kiro/CLOUD.md`](.kiro/CLOUD.md) (documentado, opcional) |
| **Bonus 2** Power propio | [`powers/cdao-google-power/`](powers/cdao-google-power) (plugin.json + MCP + skill) |

## Seguridad

- Secretos solo en `.env` local (gitignored). `.env.example` con placeholders.
- Acceso de **solo lectura** a todas las fuentes; scopes y PAT de minimo privilegio.
- Redaccion de PII (correos) en logs y salidas (`REDACT_PII=true`).
- Fixtures y ejemplos con datos ficticios (dominio `.example`).

## Licencia

MIT. Ver [`LICENSE`](LICENSE).
