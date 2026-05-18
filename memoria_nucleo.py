# 🧠 MEMORIA INTERNA DEL NÚCLEO
memoria_guardada = []

def guardar_en_memoria(canal: str, mensaje: str, respuesta: str):
    """Guarda la conversación completa"""
    registro = {
        "canal": canal,
        "entrada": mensaje,
        "salida": respuesta
    }
    memoria_guardada.append(registro)
    return True

def obtener_memoria():
    """Devuelve el último mensaje o avisa si está vacía"""
    if len(memoria_guardada) > 0:
        ultimo = memoria_guardada[-1]
        return f"📌 Último registro -> Entrada: {ultimo['entrada']} | Salida: {ultimo['salida']}"
    return "📭 Memoria vacía. Empieza a hablarme."