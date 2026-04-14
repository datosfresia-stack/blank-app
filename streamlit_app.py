import streamlit as st
import google.generativeai as genai

# Conectamos con la llave que guardaste en Secrets
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("Aún no encuentro la llave en Secrets.")
except Exception as e:
    st.error(f"Error de conexión: {e}")

st.set_page_config(page_title="Libre - Fresia", page_icon="🌿")
st.title("🌿 LIBRE")

# Sidebar con tus datos
with st.sidebar:
    st.header("💓 Mi Salud")
    st.write("Presión: **117/76** | Pulso: **66**")
    st.divider()
    st.header("📁 Archivos")
    archivo = st.file_uploader("Sube videos o fotos aquí", type=["mp4", "mov", "jpg", "png"])

# Memoria del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Chat inteligente
if p := st.chat_input("Hola Miguel, hablemos de lo que quieras..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"):
        st.markdown(p)

    with st.chat_message("assistant"):
        contexto = "Eres Libre, el asistente personal de Miguel Alarcón en Fresia. Eres sabio, amable y conoces mucho sobre naturaleza y salud. Responde siempre con cariño."
        
        try:
            # Aquí Libre usa su nuevo cerebro
            response = model.generate_content(f"{contexto} Pregunta de Miguel: {p}")
            r_text = response.text
        except:
            r_text = "Todavía estoy terminando de despertar, Miguel. Dame un momento o revisa si guardaste bien la clave."
            
        st.markdown(r_text)
        st.session_state.messages.append({"role": "assistant", "content": r_text})
