"""Tests por ejemplo del clustering usando los fixtures mock."""

from __future__ import annotations

from src.clustering import SIN_CLASIFICAR, cluster_items, normalizar, resumir
from src.integrations.mock_provider import MockProvider


def _datos():
    p = MockProvider()
    return p.get_solicitudes(), p.get_reuniones(), p.get_workitems()


def test_normalizar_produce_ids_prefijados():
    sols, reus, wis = _datos()
    items = normalizar(sols, reus, wis)
    assert len(items) == len(sols) + len(reus) + len(wis)
    tipos = {it.id.split(":")[0] for it in items}
    assert tipos == {"solicitud", "reunion", "workitem"}


def test_clustering_agrupa_calidad_de_datos():
    sols, reus, wis = _datos()
    items = normalizar(sols, reus, wis)
    temas = {t.nombre for t in cluster_items(items)}
    assert "Calidad de datos" in temas


def test_resumen_totales_correctos():
    sols, reus, wis = _datos()
    resumen = resumir(sols, reus, wis)
    assert resumen.total_solicitudes == len(sols)
    assert resumen.total_reuniones == len(reus)
    assert resumen.total_workitems == len(wis)
    # top personas no vacio y suma consistente
    assert sum(resumen.personas_top.values()) <= len(normalizar(sols, reus, wis))


def test_items_sin_match_van_a_sin_clasificar():
    from src.models import ItemSeguimiento

    raros = [
        ItemSeguimiento(id="x:1", tipo="solicitud", titulo="zzz", persona_email="a@b.example"),
        ItemSeguimiento(id="x:2", tipo="reunion", titulo="qqq", persona_email="c@d.example"),
    ]
    temas = cluster_items(raros)
    assert len(temas) == 1
    assert temas[0].nombre == SIN_CLASIFICAR
    assert temas[0].total == 2


def test_reglas_cdao_cubren_frentes_principales():
    """Las reglas por defecto incluyen los frentes tipicos de un CDAO."""
    from src.clustering import REGLAS_DEFAULT

    nombres = {r.nombre for r in REGLAS_DEFAULT}
    esperados = {
        "Gobierno de datos",
        "Calidad de datos",
        "Tableros y BI",
        "Machine Learning y analitica",
        "Ingenieria e infraestructura",
        "Accesos y onboarding",
        "Presupuesto y licencias",
    }
    assert esperados <= nombres


def test_clustering_clasifica_ejemplos_de_cada_frente():
    """Frases representativas caen en el tema esperado."""
    from src.models import ItemSeguimiento

    casos = {
        "Actualizar el catalogo de gobierno de datos": "Gobierno de datos",
        "Nuevo dashboard de ventas en Power BI": "Tableros y BI",
        "Entrenamiento del modelo de churn": "Machine Learning y analitica",
        "Configurar pipeline ETL en Databricks": "Ingenieria e infraestructura",
        "Solicitud de acceso y credenciales": "Accesos y onboarding",
        "Renovacion de licencias y presupuesto": "Presupuesto y licencias",
    }
    for i, (texto, tema_esperado) in enumerate(casos.items()):
        item = ItemSeguimiento(
            id=f"c:{i}", tipo="solicitud", titulo=texto, persona_email="a@b.example", texto=texto
        )
        temas = cluster_items([item])
        assert temas[0].nombre == tema_esperado, f"'{texto}' -> {temas[0].nombre}"
