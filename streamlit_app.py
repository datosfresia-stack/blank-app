import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="IA Libre Fresia", layout="wide")

st.title("🤖 IA Libre Fresia")
st.success("✅ ¡Sistema en línea!")

# Cargamos el modelo directamente (no necesita internet extra ni tokens)
@st.cache_resource
def cargar_ia():
    return pipeline("text-generation", model="gpt2")

ia = cargar_ia()

# ---------------- INTERFAZ ----------------
st.info("Escribe tu pregunta y presiona Enviar")

with st.form(key="form_pregunta"):
    entrada = st.text_area("¿Qué quieres saber?", height=100)
    enviar = st.form_submit_button("🚀 Enviar")
    
if enviar and entrada:
    with st.spinner("🧠 La IA está pensando... (Primera vez tarda un poco más)"):
        try:
            # Generamos respuesta
            resultado = ia(entrada, max_length=200, temperature=0.7)[0]['generated_text']
            
            st.markdown("---")
            st.subheader("💬 Respuesta:")
            st.write(resultado)
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.divider()
st.caption("FRESIA - Red de Inteligencia Alternativa 🚀")
