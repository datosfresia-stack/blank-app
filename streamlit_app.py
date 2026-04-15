import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

st.set_page_config(page_title="Libre", page_icon="🌿")
st.title("🌿 LIBRE")

# 1. Configuración de la llave
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # TRUCO MAESTRO: Forzamos la versión v1 para evitar el error 404
    # Esto le dice a Google: "No uses la puerta beta, usa la puerta estable"
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        generation_config={"temperature": 0.7}
    )
else:
    st.error("Falta la API KEY en los Secrets.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if p := st.chat_input("Escribe aquí, Miguel..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"):
        st.markdown(p)
    
    with st.chat_message("assistant"):
        try:
            # Usamos opciones de transporte para asegurar la conexión
            response = model.generate_content(
                f"Eres Libre, la asistente de Miguel en Fresia: {p}",
                request_options=RequestOptions(api_version='v1')
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error persistente: {e}")
