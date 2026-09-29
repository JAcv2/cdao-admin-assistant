"""Dashboard de seguimiento del CDAO (Streamlit).

Consume la capa de datos directamente (mismo provider que la API) y presenta:
- Tarjetas de totales
- Ranking de personas con mas items
- Temas agrupados por el motor de clustering
- Filtro por proyecto

Ejecutar: `streamlit run src/dashboard.py`
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.clustering import cluster_items, normalizar, resumir
from src.integrations import get_provider
from src.security import redact_email, redaction_enabled


def _cargar():
    provider = get_provider()
    solicitudes = provider.get_solicitudes()
    reuniones = provider.get_reuniones()
    workitems = provider.get_workitems()
    return solicitudes, reuniones, workitems


def _fmt_email(email: str) -> str:
    return redact_email(email) if redaction_enabled() else email


def main() -> None:
    st.set_page_config(page_title="CDAO Admin Assistant", layout="wide")
    st.title("CDAO Admin Assistant")
    st.caption(
        "Seguimiento consolidado de solicitudes (Gmail), reuniones (Calendar) y "
        "work items (Azure DevOps)."
    )

    solicitudes, reuniones, workitems = _cargar()
    resumen = resumir(solicitudes, reuniones, workitems)
    items = normalizar(solicitudes, reuniones, workitems)
    temas = cluster_items(items)

    # --- Filtro por proyecto ---
    proyectos = sorted({it.proyecto for it in items if it.proyecto})
    seleccion = st.sidebar.multiselect("Filtrar por proyecto", proyectos, default=proyectos)
    if seleccion:
        items = [it for it in items if it.proyecto in seleccion or it.proyecto is None]
        temas = cluster_items(items)

    # --- Tarjetas de totales ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Solicitudes", resumen.total_solicitudes)
    c2.metric("Reuniones", resumen.total_reuniones)
    c3.metric("Work items", resumen.total_workitems)

    # --- Temas ---
    st.subheader("Temas (agrupacion por reglas)")
    for tema in temas:
        with st.expander(f"{tema.nombre}  -  {tema.total} item(s)"):
            filas = [
                {
                    "tipo": it.tipo,
                    "titulo": it.titulo,
                    "persona": _fmt_email(it.persona_email),
                    "proyecto": it.proyecto or "-",
                }
                for it in tema.items
            ]
            if filas:
                st.dataframe(pd.DataFrame(filas), use_container_width=True, hide_index=True)

    # --- Personas top ---
    st.subheader("Personas con mas items")
    if resumen.personas_top:
        df_personas = pd.DataFrame(
            [
                {"persona": _fmt_email(email), "items": n}
                for email, n in resumen.personas_top.items()
            ]
        )
        st.bar_chart(df_personas.set_index("persona"))

    st.sidebar.info(
        "Modo de datos: usa la variable DATA_PROVIDER (mock por defecto). "
        "La redaccion de correos esta " + ("activa." if redaction_enabled() else "inactiva.")
    )


if __name__ == "__main__":
    main()
