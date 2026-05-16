import os
import math
import random
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db, JobDemand  # Mantiene sus tablas previas e importaciones

app = FastAPI(title="IALibre API Central — Multi-Servicios")

# --- CONFIGURACIÓN DE SEGURIDAD CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite conexiones de todos sus portales (PrensaenLosLagos e IALibre)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================================
# 💼 SERVICIO 1: AGENCIA DE EMPLEOS (Para PrensaenLosLagos — YA FUNCIONANDO)
# =====================================================================

class DemandCreate(BaseModel):
    full_name: str
    skills: str
    experience_years: int
    contact_info: str

@app.post("/nueva-demanda")
async def crear_demanda(demanda: DemandCreate, db: AsyncSession = Depends(get_db)):
    try:
        nueva_demanda = JobDemand(
            full_name=demanda.full_name,
            skills=demanda.skills,
            experience_years=demanda.experience_years,
            contact_info=demanda.contact_info
        )
        db.add(nueva_demanda)
        await db.commit()
        await db.refresh(nueva_demanda)
        return {"status": "success", "message": "¡Registrado con éxito en IALibre!"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================================
# 🧠 SERVICIO 2: CHAT MÉDICO MATRICIAL (Para la página principal IALibre)
# =====================================================================

class DatosPaciente(BaseModel):
    edad: float
    presion: float
    frecuencia: float
    saturacion: float
    hipertenso: float
    region: float

class NeuronaMedica:
    def __init__(self):
        # Inicialización de los 6 pesos de su lógica de C++
        self.pesos = [random.uniform(-1.0, 1.0) for _ in range(6)]
    
    def activar(self, x):
        try:
            return 1 / (1 + math.exp(-x))
        except OverflowError:
            return 0.0 if x < 0 else 1.0

    def procesar(self, edad, presion, frecuencia, saturacion, hipertenso, region):
        suma = (edad * self.pesos[0] + 
                presion * self.pesos[1] + 
                frecuencia * self.pesos[2] + 
                saturacion * self.pesos[3] + 
                hipertenso * self.pesos[4] + 
                region * self.pesos[5])
        return self.activar(suma)

    def entrenar_matriz_local(self):
        casos = [
            (25, 115, 75, 98, 0, 1, 0.1),  # Joven Normal
            (82, 160, 85, 96, 1, 1, 0.2),  # Anciano Sur Aceptable
            (45, 125, 80, 94, 0, 1, 0.3),  # Límite Leve
            (45, 155, 110, 90, 0, 1, 0.7), # Alto Riesgo
            (60, 175, 130, 84, 1, 0, 0.9)  # Crítico Fuera de Zona
        ]
        velocidad = 0.7
        for _ in range(5000):
            for edad, pres, frec, sat, hip, reg, esperado in casos:
                obtenido = self.procesar(edad, pres, frec, sat, hip, reg)
                error = esperado - obtenido
                delta = error * obtenido * (1 - obtenido)
                
                self.pesos[0] += delta * edad * velocidad
                self.pesos[1] += delta * pres * velocidad
                self.pesos[2] += delta * frec * velocidad
                self.pesos[3] += delta * sat * velocidad
                self.pesos[4] += delta * hip * velocidad
                self.pesos[5] += delta * reg * velocidad

# Se inicializa y entrena la neurona médica de forma independiente en la memoria de la API
neurona_web = NeuronaMedica()
neurona_web.entrenar_matriz_local()

@app.post("/evaluar-riesgo")
async def evaluar_riesgo(paciente: DatosPaciente):
    riesgo = neurona_web.procesar(
        paciente.edad, 
        paciente.presion, 
        paciente.frecuencia, 
        paciente.saturacion, 
        paciente.hipertenso, 
        paciente.region
    )
    
    if riesgo > 0.8:
        estado = "🔴 ESTADO: GRAVE"
        analisis = "🚑 RECOMENDACIÓN: ATENCIÓN INMEDIATA.<br>📌 RAZÓN: Los valores vitales se encuentran críticamente fuera de rango."
    elif riesgo > 0.5:
        estado = "🟠 ESTADO: ALTO"
        analisis = "⚠️ RECOMENDACIÓN: MONITOREO CONSTANTE.<br>📌 RAZÓN: Se detectan alteraciones significativas en las constantes analizadas."
    elif riesgo > 0.3:
        estado = "🟡 ESTADO: LEVE"
        analisis = "👀 RECOMENDACIÓN: OBSERVACIÓN.<br>📌 RAZÓN: Valores ligeramente diferentes a lo normal (comportamiento aceptable en rangos del Sur)."
    else:
        estado = "🟢 ESTADO: NORMAL"
        analisis = "✅ RECOMENDACIÓN: ESTABLE.<br>📌 RAZÓN: Todos los parámetros médicos se encuentran dentro de lo esperado."

    return {
        "riesgo": f"{riesgo:.4f}",
        "estado": estado,
        "analisis": f"<strong>{estado}</strong><br>{analisis}"
    }

# --- RAÍZ DE VERIFICACIÓN ---
@app.get("/")
def inicio():
    return {"status": "Servidores unificados. Núcleo IALibre en línea y respondiendo."}