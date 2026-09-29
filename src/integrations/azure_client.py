"""Cliente de Azure DevOps (work items) de SOLO LECTURA.

Usa un PAT (Personal Access Token) con permisos minimos de lectura (Work Items - Read)
y la REST API con una consulta WIQL. El PAT se lee de la variable AZDO_PAT y nunca se
registra en logs.
"""

from __future__ import annotations

import base64
import os

import requests

from src.integrations.net import with_retries
from src.models import EstadoWorkItem, Persona, Prioridad, WorkItem

_TIMEOUT = 20

_WIQL = (
    "SELECT [System.Id] FROM WorkItems "
    "WHERE [System.TeamProject] = @project "
    "ORDER BY [System.ChangedDate] DESC"
)


def _config() -> tuple[str, str, str]:
    org_url = os.getenv("AZDO_ORG_URL", "").rstrip("/")
    project = os.getenv("AZDO_PROJECT", "")
    pat = os.getenv("AZDO_PAT", "")
    if not (org_url and project and pat):
        raise RuntimeError(
            "Faltan variables de Azure DevOps. Define AZDO_ORG_URL, AZDO_PROJECT y "
            "AZDO_PAT en tu .env (PAT con permiso Work Items - Read)."
        )
    return org_url, project, pat


def _auth_header(pat: str) -> dict[str, str]:
    token = base64.b64encode(f":{pat}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


def _map_estado(raw: str) -> EstadoWorkItem:
    mapa = {
        "New": EstadoWorkItem.NUEVO,
        "Active": EstadoWorkItem.ACTIVO,
        "Resolved": EstadoWorkItem.RESUELTO,
        "Closed": EstadoWorkItem.CERRADO,
        "Done": EstadoWorkItem.CERRADO,
    }
    return mapa.get(raw, EstadoWorkItem.NUEVO)


def _map_prioridad(raw) -> Prioridad:
    try:
        n = int(raw)
    except (TypeError, ValueError):
        return Prioridad.MEDIA
    if n <= 1:
        return Prioridad.ALTA
    if n == 2:
        return Prioridad.MEDIA
    return Prioridad.BAJA


def fetch_workitems(max_results: int | None = None) -> list[WorkItem]:
    """Consulta work items del proyecto configurado y los mapea a WorkItem."""
    max_results = max_results or int(os.getenv("AZDO_MAX_RESULTS", "50"))
    org_url, project, pat = _config()
    headers = _auth_header(pat)

    # 1) WIQL: obtener ids.
    wiql_url = f"{org_url}/{project}/_apis/wit/wiql?api-version=7.0"
    resp = with_retries(
        lambda: requests.post(wiql_url, json={"query": _WIQL}, headers=headers, timeout=_TIMEOUT)
    )
    resp.raise_for_status()
    ids = [w["id"] for w in resp.json().get("workItems", [])][:max_results]
    if not ids:
        return []

    # 2) Detalle de los work items.
    fields = ",".join(
        [
            "System.Title",
            "System.State",
            "System.AssignedTo",
            "System.TeamProject",
            "Microsoft.VSTS.Common.Priority",
            "System.Tags",
        ]
    )
    detail_url = (
        f"{org_url}/_apis/wit/workitems?ids={','.join(map(str, ids))}"
        f"&fields={fields}&api-version=7.0"
    )
    detail = with_retries(lambda: requests.get(detail_url, headers=headers, timeout=_TIMEOUT))
    detail.raise_for_status()

    items: list[WorkItem] = []
    for wi in detail.json().get("value", []):
        f = wi.get("fields", {})
        asignado = None
        raw_asignado = f.get("System.AssignedTo")
        if isinstance(raw_asignado, dict):
            asignado = Persona(
                nombre=raw_asignado.get("displayName", ""),
                email=raw_asignado.get("uniqueName", ""),
            )
        tags = f.get("System.Tags", "")
        etiquetas = [t.strip() for t in tags.split(";") if t.strip()] if tags else []
        items.append(
            WorkItem(
                id=str(wi.get("id")),
                titulo=f.get("System.Title", ""),
                estado=_map_estado(f.get("System.State", "New")),
                asignado=asignado,
                proyecto=f.get("System.TeamProject", project),
                prioridad=_map_prioridad(f.get("Microsoft.VSTS.Common.Priority")),
                etiquetas=etiquetas,
                url=wi.get("url"),
            )
        )
    return items
