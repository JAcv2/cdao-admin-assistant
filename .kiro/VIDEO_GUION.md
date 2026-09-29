# Guion del video demo (objetivo ~2:00-2:30, maximo 3 min)

Graba en **modo mock** (datos ficticios, PII redactada) para estabilidad y seguridad.
Sube el zoom del navegador y del editor a ~110-125% para legibilidad. Cierra
notificaciones y ventanas con datos reales.

## Preparacion (antes de grabar)

Activa el entorno virtual UNA vez en cada terminal (asi los comandos quedan cortos:
`pytest`, `uvicorn`, `streamlit`, sin la ruta larga):

```powershell
.\.venv\Scripts\Activate.ps1
```

Levanta los servicios (dos terminales, cada una con el venv activado):

```powershell
# Terminal 1 - API REST (mock)
$env:DATA_PROVIDER="mock"; uvicorn src.api:app --port 8000

# Terminal 2 - Dashboard (mock, PII redactada)
$env:DATA_PROVIDER="mock"; $env:REDACT_PII="true"; streamlit run src/dashboard.py --server.port 8501
```

> Nota: si NO activas el venv, antepon `.\.venv\Scripts\python.exe -m` a los comandos
> (p. ej. `.\.venv\Scripts\python.exe -m pytest ...`). El error "'-m' no se reconoce"
> ocurre cuando se ejecuta `-m pytest` sin el interprete de Python delante.

URLs listas:
- Dashboard: http://127.0.0.1:8501
- API docs (Swagger): http://127.0.0.1:8000/docs

Ten a la vista: el dashboard cargado, el editor con la carpeta `.kiro`, y el panel de
Kiro (MCP Servers + Powers).

---

## Escena 1 - Hook inicial (0:00-0:20)
**Pantalla:** dashboard ya cargado (http://127.0.0.1:8501).
**Narracion:** "Este es el CDAO Admin Assistant: consolida correos de Gmail, reuniones
de Calendar y tareas de Azure DevOps para un Chief Data Officer, los agrupa por tema y
los resume en un dashboard. Todo de solo lectura, construido con Kiro."

## Escena 2 - Demo del producto (0:20-0:55)
**Pantalla:** interactua con el dashboard.
- Señala las tarjetas de totales (solicitudes, reuniones, work items).
- Expande 1-2 temas del clustering.
- Usa el filtro por proyecto en la barra lateral.
- Señala que los correos salen redactados (a***@dominio).
**Narracion:** "Agrupa por tema con reglas deterministas, muestra las personas con mas
carga, y protege la informacion: los correos se redactan por seguridad."

## Escena 3 - Spec + Steering (0:55-1:15)  [L1, L2]
**Pantalla:** abre `.kiro/specs/cdao-assistant/requirements.md` y `.kiro/steering/`.
**Narracion:** "Antes de codificar defini los requisitos en notacion EARS y las
convenciones del proyecto en steering; Kiro las aplica en todo el repo."

## Escena 4 - Property-based testing (1:15-1:35)  [L4]
**Pantalla:** corre en terminal (con el venv ya activado):
```powershell
pytest tests/test_clustering_properties.py -q
```
(Si no activaste el venv: `.\.venv\Scripts\python.exe -m pytest tests/test_clustering_properties.py -q`)
**Narracion:** "El motor de clustering es una funcion pura. Con Hypothesis valido
propiedades generales: no-perdida de items, idempotencia y determinismo." (Muestra el
verde.)

## Escena 5 - MCP + Power (1:35-2:00)  [L6, L5, Bonus 2]
**Pantalla:** panel de Kiro -> MCP SERVERS y Powers.
- Muestra `cdao-google  Connected (2 tools)` (MCP propio) y `postman  Connected` (Power
  oficial).
- Abre `powers/cdao-google-power/` (plugin.json + skill) para el Power propio.
**Narracion:** "Integre dos servidores MCP: uno propio de Google que empaquete como
Power, y el de Postman del registro oficial para probar mi API."

## Escena 6 - Custom agent + Hooks (2:00-2:15)  [L7, L3]
**Pantalla:** abre `.kiro/agents/cdao-assistant.json` y `.kiro/hooks/`. Guarda un `.py`
para disparar el hook de formateo/tests.
**Narracion:** "Un agente a la medida con permisos restringidos y solo lectura, y hooks
que formatean y prueban al guardar."

## Escena 7 - Cierre (2:15-2:30)
**Pantalla:** el repo en GitHub (https://github.com/JAcv2/cdao-admin-assistant).
**Narracion:** "Codigo publico en GitHub, con la carpeta .kiro evidenciando las 7
lecciones y el Power propio. Gracias."

---

## Checklist de captura
- [ ] Dashboard con datos mock (correos redactados) visible
- [ ] Requisitos EARS + steering
- [ ] pytest property-based en verde
- [ ] MCP SERVERS: cdao-google Connected + postman Connected
- [ ] Power propio en powers/ (plugin.json)
- [ ] custom agent + hook disparando
- [ ] Repo publico en GitHub
- [ ] NO mostrar .env, tokens ni datos corporativos reales

## Tips
- Graba en segmentos y unelos; no necesitas una sola toma perfecta.
- Habla en primera persona mientras muestras.
- Muestra la evidencia en pantalla, no solo la menciones.

## Publicacion (recordatorio)
Post en X o LinkedIn con: enlace al repo, 2-3 oraciones, el video, hashtags
`#KiroUniversity` `#BuildWithKiro`, y etiqueta a `@kirodotdev` (X) o `@kiro` (LinkedIn).
Luego envia el formulario del challenge con las URLs (repo, post, video).
