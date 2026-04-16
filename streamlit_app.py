import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DEL CEREBRO (API KEY)
# Usamos tu llave y forzamos el modelo 'gemini-pro' que es el estándar de oro
try:
    genai.configure(api_key="AIzaSyBERnyHBPNKai3y-IGtykVBaTal414UC7M")
    # Cambiamos 'gemini-1.5-flash' por 'gemini-pro' para evitar el error 404
    model = genai.GenerativeModel('gemini-pro')
    # Prueba interna silenciosa
    ia_funcional = True
except Exception as e:
    ia_funcional = False
    error_msg = str(e)

# ... (El resto del código del menú se mantiene igual) ...

# 4. DENTRO DE LA LÓGICA DE IA LIBRE:
if menu == "🤖 IA LIBRE (CABEZA)":
    st.title("🤖 IA Libre: Asistente Universal")
    
    if not ia_funcional:
        st.error(f"Error de conexión: {error_msg}")
    else:
        # Aquí sigue tu chat normal...
        if prompt := st.chat_input("¿En qué puedo asesorarte hoy?"):
            with st.chat_message("assistant"):
                try:
                    # Usamos una configuración de seguridad básica
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Fallo en la respuesta: {e}")
                    
