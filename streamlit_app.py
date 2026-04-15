import streamlit as st
import google.generativeai as genai

# Configuramos la página y el diseño
st.set_page_config(page_title="Libre - Fresia", page_icon="🌿")
st.title("🌿 LIBRE")

# Conexión con la llave de Secrets
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Probamos con el nombre estándar de Gemini Pro
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"Error en la llave: {e}")
# Barra lateral con tu información
with st.sidebar:
    st.header("💓 Mi Salud")
    st.write("Presión: **117/76** | Pulso: **66**")
    st.divider()
    st.header("📁 Archivos")
    st.file_uploader("Sube videos o fotos aquí", type=["mp4", "mov", "jpg", "png"])

# Memoria del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Chat principal
if p := st.chat_input("Dime algo, Miguel..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"):
        st.markdown(p)

    with st.chat_message("assistant"):
        try:
            # Instrucción de personalidad
            prompt = f"Eres Libre, la asistente cariñosa y sabia de Miguel Alarcón en Fresia. Miguel te dice: {p}"
            response = model.generate_content(prompt)
            respuesta = response.text
            st.markdown(respuesta)
            st.session_state.messages.append({"role": "assistant", "content": respuesta})
        except Exception as e:
            st.error(f"Error real al conectar: {e}")
