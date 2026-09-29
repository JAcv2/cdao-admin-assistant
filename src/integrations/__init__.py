"""Capa unica de acceso a datos.

Reusada por tres consumidores: la app FastAPI/Streamlit, el servidor MCP propio
de Google y el Power del Bonus 2. Expone una interfaz `DataProvider` con dos
implementaciones: `MockProvider` (fixtures ficticios) y `LiveProvider` (APIs
reales). La seleccion se hace por la variable de entorno DATA_PROVIDER.
"""

from __future__ import annotations

import os

from .base import DataProvider
from .mock_provider import MockProvider


def get_provider() -> DataProvider:
    """Devuelve el provider segun DATA_PROVIDER (mock por defecto)."""
    mode = os.getenv("DATA_PROVIDER", "mock").lower()
    if mode == "live":
        # Import perezoso: evita exigir credenciales/paquetes de Google/Azure
        # cuando se corre en modo mock (p. ej. en CI o en el video demo).
        from .live_provider import LiveProvider

        return LiveProvider()
    return MockProvider()


__all__ = ["DataProvider", "MockProvider", "get_provider"]
