import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DEL CEREBRO (API KEY)
# Usamos tu llave con el modelo 'gemini-pro' que es el más estable
try:
    genai.configure(api_key="AIzaSyBERnyHBPNKai3y-IGtykVBaTal414UC7M")
    model = genai.GenerativeModel('gemini-pro')
    ia_activa = True
except Exception as e:
    ia_activa = False
    error_config = str(e)

# 2. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="IA Libre", page_icon="🤖", layout="wide")

# 3. CREACIÓN DEL MENÚ (Aquí estaba el NameError)
# Es vital que 'menu' se defina antes de cualquier 'if'
with st.sidebar:
    st.title("🌐 Portal IA Libre")
    # Definimos la variable 'menu' aquí mismo
    menu = st.radio(
        "Secciones:", 
        ["🤖 IA LIBRE (CABEZA)", "📰 PRENSAENLOSLAGOS", "📍 DATOSFRESIA", "🤝 CENTRO SOLIDARIO"]
    )
    st.divider()
    st.caption("Fresia - Región de Los Lagos")

# URL de tu Google Sites
url_google_sites = "https://sites.google.com/view/ia-libre/inicio"

# 4. LÓGICA DE LAS SECCIONES
if menu == "🤖 IA LIBRE (CABEZA)":
    st.title("🤖 IA Libre: Asistente Universal")
    
    if not ia_activa:
        st.error(f"Error de conexión con el cerebro: {error_config}")
    else:
        # Historial de chat
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Mostrar mensajes previos
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Entrada del usuario
        if prompt := st.chat_input("¿En qué puedo asesorarte hoy?"):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                try:
                    response = model.generate_content(prompt)
                    respuesta_final = response.text
                    st.markdown(respuesta_final)
                    st.session_state.chat_history.append({"role": "assistant", "content": respuesta_final})
                except Exception as e:
                    st.error(f"La IA está pensando demasiado... intenta de nuevo. (Error: {e})")

elif menu == "📰 PRENSAENLOSLAGOS":
    st.title("📰 Prensaenloslagos")
    st.link_button("👉 ABRIR NOTICIAS", url_google_sites)

elif menu == "📍 DATOSFRESIA":
    st.title("📍 DatosFresia")
    st.link_button("👉 VER DATOS DE FRESIA", url_google_sites)

elif menu == "🤝 CENTRO SOLIDARIO":
    st.title("🤝 Centro Solidario en Acción")
    st.link_button("👉 VER AYUDA SOCIAL", url_google_sites)
    
