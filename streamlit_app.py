import streamlit as st
import google.generativeai as genai

# 1. Configuración de pantalla
st.set_page_config(page_title="IA Libre Fresia", page_icon="🤖")

# 2. Conexión a la IA
# Asegúrate de que tu clave nueva (1w5A) esté en los 'Secrets' de Streamlit
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # Intentamos despertar al modelo
        model = genai.GenerativeModel('gemini-1.5-flash')
        ia_lista = True
    else:
        ia_lista = False
        st.warning("⚠️ Configura la clave en los Secrets de Streamlit.")
except Exception as e:
    ia_lista = False
    st.error(f"Error de inicio: {e}")

# 3. Interfaz de Usuario
st.title("🤖 IA Libre")
st.caption("Conectado al cerebro de Google (v1.5 Flash)")

if ia_lista:
    # Usamos una caja de texto simple
    pregunta = st.text_input("¿Qué deseas consultar hoy?", placeholder="Escribe aquí...")
    
    if pregunta:
        with st.spinner("La IA está procesando tu consulta..."):
            try:
                # Intento de respuesta estándar
                response = model.generate_content(pregunta)
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                # Si la librería es vieja, nos dirá el error aquí
                st.error("Error al obtener respuesta.")
                st.info(f"Detalle técnico: {e}")

# Pie de página
st.divider()
st.link_button("🌐 Portal Prensaenloslagos", "https://sites.google.com/view/ia-libre/inicio")
