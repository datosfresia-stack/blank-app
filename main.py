from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
# Usamos las variables de Railway que validamos anteriormente
DB_USER = "root"
DB_PASSWORD = "-M72.EIiUz_MqTdJ_mH0hw96tqSjaPW6"
DB_HOST = "turntable.proxy.rlwy.net"
DB_PORT = "36536"
DB_NAME = "railway"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- MODELO DE LA TABLA ---
class JobDemand(Base):
    __tablename__ = "demandas_empleo"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255))
    profesion = Column(String(255))
    experiencia = Column(Text)

# Crear las tablas en Railway si no existen
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Conexión Blindada: Tablas sincronizadas en Railway.")
except Exception as e:
    print(f"❌ Error de enlace: {e}")

# --- APP FASTAPI ---
app = FastAPI(title="IALibre - Prensaenloslagos")

# --- CONFIGURACIÓN DE CORS (CRUCIAL PARA EL CHAT) ---
# Esto permite que el navegador acepte peticiones desde su WordPress
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes para pruebas
    allow_credentials=True,
    allow_methods=["*"],  # Permite POST y el pre-vuelo OPTIONS
    allow_headers=["*"],
)

# --- ESQUEMA DE DATOS (PYDANTIC) ---
class DemandaCreate(BaseModel):
    nombre: str
    profesion: str
    experiencia: str

# --- ENDPOINT PARA RECIBIR DATOS DEL CHAT ---
@app.post("/nueva-demanda")
def crear_demanda(demanda: DemandaCreate):
    db = SessionLocal()
    try:
        nueva_entrada = JobDemand(
            nombre=demanda.nombre,
            profesion=demanda.profesion,
            experiencia=demanda.experiencia
        )
        db.add(nueva_entrada)
        db.commit()
        db.refresh(nueva_entrada)
        return {"status": "success", "message": "Registro guardado en Railway", "id": nueva_entrada.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Servidor IALibre Activo"}