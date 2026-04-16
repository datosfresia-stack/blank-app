import streamlit as st
import requests

st.set_page_config(page_title="IA Libre Fresia", layout="wide")

st.title("🤖 IA Libre Fresia")
st.success("✅ ¡Sistema en línea!")

# ✅ MODELO PÚBLICO Y GRATIS (NO NECESITAS TOKEN)
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"

def llamar_ia(pregunta):
    # No necesitamos autorización, es público
    headers = {}
    
    payload = {
        "inputs": pregunta,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.7,
            "return_full_text": False
        }
    }
    
    try:
        respuesta = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        
        try:
            datos = respuesta.json()
        except:
            return f"❌ Error: {respuesta.text}"

        if isinstance(datos, list) and len(datos) > 0:
            return datos[0]['generated_text']
        elif isinstance(datos, dict) and "estimated_time" in datos:
            return f"⏳ El modelo está despertando... espera {int(datos['estimated_time'])} segundos y vuelve a preguntar."
        else:
            return f"Respuesta: {str(datos)}"
            
    except requests.exceptions.Timeout:
        return "⌛ Tardó mucho. Intenta de nuevo ahora."
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
