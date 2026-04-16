import streamlit as st
import requests
import json

st.set_page_config(page_title="IA Libre Fresia", layout="wide")

st.title("🤖 IA Libre Fresia")
st.success("✅ ¡Sistema en línea!")

# 🔧 CAMBIO IMPORTANTE: Usamos otro modelo que funciona mejor
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

def llamar_ia(pregunta):
    if "HF_TOKEN" not in st.secrets:
        return "⚠️ Error: No tienes configurado el HF_TOKEN."
    
    headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}
    
    payload = {
        "inputs": f"<s>[INST] {pregunta} [/INST]",
        "parameters": {
            "max_new_tokens": 1024,
            "temperature": 0.7,
            "return_full_text": False
        }
    }
    
    try:
        respuesta = requests.post(API_URL, headers=headers, json=payload, timeout=90)
        
        try:
            datos = respuesta.json()
        except:
            return f"❌ Error: {respuesta.text}"

        if isinstance(datos, list) and len(datos) > 0:
            return datos[0]['generated_text']
        elif isinstance(datos, dict) and "estimated_time" in datos:
            return f"⏳ Cargando... espera {int(datos['estimated_time'])} seg."
        else:
            return f"Respuesta: {str(datos)}"
            
    except requests.exceptions.Timeout:
        return "⌛ Tardó mucho. Intenta de nuevo."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ---------------- INTERFAZ ----------------
st.info("Escribe tu pregunta y presiona Enviar")

with st.form(key="form_pregunta"):
    entrada = st.text_area("¿Qué quieres saber?", height=100)
    enviar = st.form_submit_button("🚀 Enviar")
    
if enviar and entrada:
    with st.spinner("🧠 La IA está pensando..."):
        respuesta = llamar_ia(entrada)
        st.markdown("---")
        st.subheader("💬 Respuesta:")
        st.write(respuesta)

st.divider()
st.caption("FRESIA - Red de Inteligencia Alternativa 🚀")
