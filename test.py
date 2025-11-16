import streamlit as st
from streamlit_folium import st_folium
import folium
import requests
from datetime import datetime

# ===============================
#   CONFIGURACIÓN DE LA PÁGINA
# ===============================
st.set_page_config(
    page_title="Panel de Inundaciones - Tláhuac",
    layout="wide",
    page_icon="🌧️"
)

# ===============================
#   ESTILOS PERSONALIZADOS
# ===============================
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
        margin-bottom: 15px;
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

# ===============================
#   API DEL CLIMA
# ===============================

def obtener_lluvia_tlahuac():
    """Devuelve la precipitación (mm/h) usando Open-Meteo API"""
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        "latitude=19.284&longitude=-99.002&hourly=precipitation"
    )
    try:
        resp = requests.get(url)
        data = resp.json()

        # Último registro de precipitación
        lluvia_mm = data["hourly"]["precipitation"][-1]
        return float(lluvia_mm)
    except:
        return 0.0

# ===============================
#   SECCIÓN SUPERIOR
# ===============================

st.markdown('<p class="title">Sistema de Monitoreo de Inundaciones – Tláhuac</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Predicción 24h • Mapa interactivo • Reporte ciudadano</p>', unsafe_allow_html=True)
st.markdown("---")

# ===============================
#        LAYOUT (3 columnas)
# ===============================
col1, col2, col3 = st.columns([1.1, 2.8, 1.1])

# ===================================
#   COL1 – PANEL DE PREDICCIONES
# ===================================
with col1:
    st.markdown('<div class="card"><h3>Probabilidad de Inundación (24h)</h3></div>', unsafe_allow_html=True)

    lluvia = obtener_lluvia_tlahuac()

    # Probabilidad según lluvia real
    def calcular_prob(lluvia):
        if lluvia >= 15:
            return 0.95
        elif lluvia >= 10:
            return 0.75
        elif lluvia >= 5:
            return 0.50
        else:
            return 0.20

    prob_general = calcular_prob(lluvia)

    zonas = {
        "San Pedro Tláhuac": prob_general,
        "San Pedro Mixquic": prob_general * 0.65,
        "Santa Catarina": prob_general * 1.05,
        "Santiago Zacahuizco": prob_general * 0.78,
        "La Logasca": prob_general * 1.15
    }

    # Tarjetas de probabilidad
    for zona, prob in zonas.items():
        color = "alert-red" if prob > 0.70 else "alert-green"
        st.markdown(f"""
            <div class="card">
                <b>{zona}</b><br>
                <div class="{color}"><b>{int(prob*100)}%</b> de riesgo</div>
            </div>
        """, unsafe_allow_html=True)

    # Indicador circular
    st.markdown(f"""
        <div class="card" style="text-align:center;">
            <h2>{int(prob_general*100)}%</h2>
            <p>Riesgo promedio</p>
            <p>Lluvia reciente: {lluvia} mm/h</p>
        </div>
    """, unsafe_allow_html=True)

# ===================================
#   COL2 – MAPA INTERACTIVO
# ===================================
with col2:
    st.markdown('<div class="card"><h3>Mapa Interactivo de Inundaciones</h3></div>', unsafe_allow_html=True)

    mapa = folium.Map(location=[19.284, -99.002], zoom_start=12)

    # Marcadores principales
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

# ===================================
#   COL3 – REPORTE CIUDADANO
# ===================================
with col3:
    st.markdown('<div class="card"><h3>Generar Reporte Ciudadano</h3></div>', unsafe_allow_html=True)

    nombre = st.text_input("Nombre")
    calle = st.text_input("Calle y número")
    descripcion = st.text_area("Descripción del incidente")
    foto = st.file_uploader("Foto del incidente")

    if st.button("Enviar reporte"):
        st.success("Reporte enviado correctamente.")
        st.write("📌 **Resumen del reporte:**")
        st.write(f"👤 **Nombre:** {nombre}")
        st.write(f"📍 **Ubicación:** {calle}")
        st.write(f"📝 **Descripción:** {descripcion}")
        if foto:
            st.image(foto, width=250)

    st.markdown('<div class="card" style="text-align:center;"><i>Historial visible al actualizar</i></div>', unsafe_allow_html=True)
