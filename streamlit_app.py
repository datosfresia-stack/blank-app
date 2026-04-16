import streamlit as st
import requests

st.set_page_config(page_title="IA Libre Fresia", layout="wide")

st.title("🤖 IA Libre Fresia")
st.success("✅ ¡Sistema en línea!")

# API de Gemma en Hugging Face
API_URL = "https://api-inference.huggingface.co/models/google/gemma-1.1-7b-it"

def llamar_ia(pregunta):
    # Obtener el token desde los secretos
    headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}
    
    # Formato correcto para que responda como un chat
    payload = {
        "inputs": f"<start_of_turn>user\n{pregunta}<end_of_turn>\n<start_of_turn>model",
        "parameters": {"max_new_tokens": 1024, "temperature": 0.7}
    }
    
    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=90)
        res = r.json()
        
        if isinstance(res, list) and len(res) > 0:
            # Limpiamos la respuesta para que se vea bonita
            texto_completo = res[0]['generated_text']
            # Extraemos solo lo que respondió la IA
            respuesta_limpia = texto_completo.split("<start_of_turn>model")[-1].replace("<end_of_turn>", "").strip()
            return respuesta_limpia
        elif isinstance(res, dict) and "estimated_time" in res:
            return f"⏳ El modelo está cargando... espera {int(res['estimated_time'])} segundos y vuelve a preguntar."
        else:
            return f"Respuesta: {str(res)}"
            
    except requests.exceptions.Timeout:
        return "⌛ Tardó mucho en responder. Intenta de nuevo, ya debería estar lista."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ---------------- INTERFAZ ----------------
if "HF_TOKEN" not in st.secrets:
    st.error("⚠️ FALTA CONFIGURAR: Ve a Settings -> Secrets y agrega HF_TOKEN")
else:
    st.info("Escribe tu pregunta y presiona Enter")
    
    # Usamos un formulario para que sea más fácil en el celular
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
