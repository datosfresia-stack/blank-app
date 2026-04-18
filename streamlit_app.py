import streamlit as st

# --- Configuración de la página ---
st.set_page_config(
    page_title="IA Libre - Plantilla",
    page_icon="🤖",
    layout="wide", # Usamos 'wide' para que ocupe todo el ancho
    initial_sidebar_state="collapsed", # Ocultamos la barra lateral por ahora si no es necesaria
)

# --- Título principal ---
st.title("IA LIBRE")

# --- Contenido principal en una fila ---
# Usamos st.columns para crear columnas y colocar el texto en ellas.
# Ajustamos el número de columnas según la cantidad de textos que queremos alinear.
col1, col2, col3 = st.columns(3)

with col1:
    st.write("PRENSA EN LOS LAGOS")

with col2:
    st.write("CENTRO SOLIDARIO EN ACCION")

with col3:
    st.write("DATOS FRESIA")

# --- Espacio adicional (opcional) ---
st.write("") # Añade un poco de espacio si lo necesitas
st.write("")

# --- Pie de página (opcional) ---
st.markdown("---")
st.markdown("Plantilla base - Proyecto IA Libre")