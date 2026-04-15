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
    .sidebar .sidebar-content { background-image: linear-gradient(#ffffff, #e3f2fd); }
    </style>
    """, unsafe_allow_html=True)

# 2. Base de Datos de Sabiduría (Estadísticas y Ciudades)
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
    
    st.header("📸 Anal

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if p := st.chat_input("¿Qué quieres mejorar hoy, Miguel?"):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"):
        st.markdown(p)
    
    with st.chat_message("assistant"):
        p_low = p.lower()
        
        # Lógica de consejos de salud
        if "peso" in p_low or "mejorar" in p_low or "pesa" in p_low:
            r = "Para mejorar los resultados de la pesa, Miguel, recuerda que en Fresia tenemos aire puro para caminar. Podríamos empezar con caminatas suaves de 20 minutos y priorizar el agua sobre otras bebidas. ¡Yo llevaré tu registro!"
        elif "foto" in p_low:
            r = "¡Recibí la imagen! Dame un momento para procesar los números. Recuerda pesarte siempre a la misma hora para que nuestra estadística sea exacta."
        elif "habitantes" in p_low or "osorno" in p_low or "fresia" in p_low:
            r = "Fresia tiene unos 12.800 habitantes, mientras que Osorno ronda los 160.000. ¡Somos un rincón tranquilo y privilegiado!"
        else:
            r = random.choice([
                "Estoy aquí para cuidarte, Miguel.",
                "¿Cómo te sientes hoy después de ver el verde de los árboles?",
                "Eres un gran ejemplo de constancia con tu salud.",
                "Dime qué más quieres que registre en mi diario."
            ])
            
        st.markdown(r)
        st.session_state.messages.append({"role": "assistant", "content": r})
        
