import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Libre", page_icon="🌿")
st.title("🌿 LIBRE")

# Conexión limpia
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Falta la API KEY en los Secrets de Streamlit.")

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
            # Forzamos la ruta completa del modelo para saltar el error 404
            model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
            
            prompt_final = f"Eres Libre, la asistente cariñosa de Miguel Alarcón en Fresia. Responde: {p}"
            response = model.generate_content(prompt_final)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
