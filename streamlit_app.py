import streamlit as st

# 1. CONFIGURACIÓN DE LA PÁGINA (Identidad del Proyecto)
st.set_page_config(
    page_title="IA Libre - Portal Multiplataforma",
    page_icon="🤖",
    layout="wide"
)

# Estilos personalizados para mejorar la apariencia de los títulos
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. MENÚ LATERAL (Los Brazos del Proyecto)
st.sidebar.title("Navegación")
menu = st.sidebar.radio(
    "Seleccione una sección:",
    ["🤖 IA LIBRE (CABEZA)", "📰 PRENSAENLOSLAGOS", "📍 DATOSFRESIA", "🤝 CENTRO SOLIDARIO"]
)

st.sidebar.divider()
st.sidebar.info("Proyecto Multiplataforma - Fresia, Los Lagos")

# 3. LÓGICA DE CADA SECCIÓN

# --- SECCIÓN: IA LIBRE ---
if menu == "🤖 IA LIBRE (CABEZA)":
    st.title("🤖 IA Libre: Asistente Universal")
    st.subheader("Motor de consultas, traducción y asesoría profesional")
    
    # Simulación de conexión a motores de búsqueda (Google, Yahoo, Hotmail/OneDrive)
    query = st.text_input("¿En qué puedo asesorarte hoy? (Precios, Leyes, Medicina, Inversiones...)", 
                          placeholder="Ej: ¿Cómo está el precio del dólar hoy?")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Traducir Voz/Texto"):
            st.write("Función de traducción activada...")
    with col2:
        if st.button("Asesoría Profesional"):
            st.write("Conectando con base de datos técnica (Leyes, Química, Medicina)...")
    with col3:
        if st.button("Consultar Inversiones"):
            st.write("Analizando mercados globales...")

    if query:
        st.chat_message("assistant").write(f"Buscando información sobre '{query}' en motores Google, Yahoo y bases de datos Linux...")

# --- SECCIÓN: PRENSAENLOSLAGOS ---
elif menu == "📰 PRENSAENLOSLAGOS":
    st.title("📰 Prensaenloslagos")
    st.write("Noticias de Chile y la Región de Los Lagos")
    
    tab1, tab2 = st.tabs(["🇨🇱 Nacional", "🏞️ Regional (Los Lagos)"])
    
    with tab1:
        st.header("Hitos Nacionales")
        st.info("Votaciones Domingo: Seguimiento minuto a minuto.")
        # Aquí se integraría el feed de WordPress o Google Sites
        st.markdown("---")
        st.write("📌 *Espacio para noticias de economía y política.*")
    
    with tab2:
        st.header("Actualidad Regional")
        st.write("Noticias locales de la Región de Los Lagos.")
    
    st.sidebar.button("Compartir en Redes Sociales 📱")

# --- SECCIÓN: DATOSFRESIA ---
elif menu == "📍 DATOSFRESIA":
    st.title("📍 DatosFresia")
    st.subheader("El corazón de la comuna")
    
    col_info, col_clima = st.columns(2)
    with col_info:
        st.success("🏥 Farmacias de Turno: Revisar horario de hoy.")
        st.write("🏛️ Noticias Municipales")
    with col_clima:
        st.metric(label="Clima en Fresia", value="18°C", delta="Soleado")
    
    st.markdown("---")
    st.write("📷 **Galería Comunal**")
    # Espacio para cargar imágenes desde la plataforma amigable

# --- SECCIÓN: CENTRO SOLIDARIO ---
elif menu == "🤝 CENTRO SOLIDARIO":
    st.title("🤝 El Centro Solidario en Acción")
    st.write("Visibilizando la ayuda comunitaria y casos sociales.")
    
    # Espacio para multimedia
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Link de ejemplo para video de ayuda
    
    st.subheader("Próximos Eventos Benéficos")
    st.warning("🎟️ Rifa Solidaria: Sábado 20 de Mayo. ¡Participa!")
    
    # Conexión con OneDrive para ver archivos de casos sociales
    st.write("📂 *Documentación y registros cargados desde OneDrive.*")

