"""Tests de la API FastAPI sobre el MockProvider (sin red, sin credenciales)."""

from __future__ import annotations

import os

from fastapi.testclient import TestClient

# Garantiza modo mock antes de importar la app.
os.environ["DATA_PROVIDER"] = "mock"

from src.api import app  # noqa: E402

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_solicitudes():
    resp = client.get("/solicitudes")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) > 0
    assert "asunto" in data[0]


def test_reuniones():
    resp = client.get("/reuniones")
    assert resp.status_code == 200
    assert len(resp.json()) > 0


def test_workitems():
    resp = client.get("/workitems")
    assert resp.status_code == 200
    assert all("proyecto" in w for w in resp.json())


def test_temas():
    resp = client.get("/temas")
    assert resp.status_code == 200
    nombres = {t["nombre"] for t in resp.json()}
    assert "Calidad de datos" in nombres


def test_resumen():
    resp = client.get("/resumen")
    assert resp.status_code == 200
    body = resp.json()
    assert body["total_solicitudes"] > 0
    assert "personas_top" in body
    assert "temas" in body
