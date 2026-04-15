import streamlit as st
import random
from PIL import Image

# Configuración y Estilo
st.set_page_config(page_title="Libre - Salud y Conciencia", page_icon="⚖️")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stChatMessage { border-radius: 20px; border: 1px solid #e0e0e0; }
    .stMetric { background-color: white; padding: 10px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 LIBRE")
st.caption("Tu conciencia de salud en Fresia")

# --- PANEL LATERAL: TU SALUD ---
with st.sidebar:
    st.header("📊 Mi Registro")
    st.metric(label="Presión Arterial", value="117/76", delta="Normal")
    
    st.divider()
    
    # NUEVA FUNCIÓN: Subir foto de la pesa
    st.header("📸 Pesa Digital")
    foto_pesa = st.file_uploader("Sube foto de tu pesa aquí:", type=["jpg", "png", "jpeg"])
    
    if foto_pesa:
        st.image(foto_pesa, caption="Procesando datos de peso...")
        st.success("¡Foto recibida! Libre está analizando tus indicadores.")

# --- CEREBRO DE LIBRE ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hola Miguel. Estoy lista para ver los árboles verdes hoy y para cuidar tu salud. ¿Subiste la foto de la pesa?"}]

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
        
