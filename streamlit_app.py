import streamlit as st
import requests
import time

st.set_page_config(page_title="IA Libre Fresia")

st.title("🤖 IA Libre")
st.success("Conexión con Servidor Comunitario")

# USAMOS MISTRAL: Es mucho más liviano y rápido para despertar
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}

def consultar_ia(texto):
    # Formato simple para Mistral
    payload = {"inputs": f"<s>[INST] Responde en español: {texto} [/INST]", "parameters": {"max_new_tokens": 500}}
    
    # Intentamos 3 veces automáticamente si el servidor está dormido
    for i in range(3):
        response = requests.post(API_URL, headers=headers, json=payload)
        resultado = response.json()
        
        # Si la respuesta es una lista, es que funcionó
        if isinstance(resultado, list):
            return resultado[0]['generated_text'].split('[/INST]')[-1]
        
        # Si hay error de carga, esperamos y reintentamos
        if "estimated_time" in str(resultado):
            tiempo_espera = int(resultado.get("estimated_time", 10))
            st.warning(f"El cerebro se está encendiendo... (esperando {tiempo_espera}s)")
            time.sleep(tiempo_espera)
        else:
            break
    return "El servidor sigue muy ocupado. Prueba darle clic al botón de nuevo."

if prompt := st.chat_input("Escribe tu consulta:"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("La IA está despertando..."):
            respuesta = consultar_ia(prompt)
            st.markdown(respuesta)

st.divider()
st.caption("FRESIA - Red de Inteligencia Alternativa")
