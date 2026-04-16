import streamlit as st
import requests

# 1. Configuración básica
st.set_page_config(page_title="IA Fresia")

# 2. Título (Esto debería aparecer SIEMPRE)
st.title("🤖 IA Libre Fresia")
st.write("Estado: Conectando con la red comunitaria...")

# 3. Función de conexión
def llamar_ia(pregunta):
    url = "https://api-inference.huggingface.co/models/mistralai/Mistral-Nemo-Instruct-2407"
    header = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}
    payload = {"inputs": f"<s>[INST] {pregunta} [/INST]"}
    try:
        r = requests.post(url, headers=header, json=payload, timeout=15)
        res = r.json()
        if isinstance(res, list):
            return res[0]['generated_text'].split('[/INST]')[-1]
        return "El servidor está despertando, intenta en 10 segundos."
    except:
        return "Error de conexión temporal."

# 4. Interfaz
if "HF_TOKEN" not in st.secrets:
    st.error("Error: No has puesto el HF_TOKEN en los Secrets.")
else:
    entrada = st.text_input("Haz tu pregunta:")
    if entrada:
        with st.spinner("Pensando..."):
            respuesta = llamar_ia(entrada)
            st.markdown("---")
            st.write(respuesta)
