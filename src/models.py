"""Modelos de dominio del CDAO Assistant.

Estos modelos son la lingua franca entre las fuentes de datos (Gmail, Calendar,
Azure DevOps) y los consumidores (API, dashboard, clustering, MCP). Cualquier
proveedor de datos (mock o live) debe mapear su fuente a estos modelos.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class Prioridad(str, Enum):
    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"


class EstadoWorkItem(str, Enum):
    NUEVO = "nuevo"
    ACTIVO = "activo"
    RESUELTO = "resuelto"
    CERRADO = "cerrado"


class Persona(BaseModel):
    """Una persona relevante para la gestion: solicitante, asistente, asignado."""

    nombre: str
    email: str
    rol: str | None = None


class Solicitud(BaseModel):
    """Solicitud derivada de un correo (Gmail) que requiere seguimiento."""

    id: str
    asunto: str
    resumen: str = ""
    remitente: Persona
    fecha: datetime
    prioridad: Prioridad = Prioridad.MEDIA
    etiquetas: list[str] = Field(default_factory=list)
    proyecto: str | None = None


class Reunion(BaseModel):
    """Reunion agendada (Google Calendar)."""

    id: str
    titulo: str
    inicio: datetime
    fin: datetime
    organizador: Persona
    asistentes: list[Persona] = Field(default_factory=list)
    etiquetas: list[str] = Field(default_factory=list)
    proyecto: str | None = None


class WorkItem(BaseModel):
    """Tarea/work item de Azure DevOps."""

    id: str
    titulo: str
    estado: EstadoWorkItem = EstadoWorkItem.NUEVO
    asignado: Persona | None = None
    proyecto: str
    prioridad: Prioridad = Prioridad.MEDIA
    etiquetas: list[str] = Field(default_factory=list)
    url: str | None = None


class ItemSeguimiento(BaseModel):
    """Representacion unificada de cualquier item para el motor de clustering.

    Solicitudes, reuniones y work items se normalizan a esta forma comun para
    poder agruparlos por tema/proyecto/persona de manera homogenea.
    """

    id: str
    tipo: str  # "solicitud" | "reunion" | "workitem"
    titulo: str
    persona_email: str
    proyecto: str | None = None
    etiquetas: list[str] = Field(default_factory=list)
    texto: str = ""  # texto libre para matching por keywords


class Tema(BaseModel):
    """Grupo de items relacionados producido por el motor de clustering."""

    nombre: str
    items: list[ItemSeguimiento] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.items)


class ResumenGestion(BaseModel):
    """Resumen ejecutivo para el dashboard del CDAO."""

    total_solicitudes: int
    total_reuniones: int
    total_workitems: int
    temas: list[Tema] = Field(default_factory=list)
    personas_top: dict[str, int] = Field(default_factory=dict)
    generado_en: datetime
