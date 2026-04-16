import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="IA Libre Fresia")

# 1. CONEXIÓN (Asegúrate que la clave 1w5A esté en Secrets)
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # CAMBIO CLAVE: Usamos 'gemini-pro' en lugar de '1.5-flash'
        model = genai.GenerativeModel('gemini-pro')
        ia_lista = True
    else:
        ia_lista = False
        st.error("⚠️ No hay llave en Secrets")
except Exception as e:
    ia_lista = False
    st.error(f"Error: {e}")

# 2. INTERFAZ
st.title("🤖 IA Libre")

if ia_lista:
    pregunta = st.text_input("Haz tu consulta:")
    if pregunta:
        try:
            # Respuesta directa
            response = model.generate_content(pregunta)
            st.markdown(response.text)
        except Exception as e:
            # Si falla, pedimos que nos diga la lista de modelos permitidos
            st.error("Error de conexión.")
            st.write("Modelos disponibles en tu cuenta:")
            try:
                modelos = [m.name for m in genai.list_models()]
                st.write(modelos)
            except:
                st.write("No se pudo listar modelos. Revisa la región de tu cuenta.")

st.divider()
st.link_button("🌐 Volver al Portal", "https://sites.google.com/view/ia-libre/inicio")
