import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Text

# --- LECTURA DE VARIABLES DE RAILWAY ---
RAW_URL = os.getenv("MYSQL_URL")

if RAW_URL:
    # Convertimos el formato mariadb:// a uno compatible con el conector
    if RAW_URL.startswith("mariadb://"):
        DATABASE_URL = RAW_URL.replace("mariadb://", "mysql+aiomysql://", 1)
    else:
        DATABASE_URL = RAW_URL
    print("🚀 Conectando a la base de datos en la nube...")
else:
    # Si falla la URL armamos la conexión con los datos separados
    USER = os.getenv("DB_USER")
    PASS = os.getenv("DB_PASSWORD")
    HOST = os.getenv("DB_HOST")
    PORT = os.getenv("DB_PORT")
    NAME = os.getenv("DB_NAME")
    DATABASE_URL = f"mysql+aiomysql://{USER}:{PASS}@{HOST}:{PORT}/{NAME}"
    print("🚀 Conexión armada manualmente...")

# --- MOTOR Y SESIÓN ---
engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
AsyncSessionLocal = sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)
Base = declarative_base()

# --- ESTRUCTURA DE LA TABLA ---
class MatrizConocimiento(Base):
    __tablename__ = "matriz_conocimiento"
    id = Column(Integer, primary_key=True, index=True)
    categoria = Column(String(100))
    concepto = Column(String(255))
    detalles = Column(Text)

# --- INICIALIZACIÓN ---
async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Base de datos conectada y tabla creada/verificada.")
    except Exception as e:
        print(f"❌ ERROR DE CONEXIÓN: {e}")

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session