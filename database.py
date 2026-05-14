import os
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno locales (si existen)
load_dotenv()

# --- LÓGICA DE CONEXIÓN DINÁMICA ---
# 1. Intentamos obtener la URL maestra de Railway
RAW_URL = os.getenv("MYSQL_URL") or os.getenv("MARIADB_URL")

if RAW_URL:
    # Si estamos en Railway, ajustamos el protocolo para SQLAlchemy asíncrono
    # Cambiamos mysql:// por mysql+aiomysql://
    DATABASE_URL = RAW_URL.replace("mysql://", "mysql+aiomysql://")
    print("🚀 IALibre detectó entorno CLOUD (Railway). Conectando...")
else:
    # Si no hay MYSQL_URL, estamos en local (Notebook en Fresia)
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "ialibre")
    
  DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print(f"🏠 IALibre detectó entorno LOCAL (Fresia). Conectando a {DB_HOST}...")

# --- CONFIGURACIÓN DEL MOTOR (ENGINE) ---
engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,    # Verifica si la conexión sigue viva antes de usarla
    pool_recycle=30,       # Recicla conexiones cada 30 segundos para evitar cortes de Railway
    connect_args={
        "connect_timeout": 60,
        "program_name": "IALibre_PrensaLagos" 
    }
)

AsyncSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

Base = declarative_base()

# --- DEPENDENCIAS Y UTILIDADES ---
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    try:
        async with engine.begin() as conn:
            # Crea las tablas si no existen
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Conexión Blindada: Base de datos sincronizada correctamente.")
    except Exception as e:
        print(f"❌ Error de enlace en la base de datos: {e}")

# --- MODELOS DE DATOS ---
class JobOffer(Base):
    __tablename__ = "job_offers"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    company = Column(String(255))
    description = Column(Text)
    location = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

class JobDemand(Base):
    __tablename__ = "job_demands"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255))
    skills = Column(Text)
    experience_years = Column(Integer)
    contact_info = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)