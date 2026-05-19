from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func

# ✅ CONEXIÓN EXACTA QUE SÍ FUNCIONA
DATABASE_URL = "mysql+aiomysql://root:E7hZ5nq8FrmUL4iSeRP1bvel5cDkQVil@nozomi.proxy.rlwy.net:18384/railway"

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# 📋 ESTRUCTURA DE LA TABLA
class EnciclopediaNodos(Base):
    __tablename__ = "enciclopedia_nodos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tema = Column(String(255), nullable=False)
    contenido = Column(Text, nullable=False)
    fecha_guardado = Column(TIMESTAMP, server_default=func.now())

# 🔌 CONEXIONES
async def get_db():
    async with AsyncSessionLocal() as sesion:
        yield sesion

async def iniciar_base_datos():
    async with engine.begin() as conexion:
        await conexion.run_sync(Base.metadata.create_all)
    print("✅ BASE DE DATOS CONECTADA")