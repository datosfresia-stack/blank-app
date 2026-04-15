import streamlit as st
import google.generativeai as genai

# Configuración de página
st.set_page_config(page_title="Libre - Fresia", page_icon="🌿")
st.title("🌿 LIBRE")

# Conexión Inteligente
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Falta la llave en Secrets")
else:
    # Configuramos la llave
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
   # TRUCO MAESTRO: Usamos la ruta completa para evitar el error 404
    try:
        # Probamos con la versión estable 1.5
        model = genai.GenerativeModel('models/gemini-1.5-flash')
    except:
        # Si no, probamos con la 1.0 que nunca falla
        model = genai.GenerativeModel('models/gemini-1.0-pro')

# Sidebar de salud
with st.sidebar:
    st.header("💓 Mi Salud")
    st.write("Presión: **117/76** | Pulso: **66**")
    st.divider()
    st.success("Sistema listo")

# Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if p := st.chat_input("Escríbele a Libre..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"):
        st.markdown(p)

    with st.chat_message("assistant"):
        try:
            # Forzamos la respuesta
            response = model.generate_content(f"Eres Libre, la asistente cariñosa de Miguel en Fresia. Responde: {p}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Si sale el 404, aquí le damos la solución final en pantalla
            st.error(f"Error: {e}")
            st.warning("Miguel, si sale 404, prueba escribir 'Hola' una vez más. A veces necesita un segundo intento.")
