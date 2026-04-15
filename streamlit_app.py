import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Libre", page_icon="🌿")
st.title("🌿 LIBRE")

# 1. Configuración de la llave
if "GOOGLE_API_KEY" in st.secrets:
    # Este comando configura la versión de forma global para que no falle
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # Usamos el modelo flash sin adornos que causen errores
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Falta la API KEY en los Secrets.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if p := st.chat_input("Escribe aquí, Miguel..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"):
        st.markdown(p)
    
    with st.chat_message("assistant"):
        try:
            # Respuesta simple y directa
            response = model.generate_content(f"Eres Libre, la asistente de Miguel en Fresia: {p}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
