import streamlit as st
import requests
import time

st.set_page_config(page_title="IA Libre Fresia")

st.title("🤖 IA Libre")
st.success("Conexión con Servidor Comunitario")

# Usamos el modelo Nemo que es más rápido
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-Nemo-Instruct-2407"
headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}

def consultar_ia(texto):
    payload = {"inputs": f"<s>[INST] {texto} [/INST]", "parameters": {"max_new_tokens": 500}}
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        resultado = response.json()
        if isinstance(resultado, list):
            return resultado[0]['generated_text'].split('[/INST]')[-1]
        elif "estimated_time" in str(resultado):
            return f"DESPERTANDO: El servidor está cargando. Reintenta en {int(resultado['estimated_time'])} segundos."
        else:
            return "El servidor está ocupado. Intenta de nuevo en un momento."
    except:
        return "Error de conexión. Revisa tu señal."

# Interfaz simple sin bloques complejos para evitar errores de espacios
pregunta = st.text_input("Escribe tu consulta aquí:")

if pregunta:
    with st.spinner("La IA está pensando..."):
        respuesta = consultar_ia(pregunta)
        st.markdown("---")
        st.write(respuesta)

st.divider()
st.caption("FRESIA - IA Independiente")
