import streamlit as st
import google.generativeai as genai

# 1. SETUP BÁSICO SIN COMPLICACIONES
st.set_page_config(page_title="IA Libre")

# CONFIGURAR IA
API_KEY = "AIzaSyBERnyHBPNKai3y-IGtykVBaTal414UC7M"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. INTERFAZ LIMPIA
st.title("🤖 IA Libre")

# Usar botones simples en lugar de menús complejos para evitar el error de Node
col1, col2 = st.columns(2)
with col1:
    if st.button("💬 Chat con IA"):
        st.session_state.seccion = "chat"
with col2:
    if st.button("📰 Noticias"):
        st.session_state.seccion = "noticias"

# Inicializar sección
if "seccion" not in st.session_state:
    st.session_state.seccion = "chat"

# 3. LÓGICA
if st.session_state.seccion == "chat":
    st.subheader("Asistente Virtual")
    user_input = st.text_input("¿En qué te ayudo?", key="input_ia")
    
    if user_input:
        try:
            response = model.generate_content(user_input)
            st.write("---")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {e}")

elif st.session_state.seccion == "noticias":
    st.subheader("Portal de Noticias")
    st.link_button("Abrir Prensaenloslagos", "https://sites.google.com/view/ia-libre/inicio")
    
