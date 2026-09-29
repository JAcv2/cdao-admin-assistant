# Requisitos - CDAO Admin Assistant

Notacion: **EARS** (Easy Approach to Requirements Syntax). Palabras clave:
- **THE SYSTEM SHALL** (requisito ubicuo)
- **WHEN <evento> THE SYSTEM SHALL** (activado por evento)
- **WHILE <estado> THE SYSTEM SHALL** (activado por estado)
- **IF <condicion> THEN THE SYSTEM SHALL** (condicional/no deseado)
- **WHERE <caracteristica> THE SYSTEM SHALL** (opcional segun configuracion)

## 1. Ingesta de fuentes (solo lectura)

- **R1.1** THE SYSTEM SHALL leer correos recientes de Gmail y mapearlos al modelo
  `Solicitud`.
- **R1.2** THE SYSTEM SHALL leer reuniones proximas de Google Calendar y mapearlas al
  modelo `Reunion`.
- **R1.3** THE SYSTEM SHALL leer work items de Azure DevOps y mapearlos al modelo
  `WorkItem`.
- **R1.4** THE SYSTEM SHALL acceder a todas las fuentes externas en modo de **solo
  lectura**; nunca crea, edita ni elimina datos en Gmail, Calendar o Azure DevOps.
- **R1.5** WHERE `DATA_PROVIDER=mock` THE SYSTEM SHALL obtener los datos desde fixtures
  ficticios locales en lugar de las APIs reales.
- **R1.6** WHERE `DATA_PROVIDER=live` THE SYSTEM SHALL obtener los datos desde las APIs
  reales usando credenciales de `.env`.

## 2. Clustering de temas (nucleo determinista)

- **R2.1** THE SYSTEM SHALL normalizar solicitudes, reuniones y work items a un tipo
  comun `ItemSeguimiento` antes de agrupar.
- **R2.2** WHEN se solicita el agrupamiento THE SYSTEM SHALL agrupar los items en temas
  segun reglas de palabras clave, remitente/persona y proyecto.
- **R2.3** THE SYSTEM SHALL asignar cada item a **exactamente un** tema; los items que
  no coinciden con ninguna regla van al tema `sin_clasificar`.
- **R2.4** THE SYSTEM SHALL ser determinista: la misma entrada produce la misma salida.
- **R2.5** THE SYSTEM SHALL producir el mismo agrupamiento (como conjuntos) sin importar
  el orden de los items de entrada.
- **R2.6** WHEN el agrupamiento se aplica dos veces sobre el mismo resultado THE SYSTEM
  SHALL producir un resultado identico (idempotencia).
- **R2.7** THE SYSTEM SHALL preservar todos los items: la suma de items en los temas es
  igual al numero de items de entrada (sin perdidas ni duplicados).

## 3. Resumen y dashboard

- **R3.1** THE SYSTEM SHALL calcular un `ResumenGestion` con totales de solicitudes,
  reuniones y work items.
- **R3.2** THE SYSTEM SHALL calcular las personas con mas items asociados (top personas).
- **R3.3** THE SYSTEM SHALL exponer via API REST los recursos: solicitudes, reuniones,
  work items, temas y resumen.
- **R3.4** THE SYSTEM SHALL presentar un dashboard con vistas de temas, personas y
  proyectos.

## 4. Seguridad (transversal)

- **R4.1** THE SYSTEM SHALL leer secretos unicamente desde variables de entorno / `.env`
  local, nunca desde el codigo ni el repositorio.
- **R4.2** IF la redaccion de PII esta habilitada (`REDACT_PII=true`) THEN THE SYSTEM
  SHALL enmascarar correos en logs y en salidas persistidas.
- **R4.3** THE SYSTEM SHALL usar scopes de Google de solo lectura
  (`gmail.readonly`, `calendar.readonly`) y un PAT de Azure DevOps de lectura minima.
- **R4.4** THE SYSTEM SHALL operar completamente con datos ficticios cuando esta en modo
  mock, de modo que la demostracion no exponga informacion corporativa real.

## 5. Integracion con Kiro (lecciones)

- **R5.1** THE SYSTEM SHALL exponer sus fuentes a Kiro mediante servidores MCP
  (Azure DevOps existente + Google propio), en modo solo lectura.
- **R5.2** THE SYSTEM SHALL empaquetar el acceso a Google como un Power propio reutilizable.

## Trazabilidad requisito -> propiedad PBT

| Requisito | Propiedad verificada por Hypothesis |
|-----------|-------------------------------------|
| R2.3, R2.7 | Particionamiento total / no-perdida |
| R2.4 | Determinismo |
| R2.5 | Estabilidad ante reordenamiento |
| R2.6 | Idempotencia |
