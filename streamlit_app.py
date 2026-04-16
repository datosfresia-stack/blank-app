import streamlit as st
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

st.set_page_config(page_title="IA Libre Fresia", layout="wide")

st.title("🤖 IA Libre Fresia")
st.success("✅ ¡Sistema en línea!")

# Cargamos modelo que funciona bien
@st.cache_resource
def cargar_ia():
    model_name = "datificate/gpt2-small-spanish"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return pipeline("text-generation", model=model, tokenizer=tokenizer)

ia = cargar_ia()

# ---------------- INTERFAZ ----------------
st.info("✍️ Escribe tu pregunta")

with st.form(key="form_pregunta"):
    entrada = st.text_area("¿Qué quieres saber?", height=100, placeholder="Escribe aquí...")
    enviar = st.form_submit_button("🚀 Enviar")
    
if enviar and entrada:
    with st.spinner("🧠 Pensando..."):
        try:
            # Generamos respuesta
            secuencia = ia(
                entrada,
                max_length=len(entrada) + 100,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                num_return_sequences=1
            )
            
            # Extraemos solo lo nuevo que escribió la IA
            texto_completo = secuencia[0]['generated_text']
            respuesta = texto_completo[len(entrada):].strip()
            
            st.markdown("---")
            st.subheader("💬 Respuesta:")
            st.write(respuesta)
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.divider()
st.caption("FRESIA - Inteligencia Artificial en Español 🇪🇸")
