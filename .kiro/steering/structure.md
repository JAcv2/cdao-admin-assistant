# Estructura del proyecto

```
.
├── .kiro/                      # Evidencia de las lecciones de Kiro
│   ├── steering/               # L2: convenciones (este directorio)
│   ├── specs/cdao-assistant/   # L1: requirements, design, tasks (EARS)
│   ├── hooks/                  # L3: automatizaciones (ruff/black/tests)
│   ├── agents/                 # L7: custom agent
│   ├── mcp.json                # L6: servidores MCP (Azure DevOps + Google propio)
│   └── CLOUD.md                # Bonus 1: notas de cloud (opcional)
├── powers/
│   └── cdao-google-power/      # Bonus 2: Power propio (plugin.json + MCP + skills)
├── src/
│   ├── models.py               # Modelos de dominio (Pydantic)
│   ├── security.py             # Redaccion de PII
│   ├── clustering.py           # Motor de agrupacion por reglas (L4)
│   ├── api.py                  # FastAPI
│   ├── dashboard.py            # Streamlit
│   └── integrations/
│       ├── base.py             # Interfaz DataProvider (solo lectura)
│       ├── mock_provider.py    # Fixtures ficticios
│       ├── live_provider.py    # Google + Azure DevOps reales
│       └── __init__.py         # get_provider() segun DATA_PROVIDER
├── data/fixtures/              # Datos ficticios (.example)
├── tests/                      # pytest + Hypothesis
├── pyproject.toml
├── .env.example                # Placeholders (el .env real NO se commitea)
└── README.md
```

## Reglas de ubicacion
- Codigo de aplicacion en `src/`. Nada de logica de negocio fuera de ahi.
- Toda integracion externa vive en `src/integrations/` y respeta la interfaz
  `DataProvider`. Nuevos consumidores (MCP, Power) reusan esta capa, no la duplican.
- Los tests reflejan la estructura de `src/` bajo `tests/`.
- Datos de ejemplo solo en `data/fixtures/` y siempre ficticios.
