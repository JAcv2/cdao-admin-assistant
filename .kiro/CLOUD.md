# Bonus 1 - Cloud features (opcional)

Esta leccion es opcional y requiere una suscripcion de pago de Kiro. Aqui queda
documentado como sincronizar la configuracion local a la nube y ejecutar parte del
desarrollo con Kiro Web / una sesion en la nube, sin bloquear el resto del proyecto.

## Como sincronizar la configuracion

1. Inicia sesion en Kiro con la cuenta que tenga habilitadas las funciones de nube.
2. Desde el cliente Kiro, activa **Cloud configuration** para sincronizar la carpeta
   `.kiro/` (steering, specs, hooks, agents, mcp) hacia la nube.
3. Verifica que los steering y el custom agent `cdao-assistant` aparecen disponibles en
   la sesion de nube.

## Ejecutar en la nube

1. Abre **Kiro Web** (o inicia una sesion en la nube).
2. Carga este repositorio.
3. Ejecuta una tarea del proyecto (por ejemplo, correr los tests o pedirle al agente un
   resumen usando el MCP `cdao-google` en modo mock).

## Estado en este repositorio

- La configuracion (`.kiro/`) esta lista para sincronizarse: es estandar y portable.
- El modo mock permite correr la app y los tests en la nube sin credenciales.
- Si activas datos reales en la nube, define las variables del `.env` como secretos de
  la sesion, nunca en el repositorio.

> Nota: por ser una funcion de pago, la evidencia efectiva (capturas de la sesion de
> nube) se agrega en el video demo si la suscripcion esta activa.
