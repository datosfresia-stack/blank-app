import streamlit as st
import requests
from datetime import datetime

# ---------------------- CONFIGURACIÓN GENERAL ----------------------
st.set_page_config(page_title="IA LIBRE", page_icon="🌍", layout="wide")

# Estilos profesionales y colores
st.markdown("""
    <style>
    .main {background-color: #f0f2f6;}
    .block-container {padding-top: 1rem; padding-bottom: 1rem;}
    .css-18e3th9 {padding-top: 2rem;}
    .stButton>button {width: 100%; border-radius: 10px; font-size: 16px; padding: 10px;}
    .card {background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

# ---------------------- MENÚ DE NAVEGACIÓN ----------------------
menu = st.sidebar.selectbox(
    "📂 MENU PRINCIPAL",
    ["🤖 IA LIBRE", "📰 PRENSA EN LOS LAGOS", "📍 DATOS FRESIA", "❤️ CENTRO SOLIDARIO"]
)

# ==============================================================
#                      SECCIÓN 1: IA LIBRE
# ==============================================================
if menu == "🤖 IA LIBRE":
    st.title("🤖 IA LIBRE")
    st.subheader("Tu asistente inteligente multiplataforma")
    st.success("✅ Sistema activo | Rápido y Preciso")

    st.markdown("---")
    
    # Conexión a IA potente
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

    def consultar_ia(mensaje):
        headers = {"Accept": "application/json"}
        prompt = f"""<s>[INST] Eres IA LIBRE, un asistente profesional, experto y muy útil.
        Conoces sobre economía, precios del dólar, inversiones, películas, traducciones, medicina, leyes, construcción, informática, marcas de ropa y geografía mundial.
        Responde siempre en ESPAÑOL, de forma clara, corta y profesional.
        Pregunta: {mensaje} [/INST]"""

        try:
            respuesta = requests.post(API_URL, headers=headers, json={"inputs": prompt, "parameters": {"max_new_tokens": 700, "temperature": 0.4}})
            if respuesta.status_code == 200:
                resultado = respuesta.json()[0]["generated_text"]
                return resultado.split("[/INST]")[-1].replace("</s>", "").strip()
            else:
                return "⏳ Procesando... por favor intenta nuevamente."
        except:
            return "🔌 Verificando conexión..."

    # Interfaz de chat
    with st.form(key="form_ia"):
        pregunta = st.text_area("✍️ ¿En qué te puedo ayudar hoy?", height=120, placeholder="Escribe tu consulta aquí...")
        enviar = st.form_submit_button("🚀 ENVIAR CONSULTA")

    if enviar and pregunta:
        with st.spinner("🧠 IA LIBRE pensando..."):
            respuesta = consultar_ia(pregunta)
            st.markdown("---")
            st.markdown("### 💬 Respuesta:")
            st.info(respuesta)

# ==============================================================
#                 SECCIÓN 2: PRENSA EN LOS LAGOS
# ==============================================================
elif menu == "📰 PRENSA EN LOS LAGOS":
    st.title("📰 PRENSA EN LOS LAGOS")
    st.image("https://i.imgur.com/yourlogo.png", width=300) # Aquí iría tu logo PLL
    st.subheader("Noticias Nacional y Regional")

    st.markdown("---")

    # Ejemplo de noticia (Fácil de agregar más)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📢 Título de Noticia Importante")
        st.caption(f"📅 {datetime.now().strftime('%d de %B, %Y')} | Región de Los Lagos")
        st.write("Aquí va el contenido de la noticia...")
        st.button("🔗 Compartir en Redes Sociales", key="1")
        st.markdown('</div>', unsafe_allow_html=True)

    st.info("💡 Tip: Para agregar noticias fácilmente, podemos conectar con Google Sites o un blog gratuito.")

# ==============================================================
#                   SECCIÓN 3: DATOS FRESIA
# ==============================================================
elif menu == "📍 DATOS FRESIA":
    st.title("📍 DATOS FRESIA")
    st.image("https://i.imgur.com/yourlogo2.png", width=300) # Aquí iría tu logo Ojo Mundo
    st.subheader("Información útil y local")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("💊 Farmacias de Turno")
        st.write("Consulta aquí las farmacias abiertas hoy.")
        st.button("Ver Listado", key="2")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🌤️ Clima Local")
        st.write("Temperatura y pronóstico del tiempo.")
        st.button("Ver Clima", key="3")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🏙️ Noticias Municipales")
    st.write("Actividades y avisos de la comuna.")
    st.button("📤 Compartir", key="4")
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================
#                 SECCIÓN 4: CENTRO SOLIDARIO
# ==============================================================
elif menu == "❤️ CENTRO SOLIDARIO":
    st.title("❤️ CENTRO SOLIDARIO EN ACCIÓN")
    st.subheader("Ayudando a nuestra comunidad")

    st.markdown("---")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📸 Galería de Actividades")
    st.write("Aquí se mostrarán fotos y videos de bingos, rifas y beneficios.")
    
    # Simulador de carga
    uploaded_file = st.file_uploader("Agregar nueva imagen o video", type=["jpg", "png", "mp4"])
    if uploaded_file:
        st.success("✅ Archivo listo para publicar")
    
    st.button("📢 Publicar Actividad", key="5")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- PIE DE PÁGINA ----------------------
st.markdown("---")
st.caption("© 2025 PROYECTO IA LIBRE | Desarrollado con tecnología de vanguardia")
