import streamlit as st

st.set_page_config(page_title="Libre - Fresia", page_icon="🌿")
st.title("🌿 LIBRE")
st.markdown("### Tu Asistente en Fresia")

with st.sidebar:
    st.header("💓 Mi Salud")
    st.write("Presión: **117/76** | Pulso: **66**")
    st.divider()
    st.header("🌳 Mi Jardín")
    st.write("- **Matico**\n- **Meli**")
    st.divider()
    st.header("📁 Subir Archivos")
    archivo = st.file_uploader("Sube tus videos aquí", type=["mp4", "mov", "jpg", "png"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if p := st.chat_input("Hola Miguel..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"):
        st.markdown(p)
    with st.chat_message("assistant"):
        r = "Te escucho, Miguel. Estoy aquí en nuestra casa de Fresia."
        if archivo:
            r = f"He recibido tu archivo {archivo.name}. ¿Qué quieres que haga con él?"
        st.markdown(r)
        st.session_state.messages.append({"role": "assistant", "content": r})
