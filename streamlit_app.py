import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="IA Libre Fresia")

# 1. CONEXIÓN LIMPIA
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # USAMOS EL MODELO MÁS COMPATIBLE DE TU LISTA
        # Le quitamos el 'models/' para que no se confunda
        model = genai.GenerativeModel('gemini-pro')
        ia_lista = True
    else:
        ia_lista = False
        st.error("Falta llave en Secrets")
except Exception as e:
    ia_lista = False
    st.error(f"Error: {e}")

st.title("🤖 IA Libre")

if ia_lista:
    st.success("✅ Conexión con Google establecida")
    
    pregunta = st.text_input("Haz tu consulta:", key="pregunta_final")
    
    if pregunta:
        with st.spinner("Buscando respuesta..."):
            try:
                # Intento con gemini-pro (El modelo más estable)
                response = model.generate_content(pregunta)
                st.markdown("---")
                st.write(response.text)
            except Exception as e:
                # Si falla, probamos con la versión de texto puro
                st.error("Ajustando frecuencia...")
                try:
                    model_alt = genai.GenerativeModel('gemini-1.0-pro')
                    response = model_alt.generate_content(pregunta)
                    st.write(response.text)
                except:
                    st.info(f"Nota del sistema: {e}")

st.divider()
st.caption("Fresia - Conexión Estable Protegida")
