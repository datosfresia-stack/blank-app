import streamlit as st

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Portal IA Libre",
    page_icon="🤖",
    layout="wide"
)

# 2. MENÚ LATERAL (Los Brazos)
st.sidebar.title("Navegación")
menu = st.sidebar.radio(
    "Seleccione una sección:",
    ["🤖 IA LIBRE (CABEZA)", "📰 PRENSAENLOSLAGOS", "📍 DATOSFRESIA", "🤝 CENTRO SOLIDARIO"]
)

st.sidebar.divider()
st.sidebar.info("Proyecto Multiplataforma - Fresia")

# URL de tu Google Sites
google_site_url = "https://sites.google.com/view/ia-libre/inicio"

# 3. LÓGICA DE SECCIONES

if menu == "🤖 IA LIBRE (CABEZA)":
    st.title("🤖 IA Libre: Asistente Universal")
    query = st.text_input("¿En qué puedo asesorarte hoy? (Precios, Leyes, Medicina, Inversiones...)")
    if query:
        st.chat_message("assistant").write(f"Procesando consulta: '{query}'...")

elif menu == "📰 PRENSAENLOSLAGOS":
    st.title("📰 Prensaenloslagos")
    st.write("Noticias de Chile y la Región de Los Lagos")
    # Mostramos el Google Sites aquí adentro
    st.components.v1.iframe(google_site_url, height=800, scrolling=True)

elif menu == "📍 DATOSFRESIA":
    st.title("📍 DatosFresia")
    # También podemos mostrar el Google Sites o una página específica de él
    st.components.v1.iframe(google_site_url, height=800, scrolling=True)

elif menu == "🤝 CENTRO SOLIDARIO":
    st.title("🤝 El Centro Solidario en Acción")
    st.write("Galería de casos sociales y ayuda comunitaria")
    st.components.v1.iframe(google_site_url, height=800, scrolling=True)

# Botón para compartir en la barra lateral
if st.sidebar.button("Compartir este Portal"):
    st.sidebar.write("¡Copia el link de la barra de direcciones para compartir en Facebook o WhatsApp!")
    
