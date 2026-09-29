# Guion del video demo (30 s - 3 min)

Objetivo: mostrar la app funcionando y explicar como se aplico cada leccion. Graba en
**modo mock** para estabilidad. Ten la terminal y el navegador listos.

## Preparacion (antes de grabar)
```bash
.\.venv\Scripts\Activate.ps1
# Terminal 1: API
uvicorn src.api:app --port 8000
# Terminal 2: Dashboard
streamlit run src/dashboard.py
```

## Guion (≈ 2:30)

**0:00-0:20 — Que es**
"Este es el CDAO Admin Assistant: consolida correos, reuniones y tareas de Azure DevOps
para un Chief Data Officer, agrupa por tema y lo resume en un dashboard. Todo de solo
lectura y construido con Kiro."

**0:20-0:50 — Dashboard en accion**
Muestra el dashboard: tarjetas de totales, temas agrupados, ranking de personas y el
filtro por proyecto. Señala que los correos salen redactados (seguridad de PII).

**0:50-1:10 — Spec + Steering (L1, L2)**
Abre `.kiro/specs/cdao-assistant/requirements.md` (requisitos EARS) y `.kiro/steering/`.
"Defini requisitos y convenciones antes de codificar; Kiro los aplica en todo el repo."

**1:10-1:35 — Property-based testing (L4)**
Corre `python -m pytest tests/test_clustering_properties.py -q`. "El clustering es una
funcion pura; Hypothesis valida propiedades: no-perdida, idempotencia, determinismo."

**1:35-2:00 — MCP + Power (L6, Bonus 2)**
Muestra `.kiro/mcp.json` (Azure DevOps + Google propio) y `powers/cdao-google-power/`.
Invoca en Kiro la tool `list_recent_emails`. "Un MCP propio empaquetado como Power."

**2:00-2:20 — Custom agent + Hooks (L7, L3)**
Abre `.kiro/agents/cdao-assistant.json` (permisos de terminal, acceso solo lectura) y
`.kiro/hooks/`. Guarda un archivo `.py` para disparar el formateo/tests.

**2:20-2:30 — Cierre**
"Codigo publico en GitHub, carpeta .kiro con las 7 lecciones + bonus. Gracias."

## Checklist de captura
- [ ] Dashboard con datos mock visible
- [ ] Requisitos EARS + steering
- [ ] pytest property-based en verde
- [ ] mcp.json + Power propio + tool ejecutada
- [ ] custom agent + hook disparando
- [ ] No mostrar `.env` ni credenciales reales
```

## Publicacion (recordatorio)
Post en X o LinkedIn con: enlace al repo, 2-3 oraciones, el video, hashtags
`#KiroUniversity` `#BuildWithKiro`, y etiqueta a `@kirodotdev` (X) o `@kiro` (LinkedIn).
