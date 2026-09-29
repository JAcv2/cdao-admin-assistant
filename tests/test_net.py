"""Tests del helper de reintentos de red."""

from __future__ import annotations

import pytest

from src.integrations.net import with_retries


def test_devuelve_resultado_sin_error():
    assert with_retries(lambda: 42) == 42


def test_reintenta_y_luego_tiene_exito():
    intentos = {"n": 0}

    def flaky():
        intentos["n"] += 1
        if intentos["n"] < 3:
            raise ConnectionResetError("corte transitorio")
        return "ok"

    # espera_base baja para que el test sea rapido
    assert with_retries(flaky, intentos=3, espera_base=0.01) == "ok"
    assert intentos["n"] == 3


def test_propaga_tras_agotar_intentos():
    def siempre_falla():
        raise TimeoutError("sin red")

    with pytest.raises(TimeoutError):
        with_retries(siempre_falla, intentos=2, espera_base=0.01)


def test_no_reintenta_errores_no_transitorios():
    intentos = {"n": 0}

    def error_de_valor():
        intentos["n"] += 1
        raise ValueError("bug real")

    with pytest.raises(ValueError):
        with_retries(error_de_valor, intentos=3, espera_base=0.01)
    assert intentos["n"] == 1  # no reintenta
