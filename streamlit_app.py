import streamlit as st
import requests

# Configuración de la página
st.set_page_config(page_title="IA Fresia", layout="centered")

st.title("🤖 IA Libre Fresia")
st.write("Bienvenido al sistema de inteligencia comunitaria.")

# Tu llave de Hugging Face (Asegúrate que se llame HF_TOKEN en los Secrets)
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-Nemo-Instruct-2407"
if "HF_TOKEN" in st.secrets:
    headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}
else:
    st.error("⚠️ Falta el HF_TOKEN en los Secrets de Streamlit.")
    st.stop()

def buscar_respuesta(pregunta):
    payload = {"inputs": f"<s>[INST] {pregunta} [/INST]", "parameters": {"max_new_tokens": 500}}
    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=20)
        datos = r.json()
        if isinstance(datos, list):
            return datos[0]['generated_text'].split('[/INST]')[-1]
        elif "estimated_time" in str(datos):
            return f"⏳ El servidor está cargando. Estará listo en {int(datos['estimated_time'])} segundos. ¡Intenta de nuevo en un momento!"
        else:
            return "El servidor está ocupado. Prueba darle a 'Enter' otra vez."
    except:
        return "Conexión lenta. Intenta preguntar de nuevo."

# Entrada de texto
user_input = st.text_input("¿Qué quieres preguntar?")

if user_input:
    with st.spinner("Pensando..."):
        respuesta = buscar_respuesta(user_input)
        st.markdown("---")
        st.write(respuesta)

st.divider()
st.caption("Prensaenloslagos - Inteligencia Independiente")
