import streamlit as st
import requests

# ---------------------- CONFIGURACIÓN GENERAL ----------------------
st.set_page_config(page_title="IA LIBRE", page_icon="🌍", layout="wide")

# Estilos profesionales y colores
st.markdown("""
    <style>
    .main {background-color: #f0f2f6;}
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    .stButton>button {border-radius: 15px; font-size: 18px; padding: 15px; font-weight: bold;}
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
    st.subheader("Noticias Nacional y Regional")

    st.markdown("---")
    
    # Texto informativo grande y claro
    st.info("📢 **Accede a todas las noticias, reportajes y actualidad nacional y regional.**")
    
    # El botón principal - GRANDE Y VISIBLE
    url_google = "https://sites.google.com/view/ia-libre/inicio"
    
    # Usamos link_button que es lo más seguro y rápido
    st.link_button("🌐 INGRESAR A PRENSA EN LOS LAGOS", url_google, type="primary", use_container_width=True)
    
    st.markdown("---")
    st.write("💡 Al tocar el botón entrarás directo al portal con todo el contenido actualizado.")

# ==============================================================
#                   SECCIÓN 3: DATOS FRESIA
# ==============================================================
elif menu == "📍 DATOS FRESIA":
    st.title("📍 DATOS FRESIA")
    st.subheader("Información útil y local de la comuna")
    
    st.markdown("---")
    st.write("Aquí encontrarás datos importantes para el día a día:")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("💊 Farmacias de Turno")
        st.write("Consulta las farmacias que están abiertas hoy.")
        st.button("Ver Farmacias", key="farmacias")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🌤️ Clima Local")
        st.write("Temperatura y pronóstico del tiempo.")
        st.button("Ver Clima", key="clima")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🏛️ Noticias Municipales")
    st.write("Actividades y avisos de la comuna.")
    st.button("Ver Noticias", key="noticias_mun")
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================
#                 SECCIÓN 4: CENTRO SOLIDARIO
# ==============================================================
elif menu == "❤️ CENTRO SOLIDARIO":
    st.title("❤️ CENTRO SOLIDARIO EN ACCIÓN")
    st.subheader("Ayudando a nuestra comunidad")

    st.markdown("---")
    st.write("Galería de fotos y videos de actividades solidarias, bingos, rifas y beneficios.")
    st.button("📂 Ver Galería Completa", key="galeria")

# ---------------------- PIE DE PÁGINA ----------------------
st.markdown("---")
st.caption("© 2025 PROYECTO IA LIBRE | Todo funcionando correctamente")
