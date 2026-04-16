import streamlit as st
import google.generativeai as genai

# 1. IDENTIDAD BÁSICA
st.set_page_config(page_title="IA Libre", layout="wide")

# 2. CONEXIÓN AL CEREBRO
API_KEY = "AIzaSyBERnyHBPNKai3y-IGtykVBaTal414UC7M"

try:
    genai.configure(api_key=API_KEY)
    # Usamos el modelo estable
    model = genai.GenerativeModel('gemini-1.5-flash')
    ia_lista = True
except Exception as e:
    ia_lista = False
    st.error(f"Error de conexión: {e}")

# 3. INTERFAZ SENCILLA
st.title("🤖 IA Libre - Fresia")

with st.sidebar:
    st.header("Menú")
    # Ponemos una opción simple primero
    menu = st.selectbox("Selecciona:", ["Asistente IA", "Noticias"])

if menu == "Asistente IA":
    if prompt := st.chat_input("Escribe algo..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                # LLAMADA DIRECTA
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")

elif menu == "Noticias":
    st.write("Cargando portal de Prensaenloslagos...")
    st.link_button("Ir al Sitio Oficial", "https://sites.google.com/view/ia-libre/inicio")
    
