"""MockProvider: carga datos ficticios desde data/fixtures/.

Se usa por defecto y para grabar el video demo, de modo que la demostracion no
dependa de tokens vivos ni exponga informacion corporativa real.
"""

from __future__ import annotations

import json
from pathlib import Path

from src.integrations.base import DataProvider
from src.models import Reunion, Solicitud, WorkItem

_FIXTURES_DIR = Path(__file__).resolve().parents[2] / "data" / "fixtures"


def _load(name: str) -> list[dict]:
    path = _FIXTURES_DIR / name
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


class MockProvider(DataProvider):
    """Proveedor de datos basado en fixtures JSON ficticios."""

    def __init__(self, fixtures_dir: Path | None = None) -> None:
        self._dir = fixtures_dir or _FIXTURES_DIR

    def _read(self, name: str) -> list[dict]:
        path = self._dir / name
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)

    def get_solicitudes(self) -> list[Solicitud]:
        return [Solicitud(**row) for row in self._read("solicitudes.json")]

    def get_reuniones(self) -> list[Reunion]:
        return [Reunion(**row) for row in self._read("reuniones.json")]

    def get_workitems(self) -> list[WorkItem]:
        return [WorkItem(**row) for row in self._read("workitems.json")]
