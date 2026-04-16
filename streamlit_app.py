import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="IA Libre", page_icon="🤖", layout="wide")

# 2. CONEXIÓN AL CEREBRO (LLAVE)
# Probaremos con una lista de modelos por si uno falla
API_KEY = "AIzaSyBERnyHBPNKai3y-IGtykVBaTal414UC7M"
genai.configure(api_key=API_KEY)

# Lista de modelos para probar en orden de modernidad
modelos_a_probar = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']

if "modelo_seleccionado" not in st.session_state:
    st.session_state.modelo_seleccionado = None

# Buscamos cuál modelo está disponible para tu cuenta
if st.session_state.modelo_seleccionado is None:
    for nombre_modelo in modelos_a_probar:
        try:
            m = genai.GenerativeModel(nombre_modelo)
            # Prueba de fuego: un saludo corto
            m.generate_content("Hola", generation_config={"max_output_tokens": 1})
            st.session_state.modelo_seleccionado = nombre_modelo
            break 
        except:
            continue

# 3. INTERFAZ Y MENÚ
with st.sidebar:
    st.title("🌐 Portal IA Libre")
    menu = st.radio("Secciones:", ["🤖 IA LIBRE", "📰 NOTICIAS", "📍 FRESIA", "🤝 SOLIDARIO"])
    st.divider()
    if st.session_state.modelo_seleccionado:
        st.success(f"Cerebro: {st.session_state.modelo_seleccionado} ✅")
    else:
        st.error("Cerebro no encontrado ❌")

url_google_sites = "https://sites.google.com/view/ia-libre/inicio"

# 4. LÓGICA DE IA LIBRE
if menu == "🤖 IA LIBRE":
    st.title("🤖 IA Libre: Asistente Universal")
    
    if not st.session_state.modelo_seleccionado:
        st.error("No se pudo conectar con ningún modelo de Google. Revisa tu archivo requirements.txt")
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
                    modelo_final = genai.GenerativeModel(st.session_state.modelo_seleccionado)
                    response = modelo_final.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Error al generar respuesta: {e}")

# Resto de secciones abreviadas para velocidad
elif menu == "📰 NOTICIAS":
    st.link_button("👉 VER PRENSAENLOSLAGOS", url_google_sites)
elif menu == "📍 FRESIA":
    st.link_button("👉 VER DATOS FRESIA", url_google_sites)
elif menu == "🤝 SOLIDARIO":
    st.link_button("👉 VER CENTRO SOLIDARIO", url_google_sites)
    
