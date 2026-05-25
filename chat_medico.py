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
    diagnostico_lower = datos.diagnostico.lower()
    
    # Lógica de Orientación Oncológica (Universal)
    if "cancer" in diagnostico_lower:
        mensaje_base = f"Entiendo profundamente la situación, {datos.rol}. "
        if datos.rol == "Paciente":
            mensaje_base += "Tu bienestar emocional y físico es la prioridad. "
        else:
            mensaje_base += "Tu rol de acompañamiento es fundamental y muy valioso. "
        
        return {
            "analisis": mensaje_base + "Te sugiero revisar el feed de apoyo a un costado y contactar con centros especializados. ¿Necesitas información sobre redes de apoyo o salud mental?",
            "riesgo": "Prioridad de Orientación",
            "enlace": "https://fundacionvaldivia.cl" # Ejemplo
        }

    # Lógica estándar de signos vitales
    return {"analisis": "Hemos recibido tus datos. Un especialista de la red podría orientarte mejor.", "riesgo": "Consulta General"}
