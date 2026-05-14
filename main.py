from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db, init_db, JobDemand 
import uvicorn
import os

app = FastAPI()

# --- BLOQUE VITAL: PERMISOS PARA WORDPRESS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Esto permite que PrensaenLosLagos se conecte
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Esquema de datos para el Chat
class DemandCreate(BaseModel):
    full_name: str
    skills: str
    experience_years: int = 0
    contact_info: str

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def root():
    return {"message": "Servidor IALibre Activo"}

@app.post("/nueva-demanda")
async def crear_demanda(data: DemandCreate, db: AsyncSession = Depends(get_db)):
    try:
        nueva_demanda = JobDemand(
            full_name=data.full_name,
            skills=data.skills,
            experience_years=data.experience_years,
            contact_info=data.contact_info
        )
        db.add(nueva_demanda)
        await db.commit()
        return {"status": "success"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)