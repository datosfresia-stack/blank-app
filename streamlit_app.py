import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer

st.set_page_config(page_title="IA Libre Fresia", layout="wide")

st.title("🤖 IA Libre Fresia")
st.success("✅ ¡Sistema en línea!")

# Cargamos un modelo hecho PARA CHATEAR (DialoGPT de Microsoft)
@st.cache_resource
def cargar_ia():
    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")
    return tokenizer, model

tokenizer, model = cargar_ia()

# ---------------- INTERFAZ ----------------
st.info("Escribe tu pregunta y presiona Enviar")

with st.form(key="form_pregunta"):
    entrada = st.text_input("¿Qué quieres saber?", value="Hola")
    enviar = st.form_submit_button("🚀 Enviar")
    
if enviar and entrada:
    with st.spinner("🧠 La IA está pensando..."):
        try:
            # Codificamos el mensaje
            input_ids = tokenizer.encode(entrada + tokenizer.eos_token, return_tensors='pt')
            
            # Generamos la respuesta
            respuesta_ids = model.generate(input_ids, max_length=50, pad_token_id=tokenizer.eos_token_id)
            respuesta = tokenizer.decode(respuesta_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
            
            st.markdown("---")
            st.subheader("💬 Respuesta:")
            st.write(respuesta)
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.divider()
st.caption("FRESIA - Red de Inteligencia Alternativa 🚀")
