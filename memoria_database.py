from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Text
import os

# ✅ AHORA SE CONECTA A LO QUE TENEMOS EN RAILWAY
if os.getenv("RAILWAY_ENVIRONMENT"):
    # Usamos la variable que ya está creada allá (MYSQL_URL)
    DATABASE_URL = os.getenv("MYSQL_URL", "").replace("mysql://", "mysql+aiomysql://")
else:
    # En tu PC sigue usando la interna (para que siga funcionando aquí)
    DATABASE_URL = "sqlite+aiosqlite:///./base_prueba.db"

engine = create_async_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class MatrizConocimiento(Base):
    __tablename__ = "conocimiento"
    id = Column(Integer, primary_key=True, index=True)
    categoria = Column(String(50))
    concepto = Column(Text)
    detalles = Column(Text)

async def get_db():
    async with AsyncSessionLocal() as sesion:
        yield sesion

async def init_db():
    async with engine.begin() as conexion:
        await conexion.run_sync(Base.metadata.create_all)