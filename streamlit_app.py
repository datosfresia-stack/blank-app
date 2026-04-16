import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="IA Libre Fresia", layout="wide")

st.title("🤖 IA Libre Fresia")
st.success("✅ ¡Sistema en línea y hablando español!")

# Cargamos una IA que entiende y escribe ESPAÑOL muy bien
@st.cache_resource
def cargar_ia():
    # Usamos un modelo entrenado para hablar
    return pipeline("text-generation", model="PlanTL-GOB-ES/gpt2-base-bpe-doccano")

ia = cargar_ia()

# ---------------- INTERFAZ ----------------
st.info("✍️ Escribe lo que quieras y te responderé")

with st.form(key="form_pregunta"):
    entrada = st.text_area("¿En qué te puedo ayudar?", height=100, placeholder="Escribe aquí tu mensaje...")
    enviar = st.form_submit_button("🚀 Enviar")
    
if enviar and entrada:
    with st.spinner("🧠 Pensando en español... un momento..."):
        try:
            # Le damos instrucciones claras
            prompt = f"Usuario: {entrada}\nAsistente: "
            
            resultado = ia(
                prompt, 
                max_length=100, 
                do_sample=True, 
                temperature=0.8, 
                top_p=0.9
            )[0]['generated_text']
            
            # Extraemos solo la respuesta
            respuesta_final = resultado.split("Asistente:")[-1]
            
            st.markdown("---")
            st.subheader("💬 Respuesta:")
            st.write(respuesta_final)
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.divider()
st.caption("FRESIA - Hecho con ❤️ e Inteligencia Artificial")
