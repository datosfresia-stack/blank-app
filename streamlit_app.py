import streamlit as st
import google.generativeai as genai
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import json
import os

st.set_page_config(page_title="Libre - Conectada", page_icon="🌿")
st.title("🌿 LIBRE: Acceso a Drive")

# 1. Configuración de Inteligencia
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Falta API KEY")

# 2. Configuración de Google Drive (OAuth)
def autenticar_drive():
    if not os.path.exists('credentials.json'):
        st.error("No se encuentra el archivo credentials.json")
        return None
    
    # Configuración del flujo de permiso
    flow = Flow.from_client_secrets_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/drive.readonly'],
        redirect_uri='https://datosfresia-stack.streamlit.app/_stcore/host-auth-response'
    )
    
    auth_url, _ = flow.authorization_url(prompt='consent')
    st.link_button("🔑 Conectar mi Google Drive con Libre", auth_url)

# Interfaz
st.info("Hola Miguel, para que pueda ver tus archivos de Fresia, necesito que me des permiso.")
autenticar_drive()

if p := st.chat_input("¿Qué quieres que busque en tu Drive?"):
    with st.chat_message("assistant"):
        st.write("Una vez que me des permiso arriba, podré analizar tus archivos.")
