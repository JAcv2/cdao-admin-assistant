"""Utilidades de seguridad: redaccion/anonimizacion de PII.

Se usa antes de escribir a logs o de persistir salidas del clustering, para que
informacion corporativa (correos, nombres) no quede expuesta en disco ni en el
repositorio publico.
"""

from __future__ import annotations

import os
import re

_EMAIL_RE = re.compile(r"([A-Za-z0-9._%+-])[A-Za-z0-9._%+-]*(@[A-Za-z0-9.-]+\.[A-Za-z]{2,})")


def redaction_enabled() -> bool:
    """La redaccion esta activa salvo que REDACT_PII este explicitamente en 'false'."""
    return os.getenv("REDACT_PII", "true").lower() != "false"


def redact_email(email: str) -> str:
    """Enmascara el local-part de un correo: 'ana.perez@corp.com' -> 'a***@corp.com'."""

    def _mask(match: re.Match[str]) -> str:
        first = match.group(1)
        domain = match.group(2)
        return f"{first}***{domain}"

    return _EMAIL_RE.sub(_mask, email)


def redact_text(text: str) -> str:
    """Redacta todos los correos encontrados en un texto libre."""
    return _EMAIL_RE.sub(lambda m: f"{m.group(1)}***{m.group(2)}", text)


def safe(value: str) -> str:
    """Aplica redaccion solo si esta habilitada; util para logging."""
    return redact_text(value) if redaction_enabled() else value
