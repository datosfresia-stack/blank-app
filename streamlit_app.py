import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="IA Libre Fresia", page_icon="🤖")

# CONEXIÓN
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # CAMBIAMOS AL MODELO CON CUOTA LIBRE
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        ia_lista = True
    else:
        ia_lista = False
        st.error("⚠️ Falta la llave en Secrets.")
except Exception as e:
    ia_lista = False
    st.error(f"Error de inicio: {e}")

st.title("🤖 IA Libre")

if ia_lista:
    # Mensaje de éxito real
    st.success("✅ Sistema en línea y listo para recibir consultas.")
    
    pregunta = st.text_input("Haz tu consulta:", placeholder="Escribe aquí...")
    
    if pregunta:
        with st.spinner("Generando respuesta..."):
            try:
                response = model.generate_content(pregunta)
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                # Si este modelo también da cuota, nos avisará
                st.error("Límite de mensajes alcanzado temporalmente.")
                st.info(f"Detalle: {e}")

st.divider()
st.caption("Fresia - Versión Estable")
