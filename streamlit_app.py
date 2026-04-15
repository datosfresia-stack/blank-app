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
        # Consulta el clima de Fresia
        r = requests.get("https://wttr.in/Fresia,Chile?format=%C+%t&m&lang=es", timeout=5)
        if r.status_code == 200:
            return r.text.replace("+", "").strip()
        else:
            return "Despejado 14°C"
    except:
        return "Despejado 14°C"

def traer_noticias():
    try:
        # Conecta con el feed de BioBioChile
        feed = feedparser.parse("https://www.biobiochile.cl/lista/tag/chile/feed")
        if feed.entries:
            return [{"titulo": e.title, "link": e.link} for e in feed.entries[:10]]
        else:
            return []
    except:
        return []

# --- CARGA INICIAL DE DATOS ---
clima_fresia = obtener_clima()
lista_noticias = traer_noticias()

# --- INTERFAZ DE USUARIO ---
st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>📰 Prensaenloslagos</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'><b>📍 Fresia, Región de Los Lagos | {clima_fresia}</b></p>", unsafe_allow_html=True)

# MARQUESINA (EL SCROLL DE NOTICIAS)
if lista_noticias:
    titulares_unidos = "  •  ".join([n['titulo'] for n in lista_noticias])
    st.markdown(f'<div class="ticker-wrapper"><marquee scrollamount="8">{titulares_unidos}</marquee></div>', unsafe_allow_html=True)
else:
    st.info("Conectando con el servidor de noticias... Revisa el archivo requirements.txt")

# PESTAÑAS DE NAVEGACIÓN
tab1, tab2, tab3, tab4 = st.tabs(["🗞️ Noticias", "🌳 Datos Fresia", "🤝 Solidario", "🤖 IA Libre"])

with tab1:
    st.subheader("Titulares Nacionales")
    if lista_noticias:
        for n in lista_noticias:
            st.markdown(f"🔹 **[{n['titulo']}]({n['link']})**")
    else:
        st.write("Las noticias se están actualizando. Vuelve en un momento.")

with tab2:
    st.subheader("Datos de la Comuna de Fresia")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Población", "12.800 hab.")
        st.write("Fresia es conocida como la 'Ciudad de las Capas'.")
    with col2:
        st.metric("Clima Actual", clima_fresia)
        st.write("Fuente: wttr.in")

with tab3:
    st.subheader("Centro Solidario en Acción")
    st.success("¡Apoyemos a nuestra comunidad!")
    st.markdown("""
    * **Campaña Ropa:** Recolección de frazadas para el invierno.
    * **Voluntariado:** Únete a los operativos en terreno.
    """)
    if st.button("Quiero participar"):
        st.balloons()
        st.write("¡Gracias Miguel! Registro enviado con éxito.")

with tab4:
    st.subheader("Consulta a la IA Libre")
    st.write("Asistente oficial para los 18 mil seguidores.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if entrada_usuario := st.chat_input("Escribe tu pregunta aquí"):
        st.session_state.messages.append({"role": "user", "content": entrada_usuario})
        with st.chat_message("user"):
            st.markdown(entrada_usuario)
        
        with st.chat_message("assistant"):
            texto_respuesta = f"Hola, soy Libre. Te informo que en Fresia tenemos {clima_fresia}. ¿Cómo puedo ayudarte con Prensaenloslagos hoy?"
            st.markdown(texto_respuesta)
            st.session_state.messages.append({"role": "assistant",
