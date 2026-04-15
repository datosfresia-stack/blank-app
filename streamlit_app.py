import streamlit as st
import google.generativeai as genai

# Conexión directa con la llave de tus Secrets
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error de configuración: {e}")

st.set_page_config(page_title="Libre - Fresia", page_icon="🌿")
st.title("🌿 LIBRE")

# Sidebar
with st.sidebar:
    st.header("💓 Mi Salud")
    st.write("Presión: **117/76** | Pulso: **66**")
    st.divider()
    st.header("📁 Archivos")
    archivo = st.file_uploader("Sube videos o fotos aquí", type=["mp4", "mov", "jpg", "png"])

# Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if p := st.chat_input("Dime algo, Miguel..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"):
        st.markdown(p)

    with st.chat_message("assistant"):
        try:
           with st.chat_message("assistant"):
        try:
            # Aquí le damos las instrucciones de quién es Libre
            prompt = f"Eres Libre, la asistente de Miguel Alarcón en Fresia. Responde con cariño y sabiduría: {p}"
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Esta es la parte clave: nos dirá la verdad del problema
            st.error(f"Error real: {e}")
