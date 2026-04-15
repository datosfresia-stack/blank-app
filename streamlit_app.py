import streamlit as st
import requests
import random

# Configuración básica
st.set_page_config(page_title="LIBRE", page_icon="🌿")

def obtener_clima():
    try:
        # Pedimos el clima en sistema métrico y español
        r = requests.get("https://wttr.in/Fresia,Chile?format=%C+%t&m&lang=es", timeout=5)
        if r.status_code == 200:
            texto = r.text.strip()
            # LIMPIEZA: Quitamos el símbolo + y arreglamos el error del Â
            texto = texto.replace("+", "")
            texto = texto.replace("Â", "")
            # Si el símbolo de grado sigue fallando, lo forzamos a que se vea bien
            if "°C" not in texto and "C" in texto:
                texto = texto.replace("C", "°C")
            return texto
    except:
        return "Clima no disponible"
    return "Nublado 10°C"

clima_limpio = obtener_clima()

# Interfaz limpia
st.title("🌿 LIBRE - Fresia")
st.write(f"**Estado actual:** {clima_limpio}")

with st.sidebar:
    st.header("📊 Salud")
    st.metric("Presión", "117/76")
    st.divider()
    st.header("📸 Pesa")
    foto = st.file_uploader("Subir foto", type=["jpg", "png", "jpeg"])
    if foto:
        st.image(foto)
        peso = st.number_input("Kilos:", min_value=0.0)
        if peso > 0:
            st.session_state['peso'] = peso
            st.success(f"Guardado: {peso}kg")

# Chat
if "msg" not in st.session_state:
    st.session_state.msg = [{"r": "assistant", "c": f"Hola Miguel. En Fresia tenemos {clima_limpio}. ¿Qué registramos hoy?"}]

for m in st.session_state.msg:
    with st.chat_message(m["r"]):
        st.write(m["c"])

if p := st.chat_input("Escribe aquí..."):
    st.session_state.msg.append({"r": "user", "c": p})
    with st.chat_message("user"): st.write(p)
    
    with st.chat_message("assistant"):
        # Lógica de respuesta inteligente
        p_low = p.lower()
        if "mejorar" in p_low and 'peso' in st.session_state:
            txt = f"Con {st.session_state['peso']} kg, Miguel, mi consejo es aprovechar que está {clima_limpio.split()[0].lower()} para caminar un poco."
        elif "clima" in p_low:
            txt = f"El sensor marca {clima_limpio} en Fresia ahora mismo."
        else:
            txt = "Te escucho, Miguel. Estoy aquí para cuidar tu salud."
            
        st.write(txt)
        st.session_state.msg.append({"r": "assistant", "c": txt})
        
