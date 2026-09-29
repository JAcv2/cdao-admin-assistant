"""Motor de clustering por reglas (Lesson 4).

`cluster_items` es una **funcion pura**: mismas entradas -> misma salida, sin
efectos secundarios, sin leer reloj ni entorno. Esto habilita el property-based
testing sobre propiedades generales (particionamiento total, no-perdida,
idempotencia, estabilidad ante reordenamiento, determinismo).
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime

from pydantic import BaseModel, Field

from src.models import (
    ItemSeguimiento,
    ResumenGestion,
    Reunion,
    Solicitud,
    Tema,
    WorkItem,
)

SIN_CLASIFICAR = "sin_clasificar"


class ReglaTema(BaseModel):
    """Regla de asignacion a un tema por coincidencia de palabras clave."""

    nombre: str
    keywords: list[str] = Field(default_factory=list)


# Reglas por defecto para el dominio del CDAO. El orden importa: gana el primero
# que coincide, garantizando pertenencia a exactamente un tema.
REGLAS_DEFAULT: list[ReglaTema] = [
    # El orden importa: gana el primer tema que coincide. Se incluyen variantes con y
    # sin tilde, singular/plural y terminos en ingles frecuentes en correos/work items.
    ReglaTema(
        nombre="Gobierno de datos",
        keywords=[
            "gobierno",
            "governance",
            "politica",
            "política",
            "catalogo",
            "catálogo",
            "linaje",
            "lineage",
            "glosario",
            "estandar",
            "estándar",
            "comite",
            "comité",
        ],
    ),
    ReglaTema(
        nombre="Calidad de datos",
        keywords=[
            "calidad",
            "quality",
            "inconsistencia",
            "incidencia",
            "incidente",
            "error de datos",
            "validacion",
            "validación",
            "profiling",
        ],
    ),
    ReglaTema(
        nombre="Tableros y BI",
        keywords=[
            "tablero",
            "dashboard",
            "reporte",
            "report",
            "indicador",
            "kpi",
            "powerbi",
            "power bi",
            "tableau",
            "visualizacion",
            "visualización",
        ],
    ),
    ReglaTema(
        nombre="Machine Learning y analitica",
        keywords=[
            "modelo",
            "model",
            "ml",
            "machine learning",
            "entrenamiento",
            "training",
            "prediccion",
            "predicción",
            "churn",
            "analitica",
            "analítica",
            "analytics",
            "feature",
        ],
    ),
    ReglaTema(
        nombre="Ingenieria e infraestructura",
        keywords=[
            "pipeline",
            "etl",
            "elt",
            "ingesta",
            "ingestion",
            "nube",
            "cloud",
            "azure",
            "aws",
            "databricks",
            "spark",
            "warehouse",
            "lakehouse",
            "infraestructura",
        ],
    ),
    ReglaTema(
        nombre="Accesos y onboarding",
        keywords=[
            "acceso",
            "accesos",
            "access",
            "permiso",
            "permisos",
            "credencial",
            "credenciales",
            "onboarding",
            "provisionar",
            "alta de usuario",
        ],
    ),
    ReglaTema(
        nombre="Presupuesto y licencias",
        keywords=[
            "presupuesto",
            "budget",
            "licencia",
            "licencias",
            "license",
            "costo",
            "costos",
            "facturacion",
            "facturación",
            "contrato",
        ],
    ),
]


def _texto_busqueda(item: ItemSeguimiento) -> str:
    """Concatena los campos relevantes de un item, en minusculas."""
    partes = [item.titulo, item.texto, item.proyecto or "", " ".join(item.etiquetas)]
    return " ".join(partes).lower()


def _tema_de(item: ItemSeguimiento, reglas: list[ReglaTema]) -> str:
    """Devuelve el nombre del primer tema cuya regla coincide, o SIN_CLASIFICAR."""
    texto = _texto_busqueda(item)
    for regla in reglas:
        if any(kw.lower() in texto for kw in regla.keywords):
            return regla.nombre
    return SIN_CLASIFICAR


def cluster_items(
    items: list[ItemSeguimiento],
    reglas: list[ReglaTema] | None = None,
) -> list[Tema]:
    """Agrupa items en temas de forma determinista.

    - Cada item se asigna a exactamente un tema (el primero que coincide) o a
      `sin_clasificar`.
    - La salida es estable: temas ordenados por nombre; items por id. Por eso el
      resultado no depende del orden de entrada.
    """
    reglas = reglas if reglas is not None else REGLAS_DEFAULT

    buckets: dict[str, list[ItemSeguimiento]] = {}
    keywords_por_tema: dict[str, list[str]] = {r.nombre: list(r.keywords) for r in reglas}
    for item in items:
        nombre = _tema_de(item, reglas)
        buckets.setdefault(nombre, []).append(item)

    temas: list[Tema] = []
    for nombre in sorted(buckets):
        items_ordenados = sorted(buckets[nombre], key=lambda it: it.id)
        temas.append(
            Tema(
                nombre=nombre,
                items=items_ordenados,
                keywords=keywords_por_tema.get(nombre, []),
            )
        )
    return temas


def normalizar(
    solicitudes: list[Solicitud],
    reuniones: list[Reunion],
    workitems: list[WorkItem],
) -> list[ItemSeguimiento]:
    """Convierte las tres fuentes a la forma comun `ItemSeguimiento`."""
    items: list[ItemSeguimiento] = []

    for s in solicitudes:
        items.append(
            ItemSeguimiento(
                id=f"solicitud:{s.id}",
                tipo="solicitud",
                titulo=s.asunto,
                persona_email=s.remitente.email,
                proyecto=s.proyecto,
                etiquetas=list(s.etiquetas),
                texto=f"{s.asunto} {s.resumen}",
            )
        )
    for r in reuniones:
        items.append(
            ItemSeguimiento(
                id=f"reunion:{r.id}",
                tipo="reunion",
                titulo=r.titulo,
                persona_email=r.organizador.email,
                proyecto=r.proyecto,
                etiquetas=list(r.etiquetas),
                texto=r.titulo,
            )
        )
    for w in workitems:
        items.append(
            ItemSeguimiento(
                id=f"workitem:{w.id}",
                tipo="workitem",
                titulo=w.titulo,
                persona_email=w.asignado.email if w.asignado else "",
                proyecto=w.proyecto,
                etiquetas=list(w.etiquetas),
                texto=w.titulo,
            )
        )
    return items


def resumir(
    solicitudes: list[Solicitud],
    reuniones: list[Reunion],
    workitems: list[WorkItem],
    reglas: list[ReglaTema] | None = None,
    generado_en: datetime | None = None,
) -> ResumenGestion:
    """Construye el resumen ejecutivo (totales, temas, top personas)."""
    items = normalizar(solicitudes, reuniones, workitems)
    temas = cluster_items(items, reglas)

    conteo = Counter(it.persona_email for it in items if it.persona_email)
    personas_top = dict(conteo.most_common(5))

    return ResumenGestion(
        total_solicitudes=len(solicitudes),
        total_reuniones=len(reuniones),
        total_workitems=len(workitems),
        temas=temas,
        personas_top=personas_top,
        generado_en=generado_en or datetime(2026, 1, 1, 0, 0, 0),
    )
