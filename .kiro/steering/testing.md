# Estrategia de testing

## Herramientas
- **pytest** para unitarios y de API.
- **Hypothesis** para property-based testing (PBT) del motor de clustering.

## Property-based testing (Lesson 4)
El motor de clustering es una funcion pura, lo que permite validar **propiedades
generales** en lugar de solo ejemplos. Propiedades derivadas de la spec:

1. **Particionamiento total**: todo item de entrada aparece en exactamente un tema
   (o en el grupo "sin_clasificar"), nunca duplicado ni perdido.
2. **No-perdida**: la suma de items en todos los temas == numero de items de entrada.
3. **Idempotencia**: agrupar dos veces produce el mismo resultado.
4. **Estabilidad ante reordenamiento**: permutar la entrada no cambia los grupos
   (comparando como conjuntos).
5. **Determinismo**: misma entrada -> misma salida.

## Convenciones
- Tests en `tests/`, nombres `test_<modulo>.py`.
- Los tests NO deben requerir red ni credenciales. Las integraciones live se prueban
  con respuestas mockeadas.
- Datos de prueba siempre ficticios.

## Comando
`python -m pytest -q`
