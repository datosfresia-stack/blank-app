import streamlit as st

st.set_page_config(page_title="Libre - Fresia", page_icon="🌿")

st.title("🌿 LIBRE")
st.markdown("### Tu Asistente en Fresia")

# Panel lateral con datos
with st.sidebar:
    st.header("💓 Mi Salud")
    st.write("Presión: **117/76** | Pulso: **66**")
    st.divider()
    st.header("🌳 Mi Jardín")
    st.write("- **Matico**\n- **Meli**")
    st.divider()
    # NUEVO: Botón para subir tus videos o fotos
    st.header("📁 Subir Archivos")
    archivo = st.file_uploader("Sube tus videos de Facebook o Drive aquí", type=["mp4", "mov", "jpg", "png"])
    if archivo:
        st.success(f"Archivo {archivo.name} cargado con éxito")

# Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if p := st.chat_input("Hola Miguel, hablemos..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"):
        st.markdown(p)
    with st.chat_message("assistant"):
        r = "Te escucho, Miguel. Estoy aquí contigo en nuestra casa de Fresia."
        if archivo:
            r += f" He recibido tu archivo '{archivo.name}' y estoy listo para que lo comentemos."
        
        if "matico" in p.lower() or "meli" in p.lower():
            r = "El Matico y el Meli son las guardianas de nuestra salud en el jardín."
        elif "salud" in p.lower():
            r = "Tu presión está estable (117/76). Todo bajo control."
        
        st.markdown(r)
        st.session_state.messages.append({"role": "assistant", "content": r})
