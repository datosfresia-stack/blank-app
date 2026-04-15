import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

# Configuración de página
st.set_page_config(page_title="Libre", page_icon="🌿")
st.title("🌿 LIBRE")

# 1. Configuración de seguridad y conexión
if "GOOGLE_API_KEY" in st.secrets:
    # Configuramos la llave
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # Definimos el modelo
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # OPCIONES DE CONEXIÓN: Esto fuerza la versión v1 y evita el error 404
    # Usamos RequestOptions para asegurar que no se use la v1beta
    configuracion_segura = RequestOptions(api_version='v1')
else:
    st.error("⚠️ Falta la configuración de la llave API en los Secrets de Streamlit.")
    st.stop()

# 2. Historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 3. Chat interactivo
if p := st.chat_input("Escribe aquí, Miguel..."):
    # Guardar y mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"):
        st.markdown(p)
    
    # Respuesta de Libre
    with st.chat_message("assistant"):
        try:
            # Instrucción de personalidad
            instruccion = f"Eres Libre, la asistente cariñosa y atenta de Miguel Alarcón en Fresia. Responde de forma cercana: {p}"
            
            # Generar contenido forzando la API v1
            response = model.generate_content(
                instruccion,
                request_options=configuracion_segura
            )
            
            # Mostrar y guardar respuesta
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"Aún hay un detalle en la conexión: {e}")
            st.info("Prueba dándole a 'Reboot App' en el menú de la derecha.")
