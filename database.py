import os
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# CONFIGURACIÓN ANTICORTES PARA RAILWAY
# Reemplace la sección del engine en su database.py con esto:
engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=30,
    connect_args={
        "connect_timeout": 60,
        # Esto obliga a enviar la contraseña correctamente
        "program_name": "IALibre_Fresia" 
    }
)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Conexión Blindada: Tablas sincronizadas en Railway.")
    except Exception as e:
        print(f"❌ Error de enlace: {e}")

# MODELOS
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