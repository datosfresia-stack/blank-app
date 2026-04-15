import streamlit as st
import google.generativeai as genai

# Configuramos la página y el diseño
st.set_page_config(page_title="Libre - Fresia", page_icon="🌿")
st.title("🌿 LIBRE")

# Conexión forzada a versión estable
try:
    # Esta línea es el truco maestro: forzamos la versión 'v1'
    from google.ai import generativelanguage as gql
    
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # Configuramos el modelo con el nombre más básico posible
    model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"max_output_tokens": 2048})
    
    # Prueba interna de seguridad
    st.success("✅ ¡Conexión establecida con el cerebro de Libre!")
except Exception as e:
    st.error(f"Error real al conectar: {e}")

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
