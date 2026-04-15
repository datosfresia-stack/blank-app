import streamlit as st
import google.generativeai as genai

st.title("🌿 LIBRE")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Probamos el modelo más básico para asegurar conexión
    model = genai.GenerativeModel('gemini-1.0-pro')
else:
    st.error("Falta la API KEY en Secrets")

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
            r = model.generate_content(f"Eres Libre, la asistente de Miguel en Fresia: {p}")
            st.markdown(r.text)
            st.session_state.messages.append({"role": "assistant", "content": r.text})
        except Exception as e:
            st.error(f"Error: {e}")
