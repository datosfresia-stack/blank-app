import streamlit as st
import requests

st.set_page_config(page_title="IA Libre Fresia")

st.title("🤖 IA Libre")
st.success("✅ Sistema conectado a la red comunitaria")

# Mantenemos el modelo Nemo que es el más estable
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-Nemo-Instruct-2407"
headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}

def consultar_ia(texto):
    payload = {"inputs": f"<s>[INST] {texto} [/INST]", "parameters": {"max_new_tokens": 500}}
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        resultado = response.json()
        
        if isinstance(resultado, list):
            return resultado[0]['generated_text'].split('[/INST]')[-1]
        elif "estimated_time" in str(resultado):
            return f"⏳ El cerebro está despertando... Reintenta en {int(resultado['estimated_time'])} segundos. ¡No te rindas!"
        else:
            return "⚠️ El servidor está muy solicitado ahora. Dale un segundo y vuelve a preguntar."
    except Exception as e:
        return f"Buscando señal... reintenta en un momento."

# Interfaz limpia
pregunta = st.text_input("Escribe tu consulta para Fresia:")

if pregunta:
    with st.spinner("Conectando con la IA..."):
        respuesta = consultar_ia(pregunta)
        st.markdown("---")
        st.write(respuesta)

st.divider()
st.caption("FRESIA - Inteligencia Local Independiente")
