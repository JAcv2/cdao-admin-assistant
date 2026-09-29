"""Interfaz comun para proveedores de datos."""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.models import Reunion, Solicitud, WorkItem


class DataProvider(ABC):
    """Contrato que deben cumplir MockProvider y LiveProvider.

    Todos los metodos son de SOLO LECTURA: el asistente nunca modifica correos,
    calendarios ni work items. Esto es una salvaguarda de seguridad explicita.
    """

    @abstractmethod
    def get_solicitudes(self) -> list[Solicitud]:
        """Correos que requieren seguimiento, mapeados a Solicitud."""

    @abstractmethod
    def get_reuniones(self) -> list[Reunion]:
        """Reuniones proximas del calendario."""

    @abstractmethod
    def get_workitems(self) -> list[WorkItem]:
        """Work items de Azure DevOps."""
