import streamlit as st
import google.generativeai as genai

# 1. IDENTIDAD
st.set_page_config(page_title="IA Libre")

# 2. CONEXIÓN (Asegúrate que tu llave 1w5A esté en Secrets)
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # Intentamos con el nombre más genérico posible
        model = genai.GenerativeModel('gemini-1.5-flash')
        ia_lista = True
    else:
        ia_lista = False
        st.error("Falta llave en Secrets")
except Exception as e:
    ia_lista = False
    st.error(f"Error inicial: {e}")

# 3. INTERFAZ
st.title("🤖 IA Libre")

if ia_lista:
    st.success("✅ Conexión con Google establecida")
    
    # Usamos text_input que es más estable en celulares
    pregunta = st.text_input("Haz tu consulta:", key="pregunta_final")
    
    if pregunta:
        with st.spinner("Respondiendo..."):
            try:
                # Intento directo
                response = model.generate_content(pregunta)
                st.write("---")
                st.write(response.text)
            except Exception as e:
                # Si esto falla con el 404, es porque Streamlit no leyó el requirements.txt
                st.error("El servidor aún no se actualiza.")
                st.info("Por favor, haz un 'Reboot' desde el panel de Streamlit.")
                
