import streamlit as st
import os
from dotenv import load_dotenv
from serpapi import GoogleSearch

# --- Configuración Inicial ---
load_dotenv() # Carga las variables de entorno desde el archivo .env
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# --- Datos de la IA y el Creador ---
nombre_ia = "IA Libre"
padre_ia = "Datos Fresia"
raices_ia = "Chile"

# --- Respuestas Predefinidas ---
respuestas_predefinidas = {
    "hola": "¡Hola! Soy IA Libre. ¿En qué puedo ayudarte hoy?",
    "quien eres": f"Soy {nombre_ia}, un asistente de inteligencia artificial creado por {padre_ia} con raíces en {raices_ia}. Mi propósito es ayudarte con información y consultas.",
    "cual es tu nombre": f"Mi nombre es {nombre_ia}.",
    "quien te creo": f"Fui creado por {padre_ia}.",
    "donde estan tus raices": f"Mis raíces están en {raices_ia}.",
    "gracias": "¡De nada! Estoy aquí para ayudarte.",
    "adios": "¡Hasta luego! Que tengas un buen día.",
    "ayuda": "Puedes preguntarme sobre diversos temas. Si no tengo la respuesta, intentaré buscarla en internet. También puedes explorar las otras secciones de la aplicación.",
    "tu proposito": "Mi propósito es ser un asistente útil, proporcionando información y apoyo en tus consultas.",
    "inteligencia artificial": "La inteligencia artificial (IA) es un campo de la informática que se centra en la creación de sistemas capaces de realizar tareas que normalmente requieren inteligencia humana, como el aprendizaje, la resolución de problemas y la toma de decisiones.",
    "wikipedia": "Wikipedia es una enciclopedia en línea colaborativa, multilingüe, libre y de acceso abierto, gestionada por la Fundación Wikimedia. Es una de las fuentes de información más consultadas en internet.",
    "youtube": "YouTube es una plataforma de videos en línea donde los usuarios pueden subir, ver y compartir videos. Es propiedad de Google y es una de las redes sociales más grandes del mundo."
}

# --- URL de tu canal de YouTube ---
# ¡¡¡ REEMPLAZADO CON LA URL QUE PROPORCIONASTE !!!
youtube_channel_url = "https://www.youtube.com/@DFresiaTV"
# Si quieres usar una miniatura de un video, descomenta y ajusta la siguiente línea:
# youtube_video_thumbnail_url = "https://img.youtube.com/vi/ID_DEL_VIDEO/0.jpg" # Reemplaza ID_DEL_VIDEO

# --- Configuración de la página de Streamlit ---
st.set_page_config(page_title="IA Libre", page_icon="🤖", layout="wide")

# --- Barra Lateral ---
with st.sidebar:
    st.header("IA Libre")
    # Opcional: Añade un logo aquí si tienes uno. Reemplaza la URL.
    # Si no tienes logo, puedes comentar o eliminar la siguiente línea.
    # st.image("https://i.imgur.com/your_logo_image.png", width=100)

    st.markdown("---")
    st.write(f"**Asistente:** {nombre_ia}")
    st.write(f"**Raíces:** {raices_ia}")
    st.write(f"**Creador:** {padre_ia}")

    st.markdown("---")
    st.subheader("Visita mi Canal")

    # --- Enlace al canal de YouTube ---
    # Opción 1: Icono de YouTube (abre en nueva pestaña) - ESTA ES LA QUE ESTÁ ACTIVA
    st.markdown(f"[![YouTube](https://img.icons8.com/color/48/000000/youtube-play.png)]( {youtube_channel_url} )", unsafe_allow_html=True)

    # Opción 2: Enlace con miniatura de video (si quieres algo más visual) - ESTÁ COMENTADA
    # Descomenta estas dos líneas si quieres usar una miniatura y ajusta la URL de la miniatura
    # youtube_video_thumbnail_url = "https://img.youtube.com/vi/ID_DEL_VIDEO/0.jpg" # <-- Pega aquí la URL de la miniatura de un video tuyo
    # st.markdown(f"[![Mi Canal de YouTube]({youtube_video_thumbnail_url})]({youtube_channel_url}?sub_confirmation=1)", unsafe_allow_html=True)

    # --- Enlace de texto adicional (opcional) ---
    st.markdown(f"¡Encuentra contenido sobre IA y tecnología! [Suscríbete en YouTube]({youtube_channel_url}?sub_confirmation=1)", unsafe_allow_html=True)

    # --- Navegación ---
    st.markdown("---")
    st.header("Navegación")
    opcion_seleccionada = st.radio(
        "Elige una sección:",
        ("Inicio", "Chat IA", "Sobre IA Libre")
    )

