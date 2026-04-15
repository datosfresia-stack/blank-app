import streamlit as st
import requests
import random

# Configuración básica (Clipper Style: Directo y funcional)
st.set_page_config(page_title="LIBRE", page_icon="🌿")

def obtener_clima():
    try:
        # Forzamos Celsius (m) y Español (es)
        r = requests.get("https://wttr.in/Fresia,Chile?format=%C+%t&m&lang=es", timeout=5)
        return r.text.replace("+", "").strip()
    except:
        return "Clima no disponible"

clima = obtener_clima()

# Interfaz
st.title("🌿 LIBRE - Fresia")
st.write(f"**Estado actual:** {clima}")

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
    st.session_state.msg = [{"r": "assistant", "c": f"Hola Miguel. En Fresia tenemos {clima}. ¿Qué registramos hoy?"}]

for m in st.session_state.msg:
    with st.chat_message(m["r"]):
        st.write(m["c"])

if p := st.chat_input("Escribe aquí..."):
    st.session_state.msg.append({"r": "user", "c": p})
    with st.chat_message("user"): st.write(p)
    
    with st.chat_message("assistant"):
        txt = "Te escucho, Miguel. Vamos a cuidar esa salud."
        if "mejorar" in p.lower() and 'peso' in st.session_state:
            txt = f"Con {st.session_state['peso']}kg, te sugiero caminar por el jardín hoy."
        st.write(txt)
        st.session_state.msg.append({"r": "assistant", "c": txt})
        
