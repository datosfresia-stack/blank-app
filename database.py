import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Text

# --- CONFIGURACIÓN DE CONEXIÓN ---
# Se extrae la URL de Railway y se fuerza el driver aiomysql
RAW_URL = os.getenv("MYSQL_URL")

if RAW_URL:
    # Esta transformación es vital para evitar el error 'ModuleNotFoundError'
    if RAW_URL.startswith("mysql://"):
        DATABASE_URL = RAW_URL.replace("mysql://", "mysql+aiomysql://")
    else:
        DATABASE_URL = RAW_URL
    print("🚀 IALibre detectó entorno CLOUD (Railway).")
else:
    # Respaldo para pruebas locales
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
        # Esto crea la tabla en MariaDB automáticamente
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tablas sincronizadas en la nube.")

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session