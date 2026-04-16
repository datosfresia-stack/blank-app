import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="IA Libre Fresia", layout="wide")

st.title("🤖 IA Libre Fresia")
st.success("✅ ¡Sistema en línea y hablando español!")

# 🇪🇸 MODELO SEGURO Y LIGERO
@st.cache_resource
def cargar_ia():
    # Usamos "DistilGPT2" pero configurado para que responda bien
    return pipeline(
        "text-generation",
        model="distilgpt2",
        max_new_tokens=100
    )

ia = cargar_ia()

# ---------------- INTERFAZ ----------------
st.info("✍️ Escribe lo que quieras y te responderé")

with st.form(key="form_pregunta"):
    entrada = st.text_area("¿En qué te puedo ayudar?", height=100, placeholder="Escribe aquí tu mensaje...")
    enviar = st.form_submit_button("🚀 Enviar")
    
if enviar and entrada:
    with st.spinner("🧠 Pensando... un momento..."):
        try:
            # Instrucciones para que responda en español
            prompt = f"""
            Usuario: {entrada}
            Asistente: Eres un asistente amable y útil. Responde en español de forma clara y corta.
            """
            
            resultado = ia(
                prompt,
                do_sample=True,
                temperature=0.7,
                top_p=0.9
            )[0]['generated_text']
            
            # Limpiamos la respuesta
            respuesta_final = resultado.split("Asistente:")[-1].strip()
            
            st.markdown("---")
            st.subheader("💬 Respuesta:")
            st.write(respuesta_final)
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.divider()
st.caption("FRESIA - Hecho con ❤️ e Inteligencia Artificial")
