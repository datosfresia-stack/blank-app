import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Text

# --- CONFIGURACIÓN DE CONEXIÓN ---
# Forzamos el uso de aiomysql para evitar el error "ModuleNotFoundError: No module named 'MySQLdb'"
RAW_URL = os.getenv("MYSQL_URL")

if RAW_URL:
    # Si la URL empieza con mysql://, la cambiamos a mysql+aiomysql://
    if RAW_URL.startswith("mysql://"):
        DATABASE_URL = RAW_URL.replace("mysql://", "mysql+aiomysql://", 1)
    # Si por alguna razón Railway entrega mariadb://, también la ajustamos
    elif RAW_URL.startswith("mariadb://"):
        DATABASE_URL = RAW_URL.replace("mariadb://", "mysql+aiomysql://", 1)
    else:
        DATABASE_URL = RAW_URL
    print("🚀 Entorno CLOUD: Usando conector asíncrono aiomysql")
else:
    # Conexión local de respaldo
    DATABASE_URL = "mysql+aiomysql://root:password@localhost:3306/ialibre_db"
    print("🏠 Entorno LOCAL")

# --- MOTOR Y SESIÓN ---
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

# --- INICIALIZACIÓN ---
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Base de datos lista.")

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session