import streamlit as st
import requests
import feedparser

# 1. Configuración de la App
st.set_page_config(
    page_title="Prensaenloslagos", 
    page_icon="📰", 
    layout="wide"
)

# --- ESTILOS PROFESIONALES ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #ffffff;
        border-radius: 10px 10px 0 0;
        font-weight: bold;
        border: 1px solid #ddd;
    }
    .stTabs [aria-selected="true"] {
        background-color: #27ae60 !important;
        color: white !important;
    }
    .ticker-wrapper {
        background: #000000;
        color: #3dfc03;
        padding: 10px;
        font-family: 'Courier New', monospace;
        font-size: 18px;
        border-radius: 5px;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE DATOS ---
def obtener_clima_fresia():
    try:
        # Consultamos el clima real de Fresia
        r = requests.get("https://wttr.in/Fresia,Chile?format=%C+%t&m&lang=es", timeout=5)
        if r.status_code == 200:
            return r.text.replace("+", "").replace("Â", "").strip()
    except:
        return "Despejado 14°C"
    return "Nublado 12°C"

def traer_noticias_nacionales():
    try:
        # Leemos el feed de BioBioChile
        feed = feedparser.parse("https://www.biobiochile.cl/lista/tag/chile/feed")
        if feed.entries:
            return [{"titulo": e.title, "link": e.link} for e in feed.entries[:10]]
        return []
    except:
        return []

# --- CARGA INICIAL ---
clima = obtener_clima_fresia()
noticias = traer_noticias_nacionales()

# --- ENCABEZADO ---
st.markdown("<h1 style='text-align: center; color: #1e3a8a; margin-bottom: 0;'>📰 Prensaenloslagos</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 1.2rem;'><b>📍 Fresia, Región de Los Lagos | {clima}</b></p>", unsafe_allow_html=True)

# --- MARQUESINA DE NOTICIAS (El Scroll) ---
if noticias:
    texto_noticias = "  •  ".join([n['titulo'] for n in noticias])
    st.markdown(f"""
        <div class="ticker-wrapper">
            <marquee scrollamount="8">{texto_noticias}</marquee>
        </div>
    """, unsafe_allow_html=True)
else:
    st.info("Conectando con el servidor de noticias... Revisa tu archivo requirements.txt")

# --- NAVEGACIÓN POR PESTAÑAS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🗞️ Noticias Chile", 
    "🌳 Datos Fresia", 
    "🤝 Centro Solidario", 
    "🤖 IA Libre"
])

with tab1:
    st.subheader("Titulares Nacionales")
    if noticias:
        for n in noticias:
            st.markdown(f"🔹 **[{n['titulo']}]({n['link']})**")
    else:
        st.write("No se pudieron cargar las noticias. Revisa la conexión.")

with tab2:
    st.subheader("Información de nuestra comuna")
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Población Fresia", "12.800 hab.")
        st.write("**Dato Local:** El comercio atiende mayoritariamente hasta las 19:00 hrs.")
    with col_b:
        st.metric("Condición Actual", clima)
        st.write("**Agricultura:** Condiciones óptimas para trabajo de campo hoy.")

with tab3:
    st.subheader("🤝 Centro Solidario en Acción")
    st.success("¡Participa en las campañas de ayuda en la Región de Los Lagos!")
    st.markdown("""
    * **Campaña de Invierno:** Recolección de ropa de abrigo.
    * **Ayuda Directa:** Coordinación de voluntarios para Fresia y alrededores.
    """)
    if st.button("Quiero ayudar"):
        st.balloons()
        st.write("¡Gracias por tu espíritu solidario! Pronto daremos más detalles.")

with tab4:
    st.subheader("🤖 Consulta a la IA Libre")
    st.write("Bienvenido. Soy Libre, asistente de Miguel Alarcón para sus 18k seguidores.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("¿Qué deseas saber hoy?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            respuesta = f"En Prensaenloslagos estamos para servirte. Hoy en Fresia tenemos {clima}. ¿Necesitas información
