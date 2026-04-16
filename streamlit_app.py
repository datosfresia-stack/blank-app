import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM

st.set_page_config(page_title="IA Libre Fresia", layout="wide")

st.title("🤖 IA Libre Fresia")
st.success("✅ ¡Sistema en línea!")

# 🇪🇸 MODELO QUE HABLA ESPAÑOL PERFECTO
@st.cache_resource
def cargar_ia():
    # Usamos un modelo entrenado para español e inglés
    tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-coder-1.3b-instruct")
    model = AutoModelForCausalLM.from_pretrained("deepseek-ai/deepseek-coder-1.3b-instruct")
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
            # Le decimos que actúe como un asistente amable
            prompt = f"### Instrucción:\nEres un asistente útil y amable. Responde en español.\n\n### Pregunta:\n{entrada}\n\n### Respuesta:\n"
            
            input_ids = tokenizer(prompt, return_tensors='pt').input_ids
            outputs = model.generate(input_ids, max_new_tokens=150, do_sample=True, top_p=0.95, temperature=0.7)
            respuesta = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Limpiamos para mostrar solo la respuesta
            respuesta_final = respuesta.split("### Respuesta:")[-1].strip()
            
            st.markdown("---")
            st.subheader("💬 Respuesta:")
            st.write(respuesta_final)
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.divider()
st.caption("FRESIA - Red de Inteligencia Alternativa 🚀")
