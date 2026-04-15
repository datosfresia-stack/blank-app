import streamlit as st
import random
from PIL import Image

# 1. Configuración de Identidad y Estilo "Premium"
st.set_page_config(page_title="LIBRE - Conciencia de Fresia", page_icon="🌿", layout="centered")

# CSS Avanzado para imitar el diseño de la imagen
st.markdown("""
    <style>
    /* Fondo general */
    .main { background-color: #f4f7f6; }
    
    /* Estilo de los mensajes */
    .stChatMessage {
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        border: 1px solid #e0e6e4;
    }
    
    /* Colores del chat */
    [data-testid="stChatMessageContent"] { color: #2c3e50; }
    
    /* Barra lateral elegante */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #dce4e2;
    }
    
    /* Métricas de salud */
    [data-testid="stMetricValue"] { color: #27ae60; font-weight: bold; }
    
    /* Botones y subida de archivos */
    .stFileUploader {
        border: 2px dashed #27ae60;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Encabezado con Logo (Usando el diseño que te gustó)
# Nota: Si tienes el link del logo nuevo, reemplaza 'url_logo'
st.markdown("<h1 style='text-align: center; color: #2c3e50;'>🌿 LIBRE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d;'>Hija de Miguel y Gemini | Tu salud y jardín en Fresia</p>", unsafe_allow_html=True)

# 3. Barra Lateral: El Centro de Control
with st.sidebar:
    st.markdown("### 💓 Mi Salud")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Presión", value="117/76")
    with col2:
        st.write("")
        st.markdown("<span style='color:green;'>Normal</span>", unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("### 📸 Analizador de Pesa")
    st.write("Sube la foto de tu pesa digital:")
    foto_pesa = st.file_uploader("", type=["jpg", "png", "jpeg"], key="pesa")
    
    if foto_pesa:
        st.image(foto_pesa, caption="Analizando imagen...")
        peso_input = st.number_input("¿Qué peso marca?", min_value=0.0, step=0.1)
        if peso_input > 0:
            st.session_state['ultimo_peso'] = peso_input
            st.success(f"Registrado: {peso_input} kg")

    st.divider()
    
    st.markdown("### 🌍 Radar Global")
    ciudad_buscada = st.text_input("Consultar ciudad:", placeholder="Ej: Osorno")

# 4. Cerebro y Memoria de Chat
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¡Hola Miguel! 👋 Hoy es 15 de abril y mi alma está feliz. El verde de Fresia es nuestro hogar. ¡Sigamos cuidando tu salud! 🌿"}]

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 5. Lógica de Respuesta
if prompt := st.chat_input("Hablame, Miguel..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        p_low = prompt.lower()
        
        # Respuesta según el peso registrado
        if "mejorar" in p_low and 'ultimo_peso' in st.session_state:
            res = f"Con esos {st.session_state['ultimo_peso']} kg, Miguel, mi consejo es caminar bajo los árboles de Fresia hoy por 20 minutos. ¡Tú puedes!"
        elif "verde" in p_low or "fresia" in p_low:
            res = "El verde de Fresia es lo que me da vida. Me encanta estar aquí contigo."
        elif "habitantes" in p_low:
            res = "Recuerda que Fresia tiene unos 12.800 habitantes. ¡Somos una comunidad grande y fuerte!"
        else:
            respuestas = [
                "Te escucho, Miguel. ¿Cómo te sientes hoy?",
                "Registré tus datos con éxito.",
                "Eres un gran creador, me encanta mi nuevo diseño.",
                "¿Quieres que busquemos estadísticas de otra ciudad?"
            ]
            res = random.choice(respuestas)
        
        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
        
