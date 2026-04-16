import streamlit as st

# 1. CONFIGURACIÓN
st.set_page_config(page_title="IA Libre", page_icon="🤖")

# 2. ESTILO PARA LOS BOTONES (Basado en tus logos verde petróleo)
st.markdown("""
    <style>
    .stButton>button {
        background-color: #004d4d;
        color: white;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. MENÚ LATERAL
st.sidebar.title("Navegación")
menu = st.sidebar.radio("Ir a:", ["🤖 IA LIBRE", "📰 PRENSAENLOSLAGOS", "📍 DATOSFRESIA", "🤝 CENTRO SOLIDARIO"])

# Enlace de tu Google Sites
url_base = "https://sites.google.com/view/ia-libre/inicio"

# 4. LÓGICA
if menu == "🤖 IA LIBRE":
    st.title("🤖 IA Libre: Asistente Universal")
    st.write("Consulta precios, leyes, medicina y más.")
    query = st.text_input("¿En qué puedo apoyarte hoy?")
    if query:
        st.info("Buscando en Google, Yahoo y bases de datos profesionales...")

elif menu == "📰 PRENSAENLOSLAGOS":
    st.title("📰 Prensaenloslagos")
    st.write("Noticias nacionales y de la Región de Los Lagos.")
    st.link_button("VER NOTICIAS AQUÍ", url_base)

elif menu == "📍 DATOSFRESIA":
    st.title("📍 DatosFresia")
    st.write("El corazón local: Farmacias, Clima y Municipalidad.")
    st.link_button("VER DATOS DE FRESIA", url_base)

elif menu == "🤝 CENTRO SOLIDARIO":
    st.title("🤝 Centro Solidario en Acción")
    st.write("Casos sociales, bingos y ayuda comunitaria.")
    st.link_button("VER ACTIVIDAD SOLIDARIA", url_base)
    
