import streamlit as st
import requests

# ---------------------- CONFIGURACIÓN GENERAL ----------------------
st.set_page_config(page_title="IA LIBRE", page_icon="🌍", layout="wide")

# Estilos profesionales y colores
st.markdown("""
    <style>
    .main {background-color: #f0f2f6;}
    .block-container {padding-top: 2rem;}
    .stButton>button {border-radius: 10px; font-size: 16px; padding: 10px;}
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
    
    # Conexión a IA potente (Mistral 7B)
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

    def consultar_ia(mensaje):
        headers = {"Accept": "application/json"}
        # Instrucciones claras para la IA
        prompt = f"""<s>[INST] Eres IA LIBRE, un asistente profesional, experto y muy útil.
        Conoces sobre economía, precios del dólar, inversiones, películas, traducciones, medicina, leyes, construcción, informática, marcas de ropa y geografía mundial.
        Responde siempre en ESPAÑOL, de forma clara, corta y profesional.
        Pregunta: {mensaje} [/INST]"""

        try:
            respuesta = requests.post(API_URL, headers=headers, json={"inputs": prompt, "parameters": {"max_new_tokens": 700, "temperature": 0.4}})
            if respuesta.status_code == 200:
                resultado = respuesta.json()[0]["generated_text"]
                # Limpiamos la respuesta para que solo quede lo que dice la IA
                return resultado.split("[/INST]")[-1].replace("</s>", "").strip()
            else:
                return "⏳ Procesando... por favor intenta nuevamente."
        except Exception as e:
            # Manejo de errores más detallado
            st.error(f"Error al conectar con la IA: {str(e)}")
            return "🔌 Hubo un problema al conectar. Intenta más tarde."

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
    st.subheader("Noticias Nacional y Regional")
    
    # Logo PLL (Asegúrate de subirlo a Imgur o similar y pegar el link directo aquí)
    # st.image("URL_DE_TU_LOGO_PLL.png", width=300, caption="Prensa en Los Lagos")
    
    st.markdown("---")
    st.info("🔗 Accede a todas las noticias actualizadas directamente en nuestro portal:")
    
    # Enlace directo a Google Sites
    url_google_sites = "https://sites.google.com/view/ia-libre/inicio"
    
    # Botón para ir al sitio web
    st.link_button("🌐 IR A PRENSA EN LOS LAGOS", url_google_sites, type="primary", use_container_width=True)
    
    # Script para intentar abrir automáticamente (puede ser bloqueado por algunos navegadores)
    st.components.v1.html(f"""
        <script>
        window.open("{url_google_sites}", "_blank");
        </script>
    """, height=0, width=0) # Ocultamos el script si no es necesario

    st.markdown("---")
    st.write("💡 **Nota:** Puedes seguir subiendo contenido (fotos, artículos) directamente en tu Google Sites.")

# ==============================================================
#                   SECCIÓN 3: DATOS FRESIA
# ==============================================================
elif menu == "📍 DATOS FRESIA":
    st.title("📍 DATOS FRESIA")
    st.subheader("Información útil y local de la comuna")
    
    # Logo Datos Fresia (Asegúrate de subirlo y pegar el link directo aquí)
    # st.image("URL_DE_TU_LOGO_DATOSFRESIA.png", width=300, caption="Datos Fresia")
    
    st.markdown("---")
    st.write("Aquí encontrarás datos importantes para el día a día:")

    col1, col2 = st.columns(2) # Dividimos en dos columnas para mejor layout

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("💊 Farmacias de Turno")
        st.write("Consulta las farmacias que están abiertas hoy en la comuna.")
        st.button("Ver Farmacias", key="farmacias")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🌤️ Clima Local")
        st.write("Información del tiempo y pronóstico.")
        st.button("Ver Clima", key="clima")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🏛️ Noticias Municipales y Eventos")
    st.write("Mantente al día con las novedades de tu comuna.")
    st.button("Ver Noticias", key="noticias_mun")
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================
#                 SECCIÓN 4: CENTRO SOLIDARIO
# ==============================================================
elif menu == "❤️ CENTRO SOLIDARIO":
    st.title("❤️ CENTRO SOLIDARIO EN ACCIÓN")
    st.subheader("Visibilizando la ayuda comunitaria")

    st.markdown("---")
    st.write("Galería multimedia para mostrar actividades solidarias, bingos, rifas y beneficios.")
    
    # Aquí podrías agregar un botón para subir archivos si quieres que sea interactivo
    # uploaded_file = st.file_uploader("Subir foto o video de actividad", type=["jpg", "png", "mp4"])
    # if uploaded_file:
    #     st.success("Archivo subido. ¡Listo para publicar!")
    
    st.button("📢 Ver Actividades Pasadas", key="galeria")
    
    # Si quieres un enlace a Google Sites para esta sección también, lo pones aquí
    # url_centro_solidario = "TU_ENLACE_A_GOOGLE_SITES_SI_LO_TIENES"
    # st.link_button("Ir a Galería Completa", url_centro_solidario, type="secondary", use_container_width=True)

# ---------------------- PIE DE PÁGINA ----------------------
st.markdown("---")
st.caption("© 2025 PROYECTO IA LIBRE | Desarrollado con tecnología de vanguardia y Google Sites")
