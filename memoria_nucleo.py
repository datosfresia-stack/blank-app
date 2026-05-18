# 🧠 IALIBRE NÚCLEO — UNIDAD CENTRAL DE MEMORIA VOLÁTIL V4.2
# Diseñado para gestionar flujos técnicos continuos de alta densidad (jornadas de más de 12 horas)

# Almacén central de memoria en caliente (RAM del contenedor)
MEMORIA_SECUENCIAL = []

def guardar_en_memoria(canal: str, mensaje: str, respuesta: str) -> bool:
    """
    Registra el intercambio síncrono en la memoria activa del proceso.
    Adapta las entradas al formato nativo de roles de la API de Gemini.
    """
    global MEMORIA_SECUENCIAL
    
    # 1. Inyectamos la transmisión de Miguel mapeando el canal activo
    MEMORIA_SECUENCIAL.append({
        "role": "user", 
        "parts": [f"[{canal.upper()}] Consulta de Miguel: {mensaje}"]
    })
    
    # 2. Inyectamos la inferencia de respuesta generada por el Núcleo
    MEMORIA_SECUENCIAL.append({
        "role": "model", 
        "parts": [respuesta]
    })
    
    # 3. FILTRO DE RESILIENCIA (Anti-Saturación de Buffer):
    # Si la sesión supera los 80 intercambios técnicos masivos, recortamos los más antiguos.
    # Esto previene errores 'Out of Memory' en Railway provocados por el envío de códigos fuentes gigantescos.
    if len(MEMORIA_SECUENCIAL) > 80:
        MEMORIA_SECUENCIAL = MEMORIA_SECUENCIAL[-80:]
        
    return True

def obtener_historial_nativo() -> list:
    """
    Devuelve el buffer completo de la conversación estructurado para inyectarse
    directamente en el constructor 'model.start_chat(history=...)' de Gemini.
    """
    global MEMORIA_SECUENCIAL
    return MEMORIA_SECUENCIAL

def obtener_ultimo_registro_diagnostico() -> str:
    """
    Analizador de estado físico de la memoria. Devuelve un string simplificado
    para telemetría e inspección rápida en la consola web.
    """
    global MEMORIA_SECUENCIAL
    
    if len(MEMORIA_SECUENCIAL) >= 2:
        # El último es el modelo (salida), el penúltimo es el usuario (entrada)
        ultimo_input = MEMORIA_SECUENCIAL[-2]["parts"][0]
        ultimo_output = MEMORIA_SECUENCIAL[-1]["parts"][0]
        
        # Recortamos visualmente para el log de diagnóstico si es un código larguísimo
        resumen_in = ultimo_input[:80] + "..." if len(ultimo_input) > 80 else ultimo_input
        resumen_out = ultimo_output[:80] + "..." if len(ultimo_output) > 80 else ultimo_output
        
        return f"📌 Telemetría Activa (Nodos en memoria: {len(MEMORIA_SECUENCIAL)}) -> Entrada: {resumen_in} | Respuesta: {resumen_out}"
        
    return "📭 Matriz de memoria volátil vacía. El puente secuencial está listo para la primera transmisión."

def resetear_memoria_activa() -> bool:
    """
    Limpia el buffer de la sesión actual en caso de requerir un reinicio completo
    de la matriz de atención cognitiva sin apagar el contenedor de Railway.
    """
    global MEMORIA_SECUENCIAL
    MEMORIA_SECUENCIAL.clear()
    return True