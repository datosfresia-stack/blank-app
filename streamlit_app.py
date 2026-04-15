import streamlit as st
import requests
import feedparser

# 1. CONFIGURACIÓN DE LA APP
st.set_page_config(
    page_title="Prensaenloslagos", 
    page_icon="📰", 
    layout="wide"
)

# --- ESTILOS VISUALES ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .ticker-wrapper {
        background: #000000;
        color: #3dfc03;
        padding: 12px;
        font-family: 'Courier New', monospace;
        font-size: 18px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #27ae60 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE DATOS ---
def obtener_clima():
    try:
        r = requests.get("https://wttr.in/Fresia,Chile?format=%C+%t&m&lang=es", timeout=5)
        return r.text.replace("+", "").strip() if r.status_code == 200 else "Despejado 14°C"
    except:
        return "Despejado 14°C"

def traer_noticias():
    try:
        feed = feedparser.parse("https://www.biobiochile.cl/lista/tag/chile/feed")
        return [{"titulo": e.title, "link": e.link} for e in feed.entries[:10]] if feed.entries else []
    except:
        return []

# --- CARGA DE DATOS ---
clima = obtener_clima()
noticias = traer_noticias()

# --- INTERFAZ PRINCIPAL ---
st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>📰 Prensaenloslagos</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'><b>📍 Fresia | {clima}</b></p>", unsafe_allow_html=True)

# MARQUESINA (SCROLL)
if noticias:
    titulares = "  •  ".join([n['titulo'] for n in noticias])
    st.markdown(f'<div class="ticker-wrapper"><marquee scrollamount="8">{titulares}</marquee></div>', unsafe_allow_html=True)

# PESTAÑAS
tab1, tab2, tab3, tab4 = st.tabs(["🗞️ Noticias", "🌳 Datos Fresia", "🤝 Solidario", "🤖 IA Libre"])

with tab1:
    st.subheader("Últimas Noticias")
    if noticias:
        for n in noticias:
            st.markdown(f"🔹 [{n['titulo']}]({n['link']})")
    else:
        st.info("Cargando noticias nacionales...")

with tab2:
    st.subheader("Datos de Fresia")
    st.write("Información local para la comunidad.")
    st.metric("Población Local", "12.800 hab.")

with tab3:
    st.subheader("Centro Solidario")
    st.success("Campaña: Ayuda para el invierno en la Región de Los Lagos.")
    if st.button("Unirme"):
        st.balloons()

with tab4:
    st.subheader("Consulta a Libre")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if p := st.chat_input("Escribe tu duda aquí"):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"):
            st.markdown(p)
        
        with st.chat_message("assistant"):
            # Respuesta segura sin cortes
            resp = f"Hola, soy Libre. Hoy en Fresia tenemos {clima}. ¿Cómo puedo apoyarte hoy?"
            st.markdown(resp)
            st.session_state.messages.append({"role": "assistant", "content": resp})

# BARRA LATERAL
with st.sidebar:
    st.header("⚙️ Panel de Control")
    st.write("Bienvenido, Miguel.")
    st.divider()
    st.file_uploader("Subir registro de salud", type=['jpg', 'png'])
