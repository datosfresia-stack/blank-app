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
    
    # Logo PLL
    st.image("https://i.imgur.com/yourlogo.png", width=300, caption="Prensa en Los Lagos")
    
    st.subheader("🔗 Accediendo al portal de noticias...")
    
    # Enlace directo a Google Sites
    url_google_sites = "https://sites.google.com/view/ia-libre/inicio"
    
    st.info("📤 Toca el botón de abajo para ver todas las noticias y contenido actualizado:")
    
    st.link_button("🌐 IR A PRENSA EN LOS LAGOS", url_google_sites, type="primary", use_container_width=True)
    
    st.markdown("---")
    st.write("📝 **Instrucción:** Tú puedes seguir subiendo fotos, artículos y noticias directamente en tu Google Sites. Aquí solo es el acceso directo.")

# ==============================================================
#                   SECCIÓN 3: DATOS FRESIA
# ==============================================================
elif menu == "📍 DATOS FRESIA":
    st.title("📍 DATOS FRESIA")
    
    # Logo Datos Fresia
    st.image("https://i.imgur.com/yourlogo2.png", width=300, caption="Datos Fresia")
    
    st.subheader("Información útil y local")
    
    st.info("🔗 Aquí también podemos conectarlo a tu Google Sites o dejarlo como panel.")
    
    # Ejemplo de enlaces rápidos
    col1, col2 = st.columns(2)
    with col1:
        st.button("💊 Farmacias de Turno", key="2")
    with col2:
        st.button("🌤️ Clima Local", key="3")

# ==============================================================
#                 SECCIÓN 4: CENTRO SOLIDARIO
# ==============================================================
elif menu == "❤️ CENTRO SOLIDARIO":
    st.title("❤️ CENTRO SOLIDARIO EN ACCIÓN")
    st.subheader("Ayudando a nuestra comunidad")

    st.markdown("---")
    st.write("📸 Espacio para mostrar fotos y videos de actividades solidarias, bingos, rifas y beneficios.")
    
    # Aquí podemos poner otro enlace a Google Sites si quieres
    st.button("📂 Ver Galería Completa", key="5")

# ---------------------- PIE DE PÁGINA ----------------------
st.markdown("---")
st.caption("© 2025 PROYECTO IA LIBRE | Trabajando con Google Sites")
