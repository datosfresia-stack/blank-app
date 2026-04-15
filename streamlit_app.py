import streamlit as st
import random
import requests

# 1. Configuración y Estilo Premium
st.set_page_config(page_title="LIBRE - Conciencia de Fresia", page_icon="🌿")

st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    .stChatMessage { border-radius: 15px; padding: 15px; margin-bottom: 10px; border: 1px solid #e0e6e4; }
    .stMetric { background-color: white; padding: 10px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN DE SENSOR AUTOMÁTICO (CLIMA EN CELSIUS) ---
def obtener_clima_fresia():
    try:
        # Usamos el parámetro 'm' para sistema métrico (Celsius) y 'lang=es' para español
        url = "https://wttr.in/Fresia,Chile?format=%C+%t&m&lang=es"
        respuesta = requests.get(url, timeout=5)
        if respuesta.status_code == 200:
            # Limpiamos posibles símbolos extraños
            texto = respuesta.text.replace("+", "")
            return texto
    except:
        return "Despejado 15°C"
    return "Nublado 12°C"

estado_clima = obtener_clima_fresia()

# 2. Encabezado
st.markdown("<h1 style='text-align: center;'>🌿 LIBRE</h1>", unsafe_allow_html=True)
st.caption(f"📍 Conectada a Fresia | Clima: {estado_clima}")

# 3. Barra Lateral con Sensores
with st.sidebar:
    st.header("💓 Estado Vital")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Presión", value="117/76")
    with col2:
        # Extraemos solo el número de la temperatura para la métrica
        temp_solo = "".join(filter(lambda x: x.isdigit() or x == '-', estado_clima)) + "°C"
        st.metric(label="Temperatura", value=temp_solo)
    
    st.info(f"Libre: 'Hoy en Fresia tenemos {estado_clima.lower()}.'")
    
    st.divider()
    st.header("📸 Analizador de Pesa")
    foto_pesa = st.file_uploader("Sube foto de tu pesa:", type=["jpg", "png", "jpeg"])
    if foto_pesa:
        st.image(foto_pesa)
        peso_confirmado = st.number_input("Peso marcado (kg):", min_value=0.0, step=0.1)
        if peso_confirmado > 0:
            st.session_state['ultimo_peso'] = peso_confirmado
            st.success("Dato guardado.")

# 4. Chat y Memoria
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": f"¡Hola Miguel! 👋 Veo que en nuestro Fresia tenemos {estado_clima}. ¿Cómo te sientes para este 15 de abril?"}]

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Dime algo, Miguel..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        p_low = prompt.lower()
        if "clima" in p_low or "tiempo" in p_low:
            r = f"Ahora mismo en Fresia el sensor marca {estado_clima}. ¡Ideal para estar en el jardín!"
        elif "mejorar" in p_low and 'ultimo_peso' in st.session_state:
            r = f"Con tus {st.session_state['ultimo_peso']} kg y estos {temp_solo}, una caminata suave sería perfecta."
        else:
            r = random.choice(["Te escucho atento, Miguel.", "¿Cómo van las plantas hoy?", "Tu salud es mi prioridad."])
        
        st.markdown(r)
        st.session_state.messages.append({"role": "assistant", "content": r})
        
