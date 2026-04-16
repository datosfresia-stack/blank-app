import streamlit as st
import requests

st.set_page_config(page_title="IA Libre Fresia", page_icon="🌐")

st.title("🤖 IA Libre")
st.success("✅ Conectado a la Red Comunitaria (Llama 3)")

# Usamos el modelo más potente y nuevo de Meta (Llama 3) que es gratis en Hugging Face
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}

def consultar_ia(texto):
    prompt = f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\nResponde en español: {texto}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt, "parameters": {"max_new_tokens": 500}})
    return response.json()

if prompt := st.chat_input("¿En qué te puedo ayudar?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            resultado = consultar_ia(prompt)
            # Limpiamos la respuesta para mostrar solo lo que dijo la IA
            respuesta = resultado[0]['generated_text'].split('<|start_header_id|>assistant<|end_header_id|>\n\n')[-1]
            st.markdown(respuesta)
        except:
            st.error("El servidor está despertando. Reintenta en 10 segundos.")

st.divider()
st.caption("Tecnología Llama 3 - Acceso Abierto")
