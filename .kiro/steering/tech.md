# Stack tecnologico

## Lenguaje y runtime
- **Python 3.10+** (desarrollado y probado con 3.14).
- Entorno virtual en `.venv/`.

## Componentes
- **FastAPI** + **uvicorn**: API REST que expone solicitudes, reuniones, work items,
  temas y el resumen ejecutivo.
- **Streamlit**: dashboard de seguimiento (temas, personas, proyectos).
- **Pydantic v2**: modelos de dominio y validacion.
- **google-api-python-client** + **google-auth-oauthlib**: acceso de solo lectura a
  Gmail y Calendar.
- **requests**: cliente REST para Azure DevOps.
- **mcp**: SDK para el servidor MCP propio de Google.

## Testing y calidad
- **pytest**: tests unitarios y de API (TestClient).
- **Hypothesis**: property-based testing del motor de clustering.
- **ruff** + **black**: linting y formateo (line-length 100).

## Convenciones de dependencias
- Dependencias de runtime en `[project.dependencies]`; herramientas de desarrollo en
  `[project.optional-dependencies].dev`.
- Imports de librerias de Google/Azure son **perezosos** (lazy) para no exigirlas en
  modo mock.

## Comandos utiles
- Tests: `python -m pytest -q`
- Lint: `ruff check .`
- Formateo: `black .`
- API: `uvicorn src.api:app --reload`
- Dashboard: `streamlit run src/dashboard.py`
