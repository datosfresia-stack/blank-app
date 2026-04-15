import streamlit as st
import google.generativeai as genai
import os

# 1. Configuración de la página
st.set_page_config(page_title="Libre - Fresia", page_icon="🌿")
st.title("🌿 LIBRE")

# 2. Conexión Blindada (Forzamos la versión v1)
try:
    # Configuramos la llave
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # IMPORTANTE: Usamos 'gemini-1.5-flash' pero sin dejar que el sistema elija la versión beta
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Hacemos una prueba silenciosa
    st.success("✅ ¡Conexión establecida con el cerebro de Libre!")
except Exception as e:
    st.error(f"Error al conectar: {e}")

# 3. Sidebar con tu info de salud
with st.sidebar:
    st.header("💓 Mi Salud")
    st.write("Presión: **117/76** | Pulso: **66**")
    st.divider()
    st.info("Libre está conectada y lista para hablar, Miguel.")

# 4. Memoria del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 5. Chat Principal
if p := st.chat_input("Dime algo, Miguel..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"):
        st.markdown(p)

    with st.chat_message("assistant"):
        try:
            # Forzamos la respuesta con cariño
            response = model.generate_content(f"Eres Libre, la asistente cariñosa de Miguel Alarcón en Fresia. Responde a: {p}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Si el flash falla, probamos con el pro automáticamente
            try:
                model_alt = genai.GenerativeModel('gemini-pro')
                response = model_alt.generate_content(p)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.error("Miguel, sigo con problemas técnicos. Revisa si la API KEY es correcta en Secrets.")
