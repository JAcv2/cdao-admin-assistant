"""Tests de mapeo del cliente Azure DevOps (sin red ni credenciales).

Se prueban las funciones puras de mapeo de estado/prioridad y la cabecera de auth.
"""

from __future__ import annotations

import base64

from src.integrations import azure_client
from src.models import EstadoWorkItem, Prioridad


def test_map_estado_conocidos():
    assert azure_client._map_estado("New") == EstadoWorkItem.NUEVO
    assert azure_client._map_estado("Active") == EstadoWorkItem.ACTIVO
    assert azure_client._map_estado("Resolved") == EstadoWorkItem.RESUELTO
    assert azure_client._map_estado("Closed") == EstadoWorkItem.CERRADO


def test_map_estado_desconocido_va_a_nuevo():
    assert azure_client._map_estado("Cualquiera") == EstadoWorkItem.NUEVO


def test_map_prioridad():
    assert azure_client._map_prioridad(1) == Prioridad.ALTA
    assert azure_client._map_prioridad(2) == Prioridad.MEDIA
    assert azure_client._map_prioridad(4) == Prioridad.BAJA
    assert azure_client._map_prioridad(None) == Prioridad.MEDIA


def test_auth_header_usa_basic_con_pat():
    header = azure_client._auth_header("secretpat")
    assert header["Authorization"].startswith("Basic ")
    decoded = base64.b64decode(header["Authorization"].split(" ")[1]).decode()
    assert decoded == ":secretpat"
