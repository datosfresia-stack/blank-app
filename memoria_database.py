from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Text
import os

# ✅ CORRECCIÓN CLAVE: Usamos "aiomysql" en lugar de "mysqldb"
if os.getenv("RAILWAY_ENVIRONMENT"):
    # Aquí estaba el error: cambiamos la palabra para que reconozca el módulo instalado
    DATABASE_URL = os.getenv("MYSQL_URL", "").replace("mysql://", "mysql+aiomysql://")
else:
    # En tu PC sigue usando la base interna para que no falle
    DATABASE_URL = "sqlite+aiosqlite:///./base_prueba.db"

engine = create_async_engine(
    DATABASE_URL, 
    echo=False, 
    pool_pre_ping=True, 
    pool_recycle=300
)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# 📋 ESTRUCTURA PARA TUS 3 PESTAÑAS: LAB | CINE | AUTOEVOLUCION
class MatrizConocimiento(Base):
    __tablename__ = "conocimiento"
    id = Column(Integer, primary_key=True, index=True)
    categoria = Column(String(50), index=True)  # Aquí se guarda LAB, CINE o AUTOEVOLUCION
    concepto = Column(Text)
    detalles = Column(Text)

# 🔌 CONEXIÓN
async def get_db():
    async with AsyncSessionLocal() as sesion:
        yield sesion

# 🛠️ CREAR TABLAS SI NO EXISTEN
async def init_db():
    async with engine.begin() as conexion:
        await conexion.run_sync(Base.metadata.create_all)