import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

# 1. IDENTIDAD
st.set_page_config(page_title="IA Libre", layout="centered")

# 2. CONEXIÓN FORZADA (Asegúrate que tu llave 1w5A esté en Secrets)
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # Usamos el modelo más básico para asegurar compatibilidad
        model = genai.GenerativeModel('gemini-1.5-flash')
        ia_lista = True
    else:
        ia_lista = False
        st.error("Configura la llave en Secrets")
except Exception as e:
    ia_lista = False
    st.error(f"Error: {e}")

# 3. INTERFAZ
st.title("🤖 IA Libre")

if ia_lista:
    st.success("✅ Conexión con Google establecida")
    
    if prompt := st.chat_input("¿En qué puedo ayudarte?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                # LA LÍNEA MÁGICA: Obligamos a usar la API v1
                # Esto mata el error de 'v1beta' para siempre
                response = model.generate_content(
                    prompt, 
                    request_options=RequestOptions(api_version='v1')
                )
                st.markdown(response.text)
            except Exception as e:
                # Si esto falla, es que el 'requirements.txt' no está actualizado
                st.error("Actualizando protocolos...")
                st.info("Asegúrate de que tu requirements.txt diga: google-generativeai==0.8.3")
                
