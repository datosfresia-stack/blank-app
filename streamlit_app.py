import streamlit as st
import os
from dotenv import load_dotenv
from serpapi import GoogleSearch

# --- CONFIGURACIÓN ---
load_dotenv()
API_KEY = os.getenv("SERPAPI_API_KEY")

# --- DATOS ---
NOMBRE = "IA Libre"
CREADOR = "Datos Fresia"
RAIZ = "Chile"

# --- RESPUESTAS ---
RESPUESTAS = {
    "hola": "¡Hola! Soy IA Libre. ¿En qué puedo ayudarte?",
    "como te llamas": f"Me llamo {NOMBRE}.",
    "cual es tu nombre": f"Me llamo {NOMBRE}.",
    "quien eres": f"Soy {NOMBRE}, creado por {CREADOR} en {RAIZ}.",
    "quien te creo": f"Me creó {CREADOR}.",
    "donde estan tus raices": f"Estoy hecho en {RAIZ}.",
    "gracias": "¡De nada!",
    "adios": "¡Hasta luego!"
}

YOUTUBE = "https://www.youtube.com/@DFresiaTV"

st.set_page_config(page_title=NOMBRE, page_icon="🤖", layout="wide")

# --- MENU LATERAL ---
with st.sidebar:
    st.title("🤖 " + NOMBRE)
    st.markdown("---")
    st.write(f"**Asistente:** {NOMBRE}")
    st.write(f"**Raíces:** {RAIZ}")
    st.write(f"**Creador:** {CREADOR}")

    st.markdown("---")
    st.subheader("📺 Canal")
    st.markdown(f"[![YouTube](https://img.icons8.com/color/48/000000/youtube-play.png)]({YOUTUBE})", unsafe_allow_html=True)
    
    st.markdown("---")
    st.header("📌 MENU")
    
    # ARREGLADO: Le puse texto y key único
    opcion = st.radio(
        "Selecciona:",
        ("Inicio", "Chat", "Acerca"),
        key="menu_final_123"
    )

# --- PAGINAS ---

if opcion == "Inicio":
    st.header("Bienvenido a IA LIBRE")
    st.write(f"Soy **{NOMBRE}**, desarrollado en **{RAIZ}** por **{CREADOR}**.")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 📰 Prensa en Los Lagos")
        st.markdown("Noticias y actualidad.")
        st.markdown("[Visitar](https://sites.google.com/view/ia-libre/inicio)")
    with col2:
        st.markdown("#### 🤝 Centro Solidario")
        st.write("*(En desarrollo)*")
    with col3:
        st.markdown("#### 📍 Datos Fresia")
        st.markdown("Info de la comuna.")
        st.markdown("[Visitar](https://sites.google.com/view/datosfresia/inicio)")

elif opcion == "Chat":
    st.header("💬 CHAT IA")
    st.write("Busco información en tiempo real.")

    if 'historial' not in st.session_state:
        st.session_state.historial = []

    for msg in st.session_state.historial:
        if msg['role'] == 'user':
            st.info(f"**Tú:** {msg['content']}")
        else:
            st.success(f"**{NOMBRE}:** {msg['content']}")

    with st.form(key='form_chat', clear_on_submit=True):
        texto = st.text_area("Escribe aquí:")
        enviar = st.form_submit_button("Enviar 🔍")

    if enviar and texto:
        st.session_state.historial.append({"role":"user", "content":texto})
        
        texto_min = texto.lower().strip()
        resp = "No encontré información."
        ok = False

        # RESPUESTAS RAPIDAS
        if "hola" in texto_min:
            resp = "¡Hola! ¿En qué puedo ayudarte?"
            ok = True
        elif "como te llamas" in texto_min or "cual es tu nombre" in texto_min:
            resp = f"Me llamo {NOMBRE}."
            ok = True
        elif "quien eres" in texto_min:
            resp = f"Soy {NOMBRE}, creado por {CREADOR} en {RAIZ}."
            ok = True
        elif "quien te creo" in texto_min:
            resp = f"Me creó {CREADOR}."
            ok = True
        elif "gracias" in texto_min:
            resp = "¡De nada!"
            ok = True

        # BUSQUEDA EN GOOGLE
        if not ok and API_KEY:
            try:
                params = {
                    "q": texto,
                    "api_key": API_KEY,
                    "engine": "google",
                    "hl": "es",
                    "gl": "cl"
                }
                search = GoogleSearch(params)
                res = search.get_dict()

                if "answer_box" in res and res["answer_box"]:
                    resp = res["answer_box"].get("answer", "Sin datos")
                elif "organic_results" in res and len(res["organic_results"]) > 0:
                    primero = res["organic_results"][0]
                    resp = f"**{primero.get('title','')}**\n\n{primero.get('snippet','')}\n\n[Fuente]({primero.get('link','#')})"
                else:
                    resp = "Busqué pero no hay resultados claros."
            except Exception as e:
                resp = f"Error: {str(e)}"

        st.session_state.historial.append({"role":"assistant", "content":resp})
        st.rerun()

elif opcion == "Acerca":
    st.header("ℹ️ Acerca de")
    st.write(f"**{NOMBRE}** v1.0")
    st.write(f"Creado por: {CREADOR}")
    st.write(f"País: {RAIZ}")
    st.write("Sistema optimizado.")
    
