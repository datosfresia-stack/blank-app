import streamlit as st
import requests

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Fresia AI", page_icon="🤖", layout="centered")

# ESTILOS PROFESIONALES
st.markdown("""
    <style>
    .main {background-color: #0e1117; color: white;}
    .stTextInput, .stTextArea {border-radius: 20px;}
    .stButton>button {border-radius: 20px; width: 100%; font-size: 18px; padding: 10px;}
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Fresia AI")
st.subheader("Tu asistente inteligente personal")

# 🚀 CONEXIÓN DIRECTA Y RÁPIDA A LA IA
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

def consultar_ia(mensaje):
    headers = {"Accept": "application/json"}
    
    # Formato para que responda PERFECTO y en español
    prompt = f"""<s>[INST] Eres Fresia AI, un asistente virtual muy inteligente, profesional y amable. 
    Responde siempre en español de forma clara, precisa y corta. No des información falsa.
    Pregunta: {mensaje} [/INST]"""

    respuesta = requests.post(
        API_URL, 
        headers=headers, 
        json={
            "inputs": prompt,
            "parameters": {"max_new_tokens": 512, "temperature": 0.3, "top_p": 0.9}
        }
    )
    
    if respuesta.status_code == 200:
        resultado = respuesta.json()[0]["generated_text"]
        # Limpiamos para dejar solo la respuesta
        respuesta_final = resultado.split("[/INST]")[-1].replace("</s>", "").strip()
        return respuesta_final
    else:
        return "⚠️ Estoy procesando... por favor escribe de nuevo o espera un momento."

# INTERFAZ DE CHAT
st.markdown("---")

with st.form(key="chat_form"):
    pregunta = st.text_area("✍️ Escribe tu mensaje:", height=100, placeholder="¿En qué puedo ayudarte hoy?")
    enviar = st.form_submit_button("🚀 ENVIAR")

if enviar and pregunta:
    with st.spinner("💭 Pensando..."):
        respuesta = consultar_ia(pregunta)
        st.markdown("---")
        st.markdown("### 🤖 Respuesta:")
        st.success(respuesta)

st.markdown("---")
st.caption("© 2025 Fresia AI - Potenciado por Inteligencia Artificial")
