import streamlit as st
import requests
import feedparser

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Prensaenloslagos", page_icon="📰", layout="wide")

# 2. FUNCIONES DE DATOS (EL MOTOR)
def obtener_clima():
    try:
        r = requests.get("https://wttr.in/Fresia,Chile?format=%C+%t&m&lang=es", timeout=5)
        return r.text.replace("+", "").strip() if r.status_code == 200 else "Despejado 14°C"
    except: return "Despejado 14°C"

def obtener_noticias():
    try:
        f = feedparser.parse("https://www.biobiochile.cl/lista/tag/chile/feed")
        return [{"t": e.title, "l": e.link} for e in f.entries[:10]]
    except: return []

# Carga de datos
clima = obtener_clima()
noticias = obtener_noticias()

# 3. DISEÑO DE LA "CASA"
st.markdown("<h1 style='text-align: center; color: #1877F2;'>📰 Prensaenloslagos</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'><b>📍 Fresia, Los Lagos | {clima}</b></p>", unsafe_allow_html=True)

# MARQUESINA (SCROLL VERDE)
if noticias:
    titulares = "  •  ".join([n['t'] for n in noticias])
    st.markdown(f"""
        <div style="background: black; color: #3dfc03; padding: 10px; font-family: monospace;">
            <marquee scrollamount="8">{titulares}</marquee>
        </div>
    """, unsafe_allow_html=True)

st.write("---")

# 4. PESTAÑAS
tab1, tab2, tab3, tab4 = st.tabs(["🗞️ Noticias", "🔵 Nuestro Facebook", "🤝 Solidario", "🤖 IA Libre"])

with tab1:
    st.subheader("Titulares Nacionales")
    for n in noticias:
        st.markdown(f"🔹 [{n['t']}]({n['l']})")

with tab2:
    st.subheader("Comunidad en Redes Sociales")
    st.write("¡Ya somos miles en Facebook! Sigue nuestra cobertura en vivo.")
    # Botón grande azul tipo Facebook
    st.markdown("""
        <a href="https://www.facebook.com/prensaenloslagos" target="_blank">
            <button style="background-color: #1877F2; color: white; padding: 15px; border: none; border-radius: 10px; cursor: pointer; width: 100%; font-size: 18px;">
                Ir al Facebook de Prensaenloslagos
            </button>
        </a>
    """, unsafe_allow_html=True)
    st.info("Haz clic arriba para ver las últimas transmisiones y denuncias ciudadanas.")

with tab3:
    st.subheader("Centro Solidario")
    st.success("Campaña: Ayuda para familias de Fresia.")
    if st.button("Quiero ayudar"): st.balloons()

with tab4:
    st.subheader("Consulta a Libre (IA)")
    if "chat" not in st.session_state: st.session_state.chat = []
    
    for m in st.session_state.chat:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    
    if p := st.chat_input("Dime algo"):
        st.session_state.chat.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        
        # Respuesta automática
        resp = f"Hola Miguel, soy Libre. Te cuento que en Fresia hay {clima}."
        st.session_state.chat.append({"role": "assistant", "content": resp})
        with st.chat_message("assistant"): st.markdown(resp)

# BARRA LATERAL
with st.sidebar:
    st.image("https://img.icons8.com/color/96/facebook-new.png")
    st.title("Panel de Control")
    st.write("Miguel Alarcón")
    st.divider()
    st.write("Estado de salud: Estable")
    st.metric("Presión", "117/76")
