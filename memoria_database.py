from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# ⚠️ MODO PRUEBA: SIN CONEXIÓN REAL A BD
# Este archivo solo simula las funciones para que el sistema arranque
DATABASE_URL = "sqlite+aiosqlite:///./prueba.db" # Usamos una base de datos temporal interna, así no falla

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# 📦 MODELO IGUAL QUE ANTES
class MatrizConocimiento(Base):
    __tablename__ = "matriz_conocimiento"
    id = Base.Column(Base.Integer, primary_key=True, index=True)
    categoria = Base.Column(Base.String(50), index=True)
    concepto = Base.Column(Base.Text)
    detalles = Base.Column(Base.Text)

# 🔌 CONEXIÓN SIMULADA
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# 🛠️ CREAR TABLAS
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)