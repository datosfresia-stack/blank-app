memoria_almacenada = []

def guardar_en_memoria(categoria: str, entrada: str, respuesta: str):
    registro = {"categoria": categoria, "entrada": entrada, "respuesta": respuesta}
    memoria_almacenada.append(registro)
    if len(memoria_almacenada) > 50:
        memoria_almacenada.pop(0)

def obtener_memoria(ultimas: int = 5):
    if not memoria_almacenada:
        return "Sin registros en memoria."
    registros = memoria_almacenada[-ultimas:]
    return " | ".join([f"[{r['categoria']}]: {r['entrada']}" for r in registros])