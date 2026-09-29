"""Utilidades de red compartidas por los clientes live.

Reintentos con backoff exponencial ante cortes de red transitorios
(ConnectionResetError, TimeoutError, etc.), comunes tras proxies/firewalls
corporativos. Degrada con claridad: si tras N intentos sigue fallando, propaga
la ultima excepcion.
"""

from __future__ import annotations

import socket
import ssl
import time
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")

# Errores tipicamente transitorios que justifican un reintento.
_TRANSIENT = (
    ConnectionResetError,
    ConnectionError,
    TimeoutError,
    socket.timeout,
    ssl.SSLError,
)


def with_retries(
    fn: Callable[[], T],
    *,
    intentos: int = 3,
    espera_base: float = 1.5,
) -> T:
    """Ejecuta `fn`, reintentando ante errores de red transitorios.

    Espera espera_base, luego espera_base*2, etc. (backoff exponencial).
    """
    ultimo_error: Exception | None = None
    for i in range(intentos):
        try:
            return fn()
        except _TRANSIENT as e:
            ultimo_error = e
            if i < intentos - 1:
                time.sleep(espera_base * (2**i))
    # Se agotaron los intentos: propaga el ultimo error.
    assert ultimo_error is not None
    raise ultimo_error
