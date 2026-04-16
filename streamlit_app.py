import streamlit as st
import google.generativeai as genai

# CONFIGURACIÓN INICIAL
st.set_page_config(page_title="IA Libre", layout="wide")

# CONEXIÓN DIRECTA
API_KEY = "AIzaSyBERnyHBPNKai3y-IGtykVBaTal414UC7M"
genai.configure(api_key=API_KEY)

# FUNCIÓN PARA DESPERTAR EL CEREBRO
def despertar_cerebro():
    try:
        # Esto lista los modelos que tu llave TIENE permiso de usar
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return m.name
        return None
    except:
        return None

if "modelo_vivo" not in st.session_state:
    st.session_state.modelo_vivo = despertar_cerebro()

# BARRA LATERAL
with st.sidebar:
    st.title("🌐 Menú")
    menu = st.radio("Ir a:", ["🤖 IA LIBRE", "📰 NOTICIAS", "📍 FRESIA", "🤝 SOLIDARIO"])
    if st.session_state.modelo_vivo:
        st.success("Cerebro Online ✅")
    else:
        st.error("Cerebro Offline ❌")

# SECCIÓN IA
if menu == "🤖 IA LIBRE":
    st.title("🤖 Asistente IA Libre")
    
    if not st.session_state.modelo_vivo:
        st.warning("Google aún no activa tu llave. Intenta escribir algo abajo para forzar la conexión.")
    
    if "chat" not in st.session_state:
        st.session_state.chat = []

    for m in st.session_state.chat:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Escribe tu consulta aquí..."):
        st.session_state.chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # Usamos el modelo que el sistema encontró disponible
                m_name = st.session_state.modelo_vivo if st.session_state.modelo_vivo else "models/gemini-pro"
                model = genai.GenerativeModel(m_name)
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.chat.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error técnico: {e}")

# SECCIONES DE ENLACE
elif menu == "📰 NOTICIAS":
    st.link_button("Ir a Prensaenloslagos", "https://sites.google.com/view/ia-libre/inicio")
elif menu == "📍 FRESIA":
    st.link_button("Ir a DatosFresia", "https://sites.google.com/view/ia-libre/inicio")
elif menu == "🤝 SOLIDARIO":
    st.link_button("Ir a Centro Solidario", "https://sites.google.com/view/ia-libre/inicio")
    
