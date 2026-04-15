import streamlit as st
import requests
import feedparser

# Configuración de la página
st.set_page_config(page_title="Prensaenloslagos", page_icon="📰", layout="wide")

# --- FUNCIONES ---
def obtener_clima():
    try:
        # Buscamos el clima real de Fresia
        r = requests.get("https://wttr.in/Fresia,Chile?format=%C+%t&m&lang=es", timeout=5)
        return r.text.replace("+", "").replace("Â", "").strip()
    except:
        return "Clima no disponible"

def traer_noticias():
    try:
        # Intentamos leer el diario BioBio
        feed = feedparser.parse("https://www.biobiochile.cl/lista/tag/chile/feed")
        if feed.entries:
            return [{"titulo": e.title, "link": e.link} for e in feed.entries[:8]]
        else:
            return []
    except:
        return []

# --- CARGA DE DATOS ---
clima_actual = obtener_clima()
noticias_actuales = traer_noticias()

# --- DISEÑO VISUAL ---
st.markdown("<h1 style='text-align: center; color: #27ae60;'>📰 Prensaenloslagos</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'><b>📍 Fresia, Los Lagos | {clima_actual}</b></p>", unsafe_allow_html=True)

# 1. El Scroll de noticias (La marquesina)
if noticias_actuales:
    titulares = "  •  ".join([n['titulo'] for n in noticias_actuales])
    st.markdown(f"""
        <div style="background: #1a1a1a; color: #3dfc03; padding: 10px; font-family: 'Courier New', monospace; border-radius: 5px;">
            <marquee scrollamount="8">{titulares}</marquee>
        </div>
    """, unsafe_allow_html=True)
else:
    st.info("Conectando con el servidor de noticias... (Revisa si tienes 'feedparser' en requirements.txt)")

st.write("---")

# 2. Pestañas de la App
tab1, tab2, tab3 = st.tabs(["🗞️ Noticias", "🤝 Comunidad", "🤖 IA Libre"])

with tab1:
    st.subheader("Últimas de Chile")
    if noticias_actuales:
        for n in noticias_actuales:
            st.markdown(f"✅ **[{n['titulo']}]({n['link']})**")
    else:
        st.write("No hay noticias disponibles en este momento.")

with tab2:
    st.subheader("Centro Solidario en Acción")
    st.write("Aquí pondremos los datos de Fresia y las campañas solidarias.")
    st.button("Ver Campañas")

with tab3:
    st.subheader("Chat con IA Libre")
    if st.chat_input("¿En qué te ayudo hoy, Miguel?"):
        st.write("¡Recibido! Estoy listo para responder a tus 18 mil seguidores.")
