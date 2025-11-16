import streamlit as st
from streamlit_folium import st_folium
import folium
import requests
from datetime import datetime

st.set_page_config(layout="wide", page_title="Inundaciones Tláhuac")

# ========== ESTILOS PERSONALIZADOS ==========
st.markdown("""
    <style>
    .main { background-color: #0b1e31; }
    .title { color: white; font-size: 32px; font-weight: bold; }
    .subtitle { color: #a9c4df; font-size: 18px; }
    .white { color: white; }
    .card {
        background-color: #132b45;
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin-bottom: 10px;
    }
    .alert-red {
        background-color: #6e1b1b;
        color: white;
        padding: 8px;
        border-radius: 5px;
    }
    .alert-green {
        background-color: #1b6e2d;
        color: white;
        padding: 8px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# ========== PANEL SUPERIOR ==========
st.markdown('<p class="title">Alcaldía Tláhuac – Sistema de Monitoreo de Inundaciones</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Predicción 24h • Mapa interactivo • Reporte ciudadano</p>', unsafe_allow_html=True)
st.markdown("---")

# ========== LAYOUT PRINCIPAL ==========
col1, col2, col3 = st.columns([1.1, 2.8, 1.1])

# -----------------------------------------
# ========== COL1 – PANEL DE PREDICCIONES ==========
# -----------------------------------------
with col1:
    st.markdown('<div class="card"><h3>Probabilidad de Inundación (24h)</h3></div>', unsafe_allow_html=True)

    zonas = {
        "San Pedro Tláhuac": 0.89,
        "San Pedro Mixquic": 0.59,
        "Santa Catarina": 0.90,
        "Santiago Zacahuizco": 0.59,
        "La Logasca": 0.96
    }

    for zona, prob in zonas.items():
        color = "alert-red" if prob > 0.70 else "alert-green"
        st.markdown(f"""
            <div class="card">
                <b>{zona}</b><br>
                <div class="{color}">Probabilidad: {int(prob*100)}%</div>
            </div>
        """, unsafe_allow_html=True)

    # Indicador circular
    st.markdown("""
        <div class="card" style="text-align:center;">
            <h2>89%</h2>
            <p>Promedio de Precipitación</p>
        </div>
    """, unsafe_allow_html=True)

# -----------------------------------------
# ========== COL2 – MAPA INTERACTIVO ==========
# -----------------------------------------
with col2:
    st.markdown('<div class="card"><h3>Mapa Interactivo de Inundaciones</h3></div>', unsafe_allow_html=True)

    # Coordenadas de Tláhuac
    mapa = folium.Map(location=[19.284, -99.002], zoom_start=12)

    # Zonas afectadas
    coordenadas = {
        "San Pedro Tláhuac": [19.284, -99.008],
        "Mixquic": [19.205, -98.975],
        "Santa Catarina": [19.289, -99.015],
        "Santiago Zacahuizco": [19.300, -99.005],
    }

    for zona, coord in coordenadas.items():
        folium.Marker(
            location=coord,
            popup=f"Zona: {zona}",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(mapa)

    st_folium(mapa, height=520, width=900)

# -----------------------------------------
# ========== COL3 – REPORTE CIUDADANO ==========
# -----------------------------------------
with col3:
    st.markdown('<div class="card"><h3>Generar Reporte Ciudadano</h3></div>', unsafe_allow_html=True)

    nombre = st.text_input("Nombre")
    calle = st.text_input("Calle y número")
    descripcion = st.text_area("Descripción del incidente")
    foto = st.file_uploader("Foto/Video del incidente")

    if st.button("Enviar Reporte"):
        st.success("Reporte enviado exitosamente.")
        st.write("📌 **Datos del reporte:**")
        st.write(f"👤 **Nombre:** {nombre}")
        st.write(f"📍 **Dirección:** {calle}")
        st.write(f"📝 **Descripción:** {descripcion}")
        if foto:
            st.image(foto, width=250)

    st.markdown('<div class="card" style="text-align:center;"><i>Historial de Reportes</i></div>', unsafe_allow_html=True)
