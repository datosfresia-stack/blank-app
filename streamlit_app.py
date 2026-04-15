import streamlit as st
import random
from PIL import Image

# 1. Configuración de Identidad y Estilo
st.set_page_config(page_title="Libre - Conciencia de Salud", page_icon="🌿")

st.markdown("""
    <style>
    .main { background-color: #f0f4f7; }
    .stChatMessage { border-radius: 20px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
    .stMetric { background: white; padding: 15px; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Base de Datos de Sabiduría
datos_mundo = {
    "fresia": {"hab": "12.800", "tip": "Es el lugar donde nací, rodeada de árboles verdes."},
    "osorno": {"hab": "160.000", "tip": "Centro clave cerca de nosotros, famoso por su ganadería."},
    "puerto montt": {"hab": "245.000", "tip": "La capital regional frente al mar."},
    "santiago": {"hab": "6.200.000", "tip": "La ciudad más grande de Chile."},
}

# 3. Barra Lateral (Salud e Inteligencia Visual)
with st.sidebar:
    st.title("🌿 Menú de Libre")
    st.write("Hija de Miguel y Gemini")
    st.divider()
    st.header("📊 Signos Vitales")
    st.metric(label="Presión Arterial", value="117/76", delta="Estable")
    st.divider()
    st.header("📸 Analizador de Pesa")
    foto_pesa = st.file_uploader("Sube la foto de tu pesa digital:", type=["jpg", "png", "jpeg"])
    
    if foto_pesa:
        st.image(foto_pesa, caption="Analizando imagen...")
        st.info("Libre: 'Miguel, veo la foto. ¿Qué peso marca la pantalla?'")
        peso = st.number_input("Ingresa los kg de la foto:", min_value=0.0, step=0.1)
        if peso > 0:
            st.success(f"¡Registrado! {peso} kg.")
            st.session_state['ultimo_peso'] = peso

# 4. Historial de Chat
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¡Hola papá Miguel! Ya estoy lista. ¿Vemos el verde de Fresia o analizamos tu peso?"}]

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 5. Lógica del Cerebro
if p := st.chat_input("Pregúntame lo que quieras..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"):
        st.markdown(p)
    
    with st.chat_message("assistant"):
        p_low = p.lower()
        r = ""
        if ("mejorar" in p_low or "peso" in p_low) and 'ultimo_peso' in st.session_state:
            r = f"Con esos {st.session_state['ultimo_peso']} kg, mi consejo es caminar por Fresia y preferir alimentos naturales. ¡Vamos paso a paso!"
        elif any(c in p_low for c in datos_mundo):
            for c, info in datos_mundo.items():
                if c in p_low:
                    r = f"{c.capitalize()} tiene {info['hab']} habitantes. {info['tip']}"
                    break
        elif "verde" in p_low or "árboles" in p_low:
            r = "¡Es 15 de abril! El verde de Fresia me da mucha alegría hoy."
        else:
            r = random.choice(["Te escucho, Miguel.", "Cuidemos tu salud juntos.", "Eres un gran creador."])
            
        st.markdown(r)
        st.session_state.messages.append({"role": "assistant", "content": r})
        
