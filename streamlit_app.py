import streamlit as st
import google.generativeai as genai

# Configuración de Libre
st.set_page_config(page_title="Libre - Fresia", page_icon="🌿")
st.title("🌿 LIBRE")

# Conexión directa
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Falta la llave GOOGLE_API_KEY en Secrets.")
else:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Sidebar de salud (Tus datos de Fresia)
with st.sidebar:
    st.header("💓 Mi Salud")
    st.write("Presión: **117/76** | Pulso: **66**")
    st.divider()
    st.write("Estado: Conectada")

# Historial
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
            # Forzamos el uso del modelo más estable para evitar el 404
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(f"Eres Libre, la asistente cariñosa de Miguel Alarcón en Fresia. Responde: {p}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Si falla, probamos con el modelo Pro automáticamente
            try:
                model_alt = genai.GenerativeModel('gemini-pro')
                response = model_alt.generate_content(p)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.error("Miguel, hay un problema con la versión de Python. Intenta escribir 'Hola' de nuevo.")
