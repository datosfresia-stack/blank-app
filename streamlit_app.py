import streamlit as st
import requests

st.set_page_config(page_title="IA Libre Fresia")

st.title("🤖 IA Libre Fresia")
st.success("✅ ¡Sistema en línea!")

# Usaremos Gemma, que es de Google pero corre libre en Hugging Face (más rápido)
API_URL = "https://api-inference.huggingface.co/models/google/gemma-1.1-7b-it"
headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}

def llamar_ia(pregunta):
    # Formato para el modelo Gemma
    payload = {"inputs": pregunta, "parameters": {"max_new_tokens": 500}}
    try:
        # Le damos 60 segundos para responder (antes tenía 15)
        r = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        res = r.json()
        
        if isinstance(res, list):
            return res[0]['generated_text']
        elif "estimated_time" in str(res):
            return f"⏳ El cerebro está despertando... listo en {int(res['estimated_time'])} seg. ¡Dale a Enter de nuevo!"
        else:
            return "El servidor está ocupado. Intenta una vez más."
    except requests.exceptions.Timeout:
        return "La conexión tardó mucho. ¡Intenta preguntar de nuevo ahora que el servidor ya despertó!"
    except:
        return "Buscando señal..."

if "HF_TOKEN" not in st.secrets:
    st.error("Falta configurar el Token.")
else:
    entrada = st.text_input("Haz tu pregunta:")
    if entrada:
        with st.spinner("La IA de Fresia está pensando..."):
            respuesta = llamar_ia(entrada)
            st.markdown("---")
            st.write(respuesta)

st.divider()
st.caption("FRESIA - Red de Inteligencia Alternativa")
