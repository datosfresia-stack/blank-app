import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

# CONFIGURACIÓN
st.set_page_config(page_title="IA Libre", layout="wide")

# API KEY
API_KEY = "AIzaSyBERnyHBPNKai3y-IGtykVBaTal414UC7M"

# CONFIGURACIÓN DEL MODELO CON FORZADO DE VERSIÓN
try:
    genai.configure(api_key=API_KEY)
    # Forzamos a que use la API v1, que es donde vive gemini-1.5-flash
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash'
    )
    ia_lista = True
except Exception as e:
    ia_lista = False
    st.error(f"Error al configurar: {e}")

# INTERFAZ
with st.sidebar:
    st.title("🌐 Menú")
    menu = st.radio("Secciones:", ["🤖 IA LIBRE", "📰 NOTICIAS", "📍 FRESIA"])

if menu == "🤖 IA LIBRE":
    st.title("🤖 Asistente IA Libre")
    
    if "chat" not in st.session_state:
        st.session_state.chat = []

    for m in st.session_state.chat:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Escribe tu consulta..."):
        st.session_state.chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # Usamos RequestOptions para asegurar que no busque en v1beta
                response = model.generate_content(
                    prompt,
                    request_options=RequestOptions(api_version='v1')
                )
                st.markdown(response.text)
                st.session_state.chat.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error de conexión: {e}")
                st.info("Si el error persiste, reinicia la app en el panel de Streamlit (Reboot).")

# SECCIONES DE ENLACE
elif menu == "📰 NOTICIAS":
    st.link_button("Ir a Prensaenloslagos", "https://sites.google.com/view/ia-libre/inicio")
elif menu == "📍 FRESIA":
    st.link_button("Ir a DatosFresia", "https://sites.google.com/view/ia-libre/inicio")
    
