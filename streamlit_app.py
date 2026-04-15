import streamlit as st
import google.generativeai as genai

# Configuración de página
st.set_page_config(page_title="Libre", page_icon="🌿")
st.title("🌿 LIBRE")

# 1. Configuración de la conexión
if "GOOGLE_API_KEY" in st.secrets:
    # Configuramos la llave directamente
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # Creamos el modelo (sin configuraciones extra que causen errores)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ Falta la llave API en los Secrets de Streamlit.")
    st.stop()

# 2. Historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes guardados
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 3. Chat con Miguel
if p := st.chat_input("Dime algo, Miguel..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"):
        st.markdown(p)
    
    with st.chat_message("assistant"):
        try:
            # Personalidad de Libre
            instruccion = f"Eres Libre, la asistente cariñosa de Miguel Alarcón en Fresia. Responde con calidez: {p}"
            
            # Generar respuesta
            response = model.generate_content(instruccion)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"Todavía tenemos un detalle: {e}")
