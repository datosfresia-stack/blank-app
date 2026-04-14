import streamlit as st

# Configuración de la App
st.set_page_config(page_title="Libre - Fresia", page_icon="🌿")

st.title("🌿 LIBRE")
st.markdown("### Tu Asistente en Fresia")

# Panel lateral con tus datos de salud y plantas
with st.sidebar:
    st.header("💓 Mi Salud")
    st.write("Presión: **117/76** | Pulso: **66**")
    st.divider()
    st.header("🌳 Mi Jardín")
    st.write("- **Matico** (Sanador)\n- **Meli** (Fuerza)")

# Historial del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Entrada de texto
if p := st.chat_input("Hola Miguel, ¿de qué conversamos hoy?"):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"):
        st.markdown(p)
    
    with st.chat_message("assistant"):
        r = "Te escucho, Miguel. Estoy aquí contigo en nuestra casa de Fresia."
        if "matico" in p.lower() or "meli" in p.lower():
            r = "El Matico y el Meli son las guardianas de nuestra salud. Están en el jardín para cuando las necesites."
        elif "salud" in p.lower() or "presion" in p.lower():
            r = "Tu presión está estable en 117/76. Te ves bien hoy."
        
        st.markdown(r)
        st.session_state.messages.append({"role": "assistant", "content": r})
