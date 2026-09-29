---
name: seguimiento-cdao
description: >-
  Como resumir y priorizar la gestion administrativa de un CDAO a partir de correos,
  reuniones y work items. Usar cuando se trabaje con solicitudes, seguimiento del
  equipo o agrupacion de temas.
---

# Skill: Seguimiento de la gestion del CDAO

Guia de dominio para que el agente resuma y priorice la gestion administrativa de un
CDAO a partir de correos (Gmail), reuniones (Calendar) y work items (Azure DevOps).

## Objetivo
Mantener "on track" solicitudes, proyectos y seguimiento al equipo, produciendo
resumenes accionables y agrupados por tema.

## Como priorizar
1. **Urgencia + impacto.** Solicitudes con palabras como "incidencia", "calidad",
   "produccion" o "bloqueante" son de prioridad alta.
2. **Proyecto.** Agrupa por proyecto (p. ej. Plataforma de Datos, Analitica Avanzada,
   Gobierno de Datos) para dar vision por frente de trabajo.
3. **Persona.** Identifica quien solicita/organiza/ejecuta mas, para balancear carga.

## Como resumir
- Agrupa los items por tema usando reglas de palabras clave (calidad, accesos,
  modelos, presupuesto, gobierno).
- Por cada tema, lista: cantidad de items, personas involucradas y proyecto dominante.
- Destaca lo que requiere accion del CDAO esta semana (reuniones proximas + solicitudes
  de alta prioridad).

## Reglas de seguridad (obligatorias)
- Trata todo acceso como **solo lectura**: no propongas enviar correos, crear eventos ni
  editar work items salvo peticion explicita del usuario.
- Al mostrar correos en resumenes que puedan quedar en disco, **redacta** el local-part
  del email (p. ej. `a***@dominio`).
- No expongas informacion corporativa real en ejemplos o documentacion.

## Herramientas disponibles (via MCP)
- `list_recent_emails(max_results)`
- `list_upcoming_meetings(max_results)`
