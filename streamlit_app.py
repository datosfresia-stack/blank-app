import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

# 1. Configuración de página
st.set_page_config(page_title="IA Libre Fresia", layout="centered")

# 2. Conexión SEGURA y FORZADA
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        
        # Configuramos el modelo
        model = genai.GenerativeModel('gemini-1.5-flash')
        ia_lista = True
    else:
        ia_lista = False
        st.warning("⚠️ Falta la llave en los Secrets de Streamlit.")
except Exception as e:
    ia_lista = False
    st.error(f"Error de configuración: {e}")

# 3. Interfaz
st.title("🤖 IA Libre")

if ia_lista:
    pregunta = st.text_input("Haz tu consulta aquí:")
    
    if pregunta:
        try:
            with st.spinner("Conectando con el cerebro de Google..."):
                # ESTA ES LA LÍNEA CLAVE: Forzamos la versión v1
                response = model.generate_content(
                    pregunta,
                    request_options=RequestOptions(api_version='v1')
                )
                st.markdown("---")
                st.markdown(response.text)
        except Exception as e:
            # Si sale error, nos dirá exactamente qué puerta falló
            st.error(f"Aviso del sistema: {e}")

st.divider()
st.caption("Fresia, Región de Los Lagos - Conexión vía Google Gemini")
