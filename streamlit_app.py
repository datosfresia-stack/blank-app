import streamlit as st
import google.generativeai as genai

# 1. Configuración básica
st.set_page_config(page_title="IA Libre Fresia", page_icon="🤖")

# 2. Conexión segura con la llave de los Secrets
try:
    # Esto busca la llave en el cofre que configuraste en el Paso 1
    llave = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=llave)
    model = genai.GenerativeModel('gemini-1.5-flash')
    ia_lista = True
except Exception as e:
    ia_lista = False
    st.error("Error: Configura la clave en 'Secrets' de Streamlit.")

# 3. Interfaz
st.title("🤖 IA Libre")
st.write("Bienvenido al asistente de Fresia.")

if ia_lista:
    # Una caja de texto simple para evitar errores visuales
    pregunta = st.text_input("¿En qué te puedo ayudar hoy?")
    
    if pregunta:
        with st.spinner("Procesando..."):
            try:
                # La IA genera la respuesta
                response = model.generate_content(pregunta)
                st.subheader("Respuesta:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Google dice: {e}")

# Botón de auxilio
st.divider()
st.link_button("Ir a Prensaenloslagos", "https://sites.google.com/view/ia-libre/inicio")
