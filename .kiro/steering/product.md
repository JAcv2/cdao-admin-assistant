# Producto: CDAO Admin Assistant

## Que es
Un agente asistente de gestion administrativa para un CDAO (Chief Data & Analytics
Officer). Consolida en un solo lugar:

- **Correos** (Gmail) que representan solicitudes que requieren seguimiento.
- **Reuniones** (Google Calendar) agendadas con el equipo.
- **Tareas / work items** (Azure DevOps) de los proyectos de datos y analitica.

## Objetivo
Mantener "on track" solicitudes, proyectos y seguimiento al equipo. El asistente
agrupa items relacionados por tema, persona y proyecto, y presenta un dashboard
ejecutivo que resume la gestion.

## Usuarios
- CDAO (usuario principal): consume el dashboard y los resumenes.
- Equipo de datos/analitica: sus solicitudes, reuniones y tareas alimentan el sistema.

## Principios de producto
1. **Solo lectura de las fuentes.** El asistente nunca modifica correos, calendarios
   ni work items. Solo observa y resume.
2. **La demo no depende de credenciales vivas.** Existe un carril de datos mock
   (ficticio) para demostraciones estables.
3. **Seguridad primero.** Ninguna informacion corporativa real vive en el repositorio.
4. **Determinismo.** El clustering se basa en reglas explicables, no en cajas negras,
   para que el CDAO confie en la agrupacion.

## No objetivos (por ahora)
- No envia correos ni crea eventos ni edita work items.
- No hace analisis semantico pesado (embeddings); el clustering es por reglas.
