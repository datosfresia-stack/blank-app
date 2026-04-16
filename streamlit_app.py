import streamlit as st
import google.generativeai as genai

# CONFIGURACIÓN
st.set_page_config(page_title="IA Libre", layout="wide")
API_KEY = "AIzaSyBERnyHBPNKai3y-IGtykVBaTal414UC7M"

# INTENTO DE CONFIGURACIÓN DIRECTA
try:
    genai.configure(api_key=API_KEY)
    # Intentamos el modelo más básico de todos para asegurar compatibilidad
    model = genai.GenerativeModel('gemini-1.5-flash')
    ia_lista = True
except Exception as e:
    ia_lista = False
    error_inicial = str(e)

# INTERFAZ
with st.sidebar:
    st.title("🌐 Menú")
    menu = st.radio("Secciones:", ["🤖 IA LIBRE", "📰 NOTICIAS", "📍 FRESIA"])
    if ia_lista:
        st.success("Conexión Base OK ✅")
    else:
        st.error("Error de Configuración ❌")

# SECCIÓN CHAT
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
                # AQUÍ FORZAMOS LA RESPUESTA
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.chat.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # ESTE MENSAJE ES EL QUE NECESITO QUE ME TIRES
                st.error(f"DETALLE DEL ERROR: {e}")
                
