import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página
st.set_page_config(page_title="IA Libre Fresia", page_icon="🤖")

# 2. Conexión con el modelo exacto de tu lista
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # Usamos el modelo que tu cuenta SÍ reconoce (el #2 de tu lista)
        model = genai.GenerativeModel('gemini-2.0-flash')
        ia_lista = True
    else:
        ia_lista = False
        st.error("⚠️ Falta la llave en Secrets.")
except Exception as e:
    ia_lista = False
    st.error(f"Error de inicio: {e}")

# 3. Interfaz de Usuario
st.title("🤖 IA Libre")
st.success("¡Conexión exitosa con Gemini 2.0!")

if ia_lista:
    pregunta = st.text_input("Haz tu consulta:", placeholder="Escribe aquí...")
    
    if pregunta:
        with st.spinner("La IA está respondiendo..."):
            try:
                # Generamos la respuesta
                response = model.generate_content(pregunta)
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error("Hubo un problema al generar la respuesta.")
                st.info(f"Detalle técnico: {e}")

# Pie de página
st.divider()
st.caption("Fresia - Conectado a Gemini 2.0 Flash")
