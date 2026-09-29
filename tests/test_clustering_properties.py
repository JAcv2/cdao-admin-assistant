"""Property-based testing del motor de clustering (Lesson 4).

Cada propiedad corresponde a un requisito EARS de la spec:
- Particionamiento total / no-perdida -> R2.3, R2.7
- Determinismo -> R2.4
- Estabilidad ante reordenamiento -> R2.5
- Idempotencia -> R2.6
"""

from __future__ import annotations

from hypothesis import given, settings
from hypothesis import strategies as st

from src.clustering import REGLAS_DEFAULT, SIN_CLASIFICAR, cluster_items
from src.models import ItemSeguimiento

# Vocabulario que mezcla keywords conocidas y palabras neutras, para ejercitar
# tanto coincidencias como el bucket sin_clasificar.
_PALABRAS = [
    "calidad",
    "acceso",
    "modelo",
    "presupuesto",
    "gobierno",
    "churn",
    "onboarding",
    "licencia",
    "reporte",
    "reunion",
    "pendiente",
    "varios",
]


@st.composite
def items(draw) -> ItemSeguimiento:
    idx = draw(st.integers(min_value=0, max_value=10_000))
    tipo = draw(st.sampled_from(["solicitud", "reunion", "workitem"]))
    titulo = draw(st.lists(st.sampled_from(_PALABRAS), min_size=0, max_size=4))
    etiquetas = draw(st.lists(st.sampled_from(_PALABRAS), min_size=0, max_size=3))
    return ItemSeguimiento(
        id=f"{tipo}:{idx}",
        tipo=tipo,
        titulo=" ".join(titulo) or "sin titulo",
        persona_email=f"persona{idx}@empresa-demo.example",
        proyecto=draw(st.sampled_from([None, "Plataforma de Datos", "Analitica Avanzada"])),
        etiquetas=etiquetas,
        texto=" ".join(titulo),
    )


def _lista_items():
    # Ids unicos para evitar ambiguedad al comparar como conjuntos.
    return st.lists(items(), min_size=0, max_size=30, unique_by=lambda it: it.id)


def _ids_en(temas) -> set[str]:
    return {it.id for tema in temas for it in tema.items}


@given(_lista_items())
@settings(max_examples=200)
def test_no_perdida_y_sin_duplicados(entrada):
    """R2.7: la suma de items en los temas == items de entrada, sin duplicados."""
    temas = cluster_items(entrada, REGLAS_DEFAULT)
    total = sum(t.total for t in temas)
    assert total == len(entrada)
    assert _ids_en(temas) == {it.id for it in entrada}


@given(_lista_items())
@settings(max_examples=200)
def test_particionamiento_cada_item_en_un_solo_tema(entrada):
    """R2.3: cada id aparece en exactamente un tema."""
    temas = cluster_items(entrada, REGLAS_DEFAULT)
    vistos: list[str] = [it.id for tema in temas for it in tema.items]
    assert len(vistos) == len(set(vistos))


@given(_lista_items())
@settings(max_examples=200)
def test_determinismo(entrada):
    """R2.4: misma entrada -> misma salida."""
    r1 = cluster_items(entrada, REGLAS_DEFAULT)
    r2 = cluster_items(entrada, REGLAS_DEFAULT)
    assert [(t.nombre, [it.id for it in t.items]) for t in r1] == [
        (t.nombre, [it.id for it in t.items]) for t in r2
    ]


@given(_lista_items(), st.randoms())
@settings(max_examples=200)
def test_estabilidad_ante_reordenamiento(entrada, rnd):
    """R2.5: permutar la entrada no cambia los grupos (como conjuntos)."""
    barajada = entrada[:]
    rnd.shuffle(barajada)
    orig = {t.nombre: {it.id for it in t.items} for t in cluster_items(entrada, REGLAS_DEFAULT)}
    perm = {t.nombre: {it.id for it in t.items} for t in cluster_items(barajada, REGLAS_DEFAULT)}
    assert orig == perm


@given(_lista_items())
@settings(max_examples=200)
def test_idempotencia(entrada):
    """R2.6: reagrupar los items ya agrupados produce el mismo resultado."""
    temas1 = cluster_items(entrada, REGLAS_DEFAULT)
    plano = [it for tema in temas1 for it in tema.items]
    temas2 = cluster_items(plano, REGLAS_DEFAULT)
    assert [(t.nombre, {it.id for it in t.items}) for t in temas1] == [
        (t.nombre, {it.id for it in t.items}) for t in temas2
    ]


@given(_lista_items())
@settings(max_examples=100)
def test_solo_nombres_de_temas_validos(entrada):
    """Todo tema producido es una regla conocida o sin_clasificar."""
    nombres_validos = {r.nombre for r in REGLAS_DEFAULT} | {SIN_CLASIFICAR}
    temas = cluster_items(entrada, REGLAS_DEFAULT)
    assert all(t.nombre in nombres_validos for t in temas)
