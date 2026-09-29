# Plan de tareas - CDAO Admin Assistant

Cada tarea produce un incremento verificable. El orden prioriza tener una demo
grabable con datos mock cuanto antes.

- [x] **1. Andamiaje + doble carril de datos.** Estructura, `pyproject.toml`,
  `.gitignore` estricto, `.env.example`, modelos Pydantic, `DataProvider` +
  `MockProvider` con fixtures ficticios. _Req: R1.1-R1.6, R4.1, R4.4._

- [x] **2. Steering documents (L2).** product, tech, structure, python-conventions,
  testing, security. _Req: transversal._

- [x] **3. Specs en EARS (L1).** requirements, design, tasks con propiedades para PBT.
  _Req: todos (documentacion)._

- [ ] **4. Motor de clustering (L4).** `clustering.py` funcion pura + suite Hypothesis.
  _Req: R2.1-R2.7._

- [ ] **5. API FastAPI + Dashboard Streamlit (mock).** Endpoints + vistas + tests API.
  _Req: R3.1-R3.4._

- [ ] **6. LiveProvider Google (Gmail+Calendar).** OAuth readonly. _Req: R1.1, R1.2, R4.3._

- [ ] **7. LiveProvider Azure DevOps.** PAT readonly + WIQL. _Req: R1.3, R4.3._

- [ ] **8. MCP Google propio + mcp.json mixto (L6).** _Req: R5.1._

- [ ] **9. Power oficial (L5).** Instalar y documentar uso. _Req: soporte dev._

- [ ] **10. Power propio cdao-google-power (Bonus 2).** plugin.json + MCP + skills.
  _Req: R5.2._

- [ ] **11. Custom agent (L7).** agents/cdao-assistant.json con permisos. _Req: R4._

- [ ] **12. Hooks (L3).** PostFileSave ruff/black + tests. _Req: transversal._

- [ ] **13. Cierre.** README, mapa leccion->archivo, CLOUD.md, guion video, verificacion
  sin secretos. _Req: R4.1._
