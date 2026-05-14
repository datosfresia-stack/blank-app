import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Text

# --- CONFIGURACIÓN DE CONEXIÓN ---
# Se prioriza la variable de entorno de Railway
RAW_URL = os.getenv("MYSQL_URL")

if RAW_URL:
    # Garantizamos el uso del driver asíncrono aiomysql
    if RAW_URL.startswith("mysql://"):
        DATABASE_URL = RAW_URL.replace("mysql://", "mysql+aiomysql://")
    else:
        DATABASE_URL = RAW_URL
    print("🚀 IALibre detectó entorno CLOUD (Railway). Conectando...")
else:
    # Configuración local de respaldo
    DATABASE_URL = "mysql+aiomysql://root:password@localhost:3306/ialibre_db"
    print("🏠 IALibre detectó entorno LOCAL.")

# --- MOTOR Y SESIÓN ASÍNCRONA ---
engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
AsyncSessionLocal = sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)
Base = declarative_base()

# --- MODELO DE DATOS ---
class JobDemand(Base):
    __tablename__ = "job_demands"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255))
    skills = Column(String(255))
    experience_years = Column(Integer, default=0)
    contact_info = Column(Text)

# --- UTILIDADES ---
async def init_db():
    async with engine.begin() as conn:
        # Crea las tablas si no existen en MariaDB
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Conexión Blindada: Tablas sincronizadas.")

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session