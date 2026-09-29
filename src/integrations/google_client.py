"""Cliente de Google Workspace (Gmail + Calendar) de SOLO LECTURA.

Usa OAuth de usuario instalado (InstalledAppFlow). Los scopes son de solo lectura,
de modo que el asistente nunca puede modificar correos ni eventos.

Los imports de los SDKs de Google son perezosos: este modulo solo se importa cuando
DATA_PROVIDER=live, para no exigir las dependencias en modo mock/CI.
"""

from __future__ import annotations

import base64
import os
from datetime import datetime, timezone
from pathlib import Path

from src.integrations.net import with_retries
from src.models import Persona, Reunion, Solicitud

# Scopes de SOLO LECTURA (minimo privilegio).
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar.readonly",
]


def _load_credentials():
    """Obtiene credenciales OAuth, refrescando o iniciando el flujo si hace falta.

    - client_secret: ruta en GOOGLE_CLIENT_SECRET_FILE.
    - token cacheado: ruta en GOOGLE_TOKEN_FILE (gitignored).
    """
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    token_file = Path(os.getenv("GOOGLE_TOKEN_FILE", "./token.json"))
    secret_file = Path(os.getenv("GOOGLE_CLIENT_SECRET_FILE", "./client_secret.json"))

    creds = None
    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not secret_file.exists():
                raise FileNotFoundError(
                    f"No se encontro el client secret en {secret_file}. "
                    "Descargalo desde Google Cloud Console y define "
                    "GOOGLE_CLIENT_SECRET_FILE en tu .env."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(secret_file), SCOPES)
            creds = flow.run_local_server(port=0)
        token_file.write_text(creds.to_json(), encoding="utf-8")

    return creds


def _service(api: str, version: str):
    from googleapiclient.discovery import build

    return build(api, version, credentials=_load_credentials(), cache_discovery=False)


def _parse_persona(raw: str) -> Persona:
    """Convierte 'Nombre <correo@dominio>' o 'correo@dominio' en Persona."""
    raw = (raw or "").strip()
    if "<" in raw and ">" in raw:
        nombre = raw.split("<")[0].strip().strip('"')
        email = raw.split("<")[1].split(">")[0].strip()
    else:
        nombre = raw
        email = raw
    return Persona(nombre=nombre or email, email=email)


def fetch_solicitudes(max_results: int | None = None) -> list[Solicitud]:
    """Lee correos recientes de Gmail y los mapea a Solicitud."""
    max_results = max_results or int(os.getenv("GMAIL_MAX_RESULTS", "25"))
    service = _service("gmail", "v1")

    listing = with_retries(
        lambda: service.users()
        .messages()
        .list(userId="me", maxResults=max_results, labelIds=["INBOX"])
        .execute()
    )
    solicitudes: list[Solicitud] = []
    for meta in listing.get("messages", []):
        mensaje_id = meta["id"]
        msg = with_retries(
            lambda mid=mensaje_id: service.users()
            .messages()
            .get(
                userId="me",
                id=mid,
                format="metadata",
                metadataHeaders=["Subject", "From", "Date"],
            )
            .execute()
        )
        headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
        remitente = _parse_persona(headers.get("From", "desconocido"))
        fecha = _epoch_ms_to_dt(msg.get("internalDate"))
        solicitudes.append(
            Solicitud(
                id=meta["id"],
                asunto=headers.get("Subject", "(sin asunto)"),
                resumen=msg.get("snippet", ""),
                remitente=remitente,
                fecha=fecha,
            )
        )
    return solicitudes


def fetch_reuniones(max_results: int | None = None) -> list[Reunion]:
    """Lee proximos eventos de Google Calendar y los mapea a Reunion."""
    max_results = max_results or int(os.getenv("CALENDAR_MAX_RESULTS", "25"))
    service = _service("calendar", "v3")

    ahora = datetime.now(timezone.utc).isoformat()
    eventos = with_retries(
        lambda: service.events()
        .list(
            calendarId="primary",
            timeMin=ahora,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    reuniones: list[Reunion] = []
    for ev in eventos.get("items", []):
        inicio = _parse_event_dt(ev.get("start", {}))
        fin = _parse_event_dt(ev.get("end", {}))
        organizador = _parse_persona(ev.get("organizer", {}).get("email", "desconocido"))
        asistentes = [
            _parse_persona(a.get("email", "")) for a in ev.get("attendees", []) if a.get("email")
        ]
        reuniones.append(
            Reunion(
                id=ev.get("id", ""),
                titulo=ev.get("summary", "(sin titulo)"),
                inicio=inicio,
                fin=fin,
                organizador=organizador,
                asistentes=asistentes,
            )
        )
    return reuniones


def _epoch_ms_to_dt(value: str | None) -> datetime:
    if not value:
        return datetime.now(timezone.utc)
    return datetime.fromtimestamp(int(value) / 1000, tz=timezone.utc)


def _parse_event_dt(node: dict) -> datetime:
    raw = node.get("dateTime") or node.get("date")
    if not raw:
        return datetime.now(timezone.utc)
    # 'date' (all-day) viene como YYYY-MM-DD
    if len(raw) == 10:
        return datetime.fromisoformat(raw + "T00:00:00+00:00")
    return datetime.fromisoformat(raw.replace("Z", "+00:00"))


# Base64 helper conservado por si se requiere leer cuerpos completos mas adelante.
def _decode_body(data: str) -> str:
    return base64.urlsafe_b64decode(data.encode("utf-8")).decode("utf-8", errors="replace")
