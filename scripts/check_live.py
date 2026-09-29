"""Verificacion de conexiones live (Google + Azure DevOps).

Uso:
    python scripts/check_live.py            # verifica ambos
    python scripts/check_live.py google     # solo Google
    python scripts/check_live.py azure      # solo Azure DevOps

No imprime datos sensibles: solo confirma conexion y cuenta items. Los correos, si
aparecen, salen redactados. Lee credenciales de tu .env local.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Cargar .env si python-dotenv esta disponible.
try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
except ImportError:
    pass

# Permite importar `src` al ejecutar el script directamente.
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


def check_google() -> bool:
    print("== Google Workspace (Gmail + Calendar) ==")
    try:
        from src.integrations import google_client

        print("  Abriendo flujo OAuth (se abrira el navegador la primera vez)...")
        solicitudes = google_client.fetch_solicitudes(max_results=5)
        reuniones = google_client.fetch_reuniones(max_results=5)
        print(f"  OK Gmail: {len(solicitudes)} correo(s) leidos.")
        print(f"  OK Calendar: {len(reuniones)} reunion(es) leidas.")
        return True
    except FileNotFoundError as e:
        print(f"  FALTA credencial: {e}")
    except Exception as e:  # noqa: BLE001
        print(f"  ERROR Google: {type(e).__name__}: {e}")
    return False


def check_azure() -> bool:
    print("== Azure DevOps (work items) ==")
    try:
        from src.integrations import azure_client

        items = azure_client.fetch_workitems(max_results=5)
        print(f"  OK Azure DevOps: {len(items)} work item(s) leidos.")
        return True
    except RuntimeError as e:
        print(f"  CONFIG incompleta: {e}")
    except Exception as e:  # noqa: BLE001
        print(f"  ERROR Azure: {type(e).__name__}: {e}")
    return False


def main() -> int:
    target = sys.argv[1].lower() if len(sys.argv) > 1 else "both"
    ok = True
    if target in ("both", "google"):
        ok = check_google() and ok
    if target in ("both", "azure"):
        ok = check_azure() and ok
    print("\nResultado:", "TODO OK" if ok else "hubo fallos (revisa arriba)")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
