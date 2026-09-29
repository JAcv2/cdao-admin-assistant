"""Tests del MockProvider: valida que los fixtures cargan y mapean a modelos."""

from __future__ import annotations

from src.integrations.mock_provider import MockProvider
from src.models import Reunion, Solicitud, WorkItem
from src.security import redact_email


def test_solicitudes_cargan_y_validan():
    provider = MockProvider()
    solicitudes = provider.get_solicitudes()
    assert len(solicitudes) > 0
    assert all(isinstance(s, Solicitud) for s in solicitudes)
    assert all(s.remitente.email for s in solicitudes)


def test_reuniones_cargan_y_validan():
    provider = MockProvider()
    reuniones = provider.get_reuniones()
    assert len(reuniones) > 0
    assert all(isinstance(r, Reunion) for r in reuniones)
    assert all(r.fin >= r.inicio for r in reuniones)


def test_workitems_cargan_y_validan():
    provider = MockProvider()
    items = provider.get_workitems()
    assert len(items) > 0
    assert all(isinstance(w, WorkItem) for w in items)
    assert all(w.proyecto for w in items)


def test_fixtures_no_contienen_dominios_corporativos_reales():
    """Salvaguarda: los datos de ejemplo deben ser ficticios (.example)."""
    provider = MockProvider()
    for s in provider.get_solicitudes():
        assert s.remitente.email.endswith(".example")


def test_redaccion_de_email():
    assert redact_email("ana.torres@empresa-demo.example") == "a***@empresa-demo.example"