# --- Contenido Principal ---
if opcion_seleccionada == "Inicio":
    st.header("Bienvenido a IA LIBRE")
    st.write(f"Soy **{nombre_ia}**, tu asistente de inteligencia artificial desarrollado en **{raices_ia}**. Mi creador es **{padre_ia}**. Estoy aquí para ayudarte con información, consultas y proyectos en diversas áreas.")

    st.markdown("---")
    st.subheader("Explora nuestras secciones:")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 📰 Prensa en Los Lagos")
        st.markdown("Noticias y actualidad de la región.")
        # Reemplaza con tu URL real si es diferente
        st.markdown("[Visitar Prensa en Los Lagos](https://sites.google.com/view/ia-libre/inicio) <span style='font-size:0.8em;'>(abre en nueva pestaña)</span>", unsafe_allow_html=True)

    with col2:
        st.markdown("#### 🤝 Centro Solidario en Acción")
        st.markdown("Información sobre iniciativas sociales.")
        st.write("*(Sección en desarrollo)*")

    with col3:
        st.markdown("#### 📍 Datos Fresia")
        st.markdown("Información relevante sobre la comuna.")
        st.write("*(Sección en desarrollo)*")

elif opcion_seleccionada == "Chat IA":
    st.header("Chat de Asistencia IA")
    st.write(f"¡Hola! Soy {nombre_ia}, tu asistente de inteligencia artificial. ¿En qué puedo ayudarte hoy?")
    st.write("Puedes preguntarme sobre diversos temas, desde información general hasta apoyo en proyectos profesionales.")

    # Inicializar el historial de chat en session_state si no existe
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Mostrar el historial de chat
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.write(f"**Tú:** {message['content']}")
        else:
            st.write(f"**{nombre_ia}:** {message['content']}")

    # Usamos un formulario para manejar la entrada y el envío
    with st.form(key='chat_form'):
        user_input = st.text_area("Escribe tu consulta aquí:", height=150, key='user_input_textarea')
        submit_button = st.form_submit_button(label='Enviar Consulta')

    if submit_button and user_input:
        # Añadir el mensaje del usuario al historial
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        consulta_lower = user_input.lower()
        respuesta_ia = "Lo siento, aún estoy aprendiendo y no tengo la respuesta a esa pregunta. ¿Puedo ayudarte con otra cosa?" # Respuesta por defecto
        encontrado_predefinido = False

        # 1. Intentar buscar en respuestas predefinidas
        for palabra_clave, resp in respuestas_predefinidas.items():
            if palabra_clave in consulta_lower:
                respuesta_ia = resp
                encontrado_predefinido = True
                break

         # 2. Si no se encontró en predefinidas Y hay API Key, intentar buscar en internet
        if not encontrado_predefinido and SERPAPI_API_KEY:
            try:
                params = {
                    "q": user_input,
                    "api_key": SERPAPI_API_KEY,
                    "hl": "es", # Idioma español
                    "gl": "cl"  # Geografía Chile (opcional)
                }
                search = GoogleSearch(params)
                results = search.get_dict()

                if "organic_results" in results and results["organic_results"]:
                    primer_resultado = results["organic_results"][0]
                    titulo = primer_resultado.get("title", "Resultado de Búsqueda")
                    snippet = primer_resultado.get("snippet", "No se encontró descripción.")
                    url = primer_resultado.get("link", "#")
                    respuesta_ia = f"He encontrado información sobre tu consulta:\n\n**{titulo}**\n{snippet}\n\n[Más información]({url})"
                elif "answer" in results: # Respuesta directa de Google
                     respuesta_ia = results["answer"]
                elif "knowledge_graph" in results: # Knowledge Graph de Google
                     respuesta_ia = results["knowledge_graph"].get("description", "No se encontró descripción detallada.")
                else:
                    respuesta_ia = "Realicé una búsqueda, pero no pude extraer una respuesta clara. ¿Podrías reformular tu pregunta?"

            except Exception as e:
                respuesta_ia = f"Ocurrió un error al intentar buscar en internet: {e}. Por favor, intenta de nuevo más tarde."

        # 3. Si no se encontró en predefinidas Y NO hay API Key
        elif not SERPAPI_API_KEY and not encontrado_predefinido:
            respuesta_ia = "La funcionalidad de búsqueda en internet está configurada, pero necesito una clave API para funcionar. Por favor, consulta la documentación para configurarla."

        # Añadir la respuesta de la IA al historial
        st.session_state.chat_history.append({"role": "assistant", "content": respuesta_ia})

        # Forzar la actualización para que el nuevo mensaje aparezca inmediatamente
        st.rerun()

# --- Fin del bloque Chat IA ---

# ... (resto del código, como el 'elif opcion_seleccionada == "Sobre IA Libre":') ...