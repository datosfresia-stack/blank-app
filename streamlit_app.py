import streamlit as st
import requests

st.set_page_config(page_title="IA Libre Fresia")

st.title("🤖 IA Libre Fresia")
st.success("✅ ¡El sistema está vivo y conectado!")

# Usaremos un modelo que suele estar siempre activo
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}

def consultar_ia(texto):
    # Formato optimizado para este modelo
    prompt = f"<|user|>\n{texto}</s>\n<|assistant|>\n"
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 500, "temperature": 0.7}}
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=20)
        resultado = response.json()
        
        if isinstance(resultado, list):
            # Limpiamos la respuesta
            full_text = resultado[0]['generated_text']
            return full_text.split("<|assistant|>\n")[-1]
        elif "estimated_time" in str(resultado):
            return f"⏳ El cerebro está cargando. Estará listo en {int(resultado['estimated_time'])} segundos. ¡Intenta de nuevo ahora!"
        else:
            return "El servidor está un poco ocupado, reintenta en un momento."
    except:
        return "Buscando señal de la red comunitaria..."

# Entrada de usuario
pregunta = st.text_input("Haz tu consulta a la IA:")

if pregunta:
    with st.spinner("La IA está redactando la respuesta..."):
        respuesta = consultar_ia(pregunta)
        st.markdown("---")
        st.write(respuesta)

st.divider()
st.caption("FRESIA - Inteligencia Alternativa Independiente")
