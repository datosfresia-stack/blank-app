from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class PacienteDatos(BaseModel):
    rol: str
    diagnostico: str
    peso: float
    presion: float
    saturacion: float

@router.post("/evaluar-riesgo")
async def evaluar_riesgo(datos: PacienteDatos):
    # Convertimos a minúsculas para que detecte "Cáncer", "CANCER", "cáncer", etc.
    diag = datos.diagnostico.lower()
    
    # Lógica mejorada
    if "cancer" in diag:
        mensaje = (f"Entiendo tu situación, {datos.rol}. "
                   "He detectado tu diagnóstico. En esta etapa, el apoyo emocional y la "
                   "información correcta son vitales. Te recomiendo contactar a la Fundación "
                   "de Valdivia o centros oncológicos de tu región. "
                   "¿Necesitas apoyo en salud mental o orientación sobre hospedaje?")
        return {"analisis": mensaje, "riesgo": "Prioridad de Orientación"}
    
    # Si no es cáncer, seguimos con lo genérico
    return {"analisis": "Hemos recibido tus datos. Un especialista de la red podría orientarte mejor.", "riesgo": "Consulta General"}
