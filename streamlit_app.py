import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DEL CEREBRO (API KEY)
# Usando la llave que acabas de generar
genai.configure(api_key="AIzaSyBERnyHBPNKai3y-IGtykVBaTal414UC7M")
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. CONFIGURACIÓN DE PÁGINA E IDENTIDAD
st.set_page_config(page_title="IA Libre", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    .stButton>button { background-color: #004d4d; color: white; border-radius: 10px; }
    .stTextInput>div>div>input { border: 2px solid #004d4d; }
    </style>
    """, unsafe_allow_html=True)

# 3. NAVEGACIÓN (LOS BRAZOS)
with st.sidebar:
    st.title("🌐 Menú IA Libre")
    menu = st.radio("Secciones:", ["🤖 IA LIBRE (CABEZA)", "📰 PRENSAENLOSLAGOS", "📍 DATOSFRESIA", "🤝 CENTRO SOLIDARIO"])
    st.divider()
    st.caption("Proyecto Multiplataforma - Fresia, Los Lagos")

url_google_sites = "https://sites.google.com/view/ia-libre/inicio"

# 4. LÓGICA DE FUNCIONAMIENTO
if menu == "🤖 IA LIBRE (CABEZA)":
    st.title("🤖 IA Libre: Asistente Universal")
    st.write("Consulta profesional: Medicina, Leyes, Inversiones y Traducciones.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Chat interactivo
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("¿En qué puedo asesorarte hoy?"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # LA IA RESPONDE DE VERDAD AQUÍ
                response = model.generate_content(prompt)
                full_response = response.text
                st.markdown(full_response)
                st.session_state.chat_history.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Hubo un problema al conectar con el cerebro: {e}")

elif menu == "📰 PRENSAENLOSLAGOS":
    st.title("📰 Prensaenloslagos")
    st.link_button("👉 VER NOTICIAS NACIONAL Y REGIONAL", url_google_sites)

elif menu == "📍 DATOSFRESIA":
    st.title("📍 DatosFresia")
    st.link_button("👉 VER DATOS LOCALES FRESIA", url_google_sites)

elif menu == "🤝 CENTRO SOLIDARIO":
    st.title("🤝 Centro Solidario en Acción")
    st.link_button("👉 VER CASOS SOCIALES", url_google_sites)
    
