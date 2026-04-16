import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DEL CEREBRO (API KEY)
# Usamos el modelo 'gemini-1.5-flash' que es el actual y gratuito
try:
    genai.configure(api_key="AIzaSyBERnyHBPNKai3y-IGtykVBaTal414UC7M")
    # Este nombre es el oficial hoy en día
    model = genai.GenerativeModel('gemini-1.5-flash')
    ia_activa = True
except Exception as e:
    ia_activa = False
    error_config = str(e)

# 2. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="IA Libre", page_icon="🤖", layout="wide")

# 3. BARRA LATERAL (Aseguramos que 'menu' se cree siempre)
with st.sidebar:
    st.title("🌐 Portal IA Libre")
    menu = st.radio(
        "Secciones:", 
        ["🤖 IA LIBRE (CABEZA)", "📰 PRENSAENLOSLAGOS", "📍 DATOSFRESIA", "🤝 CENTRO SOLIDARIO"]
    )
    st.divider()
    st.caption("Fresia - Región de Los Lagos")

url_google_sites = "https://sites.google.com/view/ia-libre/inicio"

# 4. LÓGICA DE LAS SECCIONES
if menu == "🤖 IA LIBRE (CABEZA)":
    st.title("🤖 IA Libre: Asistente Universal")
    
    if not ia_activa:
        st.error(f"Error de configuración: {error_config}")
    else:
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if prompt := st.chat_input("¿En qué puedo asesorarte hoy?"):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                try:
                    # Intento de respuesta con el nuevo nombre de modelo
                    response = model.generate_content(prompt)
                    # Usamos .text para obtener el contenido
                    respuesta_final = response.text
                    st.markdown(respuesta_final)
                    st.session_state.chat_history.append({"role": "assistant", "content": respuesta_final})
                except Exception as e:
                    # Si falla, te mostrará el error real para saber si es el nombre o la llave
                    st.error(f"Aviso técnico: {e}")

# ... (El resto de los elif se mantienen igual) ...
elif menu == "📰 PRENSAENLOSLAGOS":
    st.title("📰 Prensaenloslagos")
    st.link_button("👉 ABRIR NOTICIAS", url_google_sites)

elif menu == "📍 DATOSFRESIA":
    st.title("📍 DatosFresia")
    st.link_button("👉 VER DATOS DE FRESIA", url_google_sites)

elif menu == "🤝 CENTRO SOLIDARIO":
    st.title("🤝 Centro Solidario en Acción")
    st.link_button("👉 VER AYUDA SOCIAL", url_google_sites)
    
