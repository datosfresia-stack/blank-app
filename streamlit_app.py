# Este modelo es más nuevo y suele tener mejor disponibilidad
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-Nemo-Instruct-2407"
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("La IA está despertando..."):
            respuesta = consultar_ia(prompt)
            st.markdown(respuesta)

st.divider()
st.caption("FRESIA - Red de Inteligencia Alternativa")
