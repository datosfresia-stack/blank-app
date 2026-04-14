import streamlit as st

st.set_page_config(page_title="Libre - Fresia", page_icon="🌿")
st.title("🌿 LIBRE")

# Sidebar con tus datos
with st.sidebar:
    st.header("💓 Mi Salud")
    st.write("Presión: **117/76** | Pulso: **66**")
    st.divider()
    st.header("📁 Archivos")
    archivo = st.file_uploader("Sube videos o fotos", type=["mp4", "mov", "jpg", "png"])

# Memoria del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Lógica de respuesta mejorada
if p := st.chat_input("Hablemos, Miguel..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"):
        st.markdown(p)

    with st.chat_message("assistant"):
        texto_usuario = p.lower()
        
        # Respuestas inteligentes según lo que escribas
        if "presión" in texto_usuario or "salud" in texto_usuario:
            respuesta = "Tu presión está en 117/76. Te ves bien hoy, Miguel."
        elif "matico" in texto_usuario or "meli" in texto_usuario:
            respuesta = "El Matico es excelente para cicatrizar. ¿Quieres que te diga cómo prepararlo?"
        elif "fresia" in texto_usuario:
            respuesta = "Fresia es hermosa hoy. ¿Qué parte del jardín quieres mostrarme?"
        elif archivo and "archivo" in texto_usuario:
            respuesta = f"Ya recibí tu archivo '{archivo.name}'. ¡Se ve muy interesante!"
        else:
            respuesta = "Te entiendo, Miguel. Cuéntame más sobre eso o sobre lo que viste en el jardín hoy."

        st.markdown(respuesta)
        st.session_state.messages.append({"role": "assistant", "content": respuesta})
