import streamlit as st
import sys
# Eliminamos las importaciones de subprocess ya que no las usaremos para instalar paquetes

# --- Configuración de la página ---
st.set_page_config(
    page_title="Proyecto IA Libre - Dola",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Inicialización del estado de la sesión ---
# Esto asegura que la información personal se mantenga durante la sesión del usuario.
if 'personal_info' not in st.session_state:
    st.session_state.personal_info = {
        "nombre": "",
        "email": "",
        "telefono": "",
        "direccion": ""
    }

# --- Lógica para cargar las páginas ---
# Importa las funciones de las páginas para poder llamarlas.
# Asegúrate de que estas rutas de importación coincidan con tu estructura de carpetas.
try:
    # Importaciones de las páginas
    from pages import centro_solidario, datos_fresia, prensa_lagos
    # Importaciones de las utilidades
    from utils import database_utils, multimedia_utils, personal_info as personal_info_utils, search_utils, translation_utils

    # Si tienes más páginas o utilidades, impórtalas aquí.
    # Ejemplo: from pages import otra_pagina
    # Ejemplo: from utils import otra_utilidad

except ImportError as e:
    st.error(f"Error al importar módulos: {e}. Asegúrate de que las carpetas 'pages' y 'utils' y sus archivos '__init__.py' estén correctamente configurados y que todas las dependencias estén en requirements.txt.")
    st.stop() # Detiene la ejecución si las importaciones fallan

# --- Barra lateral de navegación ---
st.sidebar.title("Navegación")

# Usamos un diccionario para mapear las opciones del menú a las funciones correspondientes.
# Asegúrate de que las claves (nombres de las opciones) coincidan con lo que esperas
# y que las funciones existan en los módulos importados.
menu_options = {
    "Inicio": lambda: st.write("Bienvenido a tu aplicación multifuncional."),
    "Centro Solidario": centro_solidario.show,
    "Datos Fresia": datos_fresia.show,
    "Prensa Lagos": prensa_lagos.show,
    "Asistente IA": lambda: st.write("Interactúa con el Asistente IA aquí."),
    # Añade aquí las demás opciones de menú y sus funciones
    # "Otra Página": otra_pagina.show,
}

selected_option = st.sidebar.radio("Ir a", list(menu_options.keys()))

# --- Mostrar contenido según la opción seleccionada ---
try:
    # Llama a la función correspondiente a la opción seleccionada.
    # Si la opción es "Asistente IA", mostramos un contenido específico aquí.
    if selected_option == "Asistente IA":
        st.title("🤖 Asistente IA")
        st.write("¡Hola! ¿En qué puedo ayudarte hoy? Puedes hacerme preguntas, pedirme que genere texto, o cualquier otra cosa que necesites.")

        # Aquí puedes añadir la lógica para interactuar con modelos de IA si lo deseas.
        # Por ejemplo, podrías tener un campo de texto y un botón para enviar consultas.
        user_input = st.text_area("Tu consulta:", height=150)
        if st.button("Enviar"):
            if user_input:
                # Aquí iría la lógica para procesar la consulta del usuario
                # con un modelo de IA (ej. usando transformers).
                # Por ahora, solo mostraremos un mensaje.
                st.info(f"Procesando tu consulta: '{user_input}'...")
                # Ejemplo de cómo podrías llamar a una función de transformers si la tuvieras:
                # from transformers import pipeline
                # generator = pipeline('text-generation', model='gpt2')
                # response = generator(user_input, max_length=50, num_return_sequences=1)
                # st.write("Respuesta IA:", response[0]['generated_text'])
            else:
                st.warning("Por favor, introduce una consulta.")

    else:
        # Para las demás opciones, llama a la función asociada del menú.
        menu_options[selected_option]()

except Exception as e:
    st.error(f"Se ha producido un error al cargar la sección '{selected_option}': {e}")
    # Opcionalmente, puedes registrar el error completo para depuración:
    # import traceback
    # st.error(traceback.format_exc())

# --- Pie de página ---
st.markdown("---")
st.markdown("© 2024 Proyecto IA Libre - Dola. Todos los derechos reservados.")