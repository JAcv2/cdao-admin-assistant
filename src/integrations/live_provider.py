"""LiveProvider: datos reales de Google Workspace + Azure DevOps.

Reusa los clientes `google_client` y `azure_client`. Los imports de esos modulos
(y sus SDKs) son perezosos: solo se cargan al construir el provider en modo live,
para que el modo mock no requiera credenciales ni paquetes de Google/Azure.

Todas las operaciones son de solo lectura.
"""

from __future__ import annotations

from src.integrations.base import DataProvider
from src.models import Reunion, Solicitud, WorkItem


class LiveProvider(DataProvider):
    def get_solicitudes(self) -> list[Solicitud]:
        from src.integrations import google_client

        return google_client.fetch_solicitudes()

    def get_reuniones(self) -> list[Reunion]:
        from src.integrations import google_client

        return google_client.fetch_reuniones()

    def get_workitems(self) -> list[WorkItem]:
        from src.integrations import azure_client

        return azure_client.fetch_workitems()
