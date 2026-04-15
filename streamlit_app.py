import streamlit as st
import requests
import feedparser
import random

# Configuración
st.set_page_config(page_title="Prensaenloslagos", page_icon="📰", layout="wide")

# Funciones de Datos
def obtener_clima():
    try:
        r = requests.get("https://wttr.in/Fresia,Chile?format=%C+%t&m&lang=es", timeout=5)
        return r.text.replace("+", "").replace("Â", "").strip()
    except: return "Despejado 12°C"

def traer_noticias():
    try:
        feed = feedparser.parse("https://www.biobiochile.cl/lista/tag/chile/feed")
        return [{"titulo": e.title, "link": e.link} for e in feed.entries[:8]]
    except: return []

# Carga de datos
clima = obtener_clima()
noticias = traer_noticias()

# Diseño
st.markdown(f"<h1 style='text-align: center;'>📰 Prensaenloslagos</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>📍 Fresia | Clima: {clima}</p>", unsafe_allow_html=True)

# --- ARREGLO DE LA MARQUESINA ---
if noticias:
    titulares = "  •  ".join([n['titulo'] for n in noticias])
    st.markdown(f"""
        <div style="background: #000; color: #0f0; padding: 10px; font-family: monospace;">
            <marquee scrollamount="7">{titulares}</marquee>
        </div>
    """, unsafe_allow_html=True)

# Pestañas
t1, t2, t3, t4 = st.tabs(["🗞️ Nacional", "🌳 Datos Fresia", "🤝 Solidaria", "🤖 IA Libre"])

with t1:
    st.subheader("Últimas Noticias de Chile")
    if not noticias:
        st.warning("Cargando noticias... Asegúrate de tener 'feedparser' en requirements.txt")
    for n in noticias:
        st.markdown(f"🔹 [{n['titulo']}]({n['link']})")

# ... (El resto de las pestañas se mantienen igual)
