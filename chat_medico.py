from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# Definimos qué datos esperamos recibir
class PacienteDatos(BaseModel):
    edad: float
    presion: float
    frecuencia: float
    saturacion: float

@router.post("/evaluar-riesgo")
async def evaluar_riesgo(datos: PacienteDatos):
    # Aquí va la lógica de negocio
    riesgo = "Bajo"
    analisis = "Tus niveles parecen estables según los parámetros generales."
    
    # Ejemplo de lógica simple
    if datos.presion > 140:
        riesgo = "Alto"
        analisis = "Presión elevada detectada. Se recomienda reposo y consulta médica."
    
    return {
        "analisis": analisis,
        "riesgo": riesgo
    }
