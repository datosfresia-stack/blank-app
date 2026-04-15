import streamlit as st
import requests
import feedparser
import random

# 1. Configuración de Identidad y Estilo Profesional
st.set_page_config(
    page_title="Prensaenloslagos", 
    page_icon="📰", 
    layout="wide"
)

# CSS Personalizado para un look de App de Noticias
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: #eee;
        border-radius: 10px 10px 0 0;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #27ae60 !important;
        color: white !important;
    }
    .news-scroll {
        background: #1a1a1a;
        color: #00ff00;
        padding: 8px;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE SENSORES Y DATOS ---

def obtener_clima_fresia():
    try:
        # Forzamos métrico (Celsius) e idioma español
        r = requests.get("https://wttr.in/Fresia,Chile?format=%C+%t&m&lang=es", timeout=5)
        if r.status_code == 200:
            return r.text.replace("+", "").replace("Â", "").strip()
    except:
        return "Parcialmente nublado 12°C"
    return "Nublado 10°C"

def traer_noticias_nacionales():
    try:
        # Feed de noticias de BioBioChile (Nacional)
        feed = feedparser.parse("https://www.biobiochile.cl/lista/tag/chile/feed")
        return [{"titulo": e.title, "link": e.link, "fecha": e.published} for e in feed.entries[:8]]
    except:
        return [{"titulo": "Servicio de noticias momentáneamente no disponible", "link": "#", "fecha": ""}]

# --- INICIO DE LA APLICACIÓN ---

clima = obtener_clima_fresia()
noticias = traer_noticias_nacionales()

# Encabezado Principal
st.markdown(f"<h1 style='text-align: center;'>📰 Prensaenloslagos</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'><b>📍 Fresia, Los Lagos | Clima: {clima}</b></p>", unsafe_allow_html=True)

# 2. Barra de Noticias en Movimiento (Ticker)
titulares_scroll = " • ".join([n['titulo'] for n in noticias])
st.markdown(f"""
    <div class="news-scroll">
        <marquee behavior="scroll" direction="left" scrollamount="7">
            {titulares_scroll}
        </marquee>
    </div>
    """, unsafe_allow_html=True)

# 3. Pestañas de Navegación
tab1, tab2, tab3, tab4 = st.tabs([
    "🗞️ Nacional", 
    "🌳 Datos Fresia", 
    "🤝 Acción Solidaria", 
    "🤖 IA Libre"
])

# --- PESTAÑA: NOTICIAS NACIONALES ---
with tab1:
    st.subheader("Últimas Noticias de Chile")
    for n in noticias:
        with st.expander(f"📌 {n['titulo']}"):
            st.write(f"Publicado el: {n['fecha']}")
            st.markdown(f"[Leer noticia completa en el portal]({n['link']})")

# --- PESTAÑA: DATOS FRESIA ---
with tab2:
    st.subheader("Información Local de Fresia")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Población", "12.800 hab.")
        st.write("**Comercio:** Ferias locales abiertas de 9:00 a 18:00.")
    with col2:
        st.metric("Temperatura", clima.split()[-1])
        st.write("**Agricultura:** Temporada de siembra activa en el sector.")
    
    st.divider()
    
