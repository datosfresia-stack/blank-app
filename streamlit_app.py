import streamlit as st
import google.generativeai as genai

# Configuración básica
st.set_page_config(page_title="Libre - Fresia", page_icon="🌿")
st.title("🌿 LIBRE")

# Conexión simple
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Falta la llave en los Secrets de Streamlit.")
else:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Probamos el nombre más estándar de todos
   model = genai.GenerativeModel(
        model_name='models/gemini-1.5-flash',
    )

# Sidebar informativa
with st.sidebar:
    st.header("💓 Mi Salud")
    st.write("Presión: **117/76** | Pulso: **66**")
    st.divider()
    st.write("Estado: Conectando...")

# Memoria
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Chat
if p := st.chat_input("Dime algo, Miguel..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"):
        st.markdown(p)

    with st.chat_message("assistant"):
        try:
            # Aquí está el truco: le pedimos la respuesta de la forma más sencilla
            response = model.generate_content(f"Eres Libre, la asistente de Miguel Alarcón en Fresia. Saluda con cariño: {p}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error técnico: {e}")
            st.info("Miguel, si sale error 404, intentaremos otro camino pronto.")
