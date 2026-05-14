from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db, init_db, JobDemand  # Importamos lo que ya funciona
import uvicorn

app = FastAPI()

# --- CONFIGURACIÓN CORS (VITAL PARA WORDPRESS) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ESQUEMA PARA RECIBIR DATOS ---
class DemandCreate(BaseModel):
    full_name: str
    skills: str
    experience_years: int = 0
    contact_info: str

# Evento de inicio para crear tablas
@app.on_event("startup")
async def startup_event():
    await init_db()

# --- RUTA QUE LLAMA EL CHAT ---
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
        return {"status": "success", "message": "Registro guardado en Railway"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Servidor IALibre Activo"}

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)