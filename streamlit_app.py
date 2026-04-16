import streamlit as st
import requests

# ---------------------- CONFIGURACIÓN GENERAL ----------------------
st.set_page_config(page_title="IA LIBRE", page_icon="🌍", layout="wide")

# ---------------------- MENÚ EN PESTAÑAS HORIZONTALES ----------------------
tab1, tab2, tab3, tab4 = st.tabs(["🤖 IA LIBRE", "📰 PRENSA", "📍 DATOS FRESIA", "❤️ SOLIDARIO"])

# ==============================================================
#                      PESTAÑA 1: IA LIBRE
# ==============================================================
with tab1:
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
                return "⏳ Procesando..."
        except:
            return "🔌 Conectando..."

    with st.form(key="form_ia"):
        pregunta = st.text_area("✍️ ¿En qué te puedo ayudar hoy?", height=120, placeholder="Escribe tu consulta aquí...")
        enviar = st.form_submit_button("🚀 ENVIAR CONSULTA")

    if enviar and pregunta:
        with st.spinner("🧠 Pensando..."):
            respuesta = consultar_ia(pregunta)
            st.markdown("---")
            st.markdown("### 💬 Respuesta:")
            st.info(respuesta)

# ==============================================================
#                      PESTAÑA 2: PRENSA
# ==============================================================
with tab2:
    st.title("📰 PRENSA EN LOS LAGOS")
    st.subheader("Noticias Nacional y Regional")

    st.markdown("---")
    
    url_google = "https://sites.google.com/view/ia-libre/inicio"
    
    st.markdown("### 👇 TOCA AQUÍ PARA ENTRAR")
    
    # Este botón abre en la MISMA VENTANA
    st.link_button("🌐 INGRESA A PRENSA EN LOS LAGOS", url_google, type="primary", use_container_width=True)
    
    st.markdown("---")
    st.write("💡 Al tocar el botón entrarás directo al portal.")

# ==============================================================
#                      PESTAÑA 3: DATOS FRESIA
# ==============================================================
with tab3:
    st.title("📍 DATOS FRESIA")
    st.subheader("Información útil y local de la comuna")
    st.markdown("---")
    st.write("Aquí encontrarás datos importantes para el día a día:")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💊 Farmacias de Turno")
        st.write("Consulta las farmacias que están abiertas hoy.")
    with col2:
        st.subheader("🌤️ Clima Local")
        st.write("Temperatura y pronóstico del tiempo.")
    st.subheader("🏛️ Noticias Municipales")
    st.write("Actividades y avisos de la comuna.")

# ==============================================================
#                      PESTAÑA 4: CENTRO SOLIDARIO
# ==============================================================
with tab4:
    st.title("❤️ CENTRO SOLIDARIO EN ACCIÓN")
    st.subheader("Ayudando a nuestra comunidad")
    st.markdown("---")
    st.write("Galería de fotos y videos de actividades solidarias.")

# ---------------------- PIE DE PÁGINA ----------------------
st.markdown("---")
st.caption("© 2025 PROYECTO IA LIBRE")
