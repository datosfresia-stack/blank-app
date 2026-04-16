import streamlit as st
import requests

# ---------------------- CONFIGURACIÓN GENERAL ----------------------
st.set_page_config(page_title="IA LIBRE", page_icon="🌍", layout="wide")

# Estilos
st.markdown("""
    <style>
    .main {background-color: #f0f2f6;}
    .block-container {padding-top: 2rem;}
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
    st.subheader("Redireccionando al portal de noticias...")
    
    # 👇 ESTO ES LO IMPORTANTE: Código mágico para abrir el link
    url_google = "https://sites.google.com/view/ia-libre/inicio"
    
    # Botón grande
    st.link_button("🌐 IR AL SITIO WEB", url_google, type="primary", use_container_width=True)
    
    # Texto informativo
    st.info("Si no se abre solo, toca el botón verde de arriba.")
    
    # Script para intentar abrir automáticamente
    st.components.v1.html(f"""
        <script>
        window.open("{url_google}", "_blank");
        </script>
    """, height=0)

# ==============================================================
#                   SECCIÓN 3: DATOS FRESIA
# ==============================================================
elif menu == "📍 DATOS FRESIA":
    st.title("📍 DATOS FRESIA")
    st.subheader("Información útil y local")
    st.write("Aquí irán farmacias, clima y noticias municipales.")

# ==============================================================
#                 SECCIÓN 4: CENTRO SOLIDARIO
# ==============================================================
elif menu == "❤️ CENTRO SOLIDARIO":
    st.title("❤️ CENTRO SOLIDARIO EN ACCIÓN")
    st.subheader("Ayudando a nuestra comunidad")
    st.write("Galería de fotos y videos de actividades solidarias.")

# ---------------------- PIE DE PÁGINA ----------------------
st.markdown("---")
st.caption("© 2025 PROYECTO IA LIBRE | Integrado con Google Sites")
