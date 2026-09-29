"""Tests de mapeo del cliente Google (sin red ni credenciales).

Se prueban las funciones puras de parseo: _parse_persona y _parse_event_dt.
Las llamadas a la API real se cubren manualmente con credenciales del usuario.
"""

from __future__ import annotations

from datetime import datetime

import pytest

# Import perezoso via importlib para no exigir SDKs de Google al recolectar tests
# si no estan instalados; si faltan, se saltan estos tests.
google_client = pytest.importorskip(
    "src.integrations.google_client",
    reason="SDK de Google no instalado; test solo aplica en modo live.",
)


def test_parse_persona_con_nombre_y_email():
    p = google_client._parse_persona("Ana Torres <ana.torres@empresa-demo.example>")
    assert p.nombre == "Ana Torres"
    assert p.email == "ana.torres@empresa-demo.example"


def test_parse_persona_solo_email():
    p = google_client._parse_persona("bruno@empresa-demo.example")
    assert p.email == "bruno@empresa-demo.example"


def test_parse_event_dt_all_day():
    dt = google_client._parse_event_dt({"date": "2026-09-29"})
    assert isinstance(dt, datetime)
    assert dt.year == 2026 and dt.month == 9 and dt.day == 29


def test_parse_event_dt_datetime_z():
    dt = google_client._parse_event_dt({"dateTime": "2026-09-29T15:00:00Z"})
    assert dt.hour == 15


def test_scopes_son_readonly():
    assert all("readonly" in s for s in google_client.SCOPES)
