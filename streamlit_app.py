import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Libre", page_icon="🌿")
st.title("🌿 LIBRE")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY="AIzaSyA5JSdx5cO8JI8nCnQJ-0EdK32uiVqnELs"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Falta la API KEY")

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
