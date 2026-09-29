"""API REST del CDAO Assistant (FastAPI).

Expone las fuentes consolidadas y el resultado del clustering. Todos los endpoints
son de solo lectura. El provider se selecciona por la variable DATA_PROVIDER
(mock por defecto).
"""

from __future__ import annotations

from fastapi import FastAPI

from src.clustering import cluster_items, normalizar, resumir
from src.integrations import get_provider
from src.models import ResumenGestion, Reunion, Solicitud, Tema, WorkItem

app = FastAPI(
    title="CDAO Admin Assistant",
    description="Consolida correos, reuniones y work items con clustering de temas.",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/solicitudes", response_model=list[Solicitud])
def get_solicitudes() -> list[Solicitud]:
    return get_provider().get_solicitudes()


@app.get("/reuniones", response_model=list[Reunion])
def get_reuniones() -> list[Reunion]:
    return get_provider().get_reuniones()


@app.get("/workitems", response_model=list[WorkItem])
def get_workitems() -> list[WorkItem]:
    return get_provider().get_workitems()


@app.get("/temas", response_model=list[Tema])
def get_temas() -> list[Tema]:
    provider = get_provider()
    items = normalizar(
        provider.get_solicitudes(),
        provider.get_reuniones(),
        provider.get_workitems(),
    )
    return cluster_items(items)


@app.get("/resumen", response_model=ResumenGestion)
def get_resumen() -> ResumenGestion:
    provider = get_provider()
    return resumir(
        provider.get_solicitudes(),
        provider.get_reuniones(),
        provider.get_workitems(),
    )
