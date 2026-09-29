# Seguridad de informacion corporativa

Requisito transversal: proteger informacion corporativa sin bloquear el desarrollo.

## Secretos y credenciales
- Secretos SOLO en `.env` local. **Nunca** commitear `.env`, tokens, `client_secret*.json`,
  `token.json`, PATs ni service accounts. El `.gitignore` los excluye explicitamente.
- Mantener `.env.example` con placeholders, sin valores reales.
- Antes de cualquier commit, verificar que no se cuele un secreto (revisar diff).

## Acceso de solo lectura y minimo privilegio
- Google OAuth con scopes de solo lectura: `gmail.readonly`, `calendar.readonly`.
- Azure DevOps con PAT de permisos minimos de lectura (Work Items - Read).
- El asistente nunca escribe en las fuentes externas.

## PII y datos en disco
- Cualquier salida persistida o log que pueda contener correos/nombres debe pasar por
  `src/security.py` (`safe()` / `redact_*`). Redaccion activa por defecto
  (`REDACT_PII=true`).
- Datos runtime reales (`data/live/`, `data/cache/`) estan gitignored; nunca al repo.

## Repositorio publico
- Capturas, ejemplos y fixtures usan datos ficticios (dominios `.example`).
- No incluir nombres de organizacion, proyectos internos ni correos reales en docs.

## Custom agent (L7)
- Permisos de terminal restringidos: permitir `pytest`, `ruff`, `black`; bloquear
  comandos destructivos.
- Acceso de solo lectura a las fuentes externas via MCP.
