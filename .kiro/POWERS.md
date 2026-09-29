# Lesson 5 - Powers de Kiro

Los Powers empaquetan documentacion, guias de flujo (steering) y, opcionalmente,
servidores MCP, que Kiro carga dinamicamente cuando los necesita.

## Power oficial instalado (del registro): Postman

El registro oficial de Kiro incluye Powers de proveedores como Datadog, Dynatrace,
Figma, Neon, Netlify, Postman, Supabase, Stripe, Strands SDK y AWS Aurora.

Para este proyecto se eligio el Power de **Postman**, porque el asistente expone una
**API REST** (FastAPI) y Postman encaja directamente para probar y documentar esos
endpoints.

### Instalacion (desde el cliente Kiro)
1. Feature Panel -> **Powers**.
2. Explora el registro oficial y busca **Postman**.
3. **Install**. El onboarding puede pedir una Postman API key (opcional para probar la
   API local).

### Como se usa en este proyecto
1. Levanta la API en modo mock:
   `uvicorn src.api:app --port 8000`  (DATA_PROVIDER=mock)
2. En Postman, importa la coleccion incluida en el repo:
   `docs/postman/CDAO-Assistant.postman_collection.json`
3. Ejecuta cualquier request (Health, Solicitudes, Reuniones, Work items, Temas,
   Resumen). La variable `baseUrl` apunta a `http://127.0.0.1:8000`.
4. El Power de Postman ayuda a explorar, probar y documentar la API del asistente.

### Instalado en Kiro
El Power de Postman se instalo via **Import power from GitHub** con la URL del
subdirectorio oficial:
`https://github.com/kirodotdev/powers/tree/main/postman`
Aparece en el panel de Powers como "API Testing with Postman - by Postman". Su MCP
server `postman` es un servicio hosted (HTTP + OAuth): pide sign-in en el navegador la
primera vez que se usa una tool.

### Uso concreto en el proyecto (L5 + L3)
Se creo el hook `.kiro/hooks/api-postman-testing.json`: cuando cambia `src/api.py`,
`pyproject.toml` o la coleccion Postman, propone correr la coleccion contra la API para
validar los endpoints. Esto usa el Power de Postman en una tarea real del asistente.

### Verificado en vivo (evidencia)
El servidor MCP `postman` (hosted, HTTP + OAuth) se conecto correctamente en el panel
MCP Servers (Connected, 41 tools). Se ejecutaron tools reales desde Kiro:
- `getAuthenticatedUser` -> usuario autenticado confirmado.
- `getWorkspaces` -> se obtuvo el workspace del usuario.
- `createCollection` -> se creo la coleccion "CDAO Admin Assistant API" en la cuenta
  Postman del usuario, con los 6 endpoints (Health, Solicitudes, Reuniones, Work items,
  Temas, Resumen).

Nota: `runCollection` figura en el modo minimal del servidor pero no quedo expuesto como
tool invocable en esta version; la ejecucion de la coleccion se hace desde la app de
Postman (Run collection) o importando `docs/postman/CDAO-Assistant.postman_collection.json`.

> Evidencia para el video: muestra el Power de Postman instalado en el Feature Panel,
> importa la coleccion `docs/postman/CDAO-Assistant.postman_collection.json` y ejecuta el
> request "Resumen ejecutivo" o "Temas" contra la API corriendo (o dispara el hook).

## Power propio (Bonus 2): cdao-google-power

Ademas del Power del registro, este repo incluye un **Power construido desde cero** en
`powers/cdao-google-power/` (ver su `plugin.json`, `POWER.md` y `README.md`). Empaqueta:
- un servidor MCP propio de Google (Gmail + Calendar, solo lectura), con las tools
  `list_recent_emails` y `list_upcoming_meetings`,
- la skill `seguimiento-cdao` y documentos de contexto para la gestion del CDAO.

Instalado y verificado en Kiro: el servidor MCP `cdao-google` figura como *connected*
en el panel MCP Servers y sus tools responden con PII redactada.

Esto demuestra tanto el consumo de un Power del registro (L5) como el empaquetado de un
Power propio (Bonus 2).
