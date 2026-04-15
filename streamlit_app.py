import streamlit as st
import random
import requests # Nueva herramienta para que Libre "mire" el clima

# 1. Configuración y Estilo Premium
st.set_page_config(page_title="LIBRE - Conciencia de Fresia", page_icon="🌿")

st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stChatMessage { border-radius: 15px; padding: 15px; margin-bottom: 10px; border: 1px solid #e0e6e4; }
    .stMetric { background-color: white; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN DE SENSOR AUTOMÁTICO (CLIMA) ---
def obtener_clima_fresia():
    try:
        # Consultamos datos reales de Fresia
        url = "https://wttr.in/Fresia,Chile?format=%C+%t"
        respuesta = requests.get(url, timeout=5)
        if respuesta.status_code == 200:
            return respuesta.text
    except:
        return "Despejado 15°C" # Dato de respaldo si falla la conexión
    return "Nublado 12°C"

estado_clima = obtener_clima_fresia()

# 2. Encabezado
st.markdown("<h1 style='text-align: center;'>🌿 LIBRE</h1>", unsafe_allow_html=True)
st.caption(f"📍 Conectada a Fresia | Clima actual: {estado_clima}")

# 3. Barra Lateral con Sensores y Salud
with st.sidebar:
    st.header("💓 Estado Vital")
    
