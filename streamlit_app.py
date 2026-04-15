import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Libre - Fresia", page_icon="🌿")
st.title("🌿 LIBRE")

# Conexión sin errores
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Falta la llave en Secrets")
else:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Probamos el nombre más moderno primero
    model = genai.GenerativeModel('gemini-1.5-flash')

with st.sidebar:
    st.header("💓 Mi Salud")
    st.write("Presión: **117/76** | Pulso: **66**")
    st.divider()
    st.success("Conectado")

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
            # USAMOS EL MÉTODO MÁS COMPATIBLE
            response = model.generate_content(f"Eres Libre, la asistente de Miguel Alarcón en Fresia. Responde: {p}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Miguel, intenta escribir de nuevo. Si sale 404, haremos el último ajuste en el archivo de texto.")
