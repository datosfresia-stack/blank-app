import streamlit as st
import requests
import feedparser

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Prensaenloslagos", 
    page_icon="📰", 
    layout="wide"
)

# --- ESTILOS VISUALES (CSS) ---
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

# --- FUNCIONES DE OBTENCIÓN DE DATOS ---
def obtener_clima():
    try:
        r = requests.get("https://wttr.in/Fresia,Chile?format=%C+%t&m&lang=es", timeout=5)
        if r.status_code == 200:
            return r.text.replace("+", "").strip()
        return "Despejado 14°C"
    except:
        return "Despejado 14°C"

def traer_noticias():
    try:
        feed = feedparser.parse("https://www.biobiochile.cl/lista/tag/chile/feed")
        if feed.entries:
            return [{"titulo": e.title, "link": e.link} for e in feed.entries[:10]]
        return []
    except:
        return []

# --- CARGA INICIAL ---
clima_fresia = obtener_clima()
lista_noticias = traer_noticias()

# --- INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>📰 Prensaenloslagos</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'><b>📍 Fresia, Región de Los Lagos | {clima_fresia}</b></p>", unsafe_allow_html=True)

# MARQUESINA (SCROLL)
if lista_noticias:
    titulares = "  •  ".join([n['titulo'] for n in lista_noticias])
    st.markdown(f'<div class="ticker-wrapper"><marquee scrollamount="8">{titulares}</marquee></div>', unsafe_allow_html=True)

# PESTAÑAS
tab1, tab2, tab3, tab4 = st.tabs(["🗞️ Noticias", "🌳 Datos Fresia", "🤝 Solidario", "🤖 IA Libre"])

with tab1:
    st.subheader("Titulares Nacionales")
    if lista_noticias:
        for n in lista_noticias:
            st.markdown(f"🔹 **[{n['titulo']}]({n['link']})**")
    else:
        st.info("Actualizando noticias...")

with tab2:
    st.subheader("Datos de la Comuna")
    st.metric("Población", "12.800 hab.")
    st.write("Clima actual en Fresia:", clima_fresia)

with tab3:
    st.subheader("Centro Solidario")
    st.success("Campaña activa: Ayuda de invierno.")
    if st.button("Participar"):
        st.balloons()

with tab4:
    st.subheader("Consulta a la IA Libre")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if entrada := st.chat_input("Escribe aquí"):
        st.session_state.messages.append({"role": "user", "content": entrada})
        with st.chat_message("user"):
            st.markdown(entrada)
        
        with st.chat_message("assistant"):
            texto = f"Hola Miguel, soy Libre. En Fresia hay {clima_fresia}. ¿Cómo te ayudo?"
            st.markdown(texto)
            st.session_state.messages.append({"role": "assistant", "content": texto})

# BARRA LATERAL
with st.sidebar:
    st.header("📊 Mi Panel")
    st.divider()
    st.metric("Última Presión", "117/76")
    st.file_uploader("Subir foto pesa", type=['jpg', 'png'])
