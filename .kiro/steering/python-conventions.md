# Convenciones de Python

## Estilo
- `black` con line-length 100; `ruff` con reglas E, F, I, UP, B.
- `from __future__ import annotations` al inicio de cada modulo.
- Type hints en todas las funciones publicas. Usa sintaxis moderna (`str | None`,
  `list[X]`, `dict[K, V]`).

## Diseno
- Modelos de dominio con **Pydantic v2** (`BaseModel`), no dataclasses sueltas.
- El **motor de clustering es una funcion pura**: mismas entradas -> misma salida,
  sin efectos secundarios ni lectura de reloj/entorno. Esto habilita el
  property-based testing.
- Integraciones externas detras de la interfaz `DataProvider`. Imports de SDKs de
  Google/Azure son perezosos dentro de `LiveProvider`.

## Nombres
- Modulos y funciones en `snake_case`; clases en `PascalCase`.
- Dominio del negocio en espanol (Solicitud, Reunion, Tema); terminos tecnicos
  estandar en ingles cuando aplique (WorkItem, provider).

## Errores y logging
- No usar `print` para logica; si se registra algo con PII, pasar por
  `security.safe()` para redactar correos.
- Fallos de red o auth deben degradar con claridad, no romper el dashboard entero.
