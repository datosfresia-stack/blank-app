import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func

# ==================================================
# 🗄️ CONFIGURACIÓN DE CONEXIÓN MARIADB (RAILWAY)
# ==================================================
DATABASE_URL = "mysql+aiomysql://root:E7hZ5nq8FrmUL4iSeRP1bvel5cDkQVil@mariadb.cba9.up.railway.app:3306/railway"

if os.getenv("USAR_PUBLICO") == "si":
    DATABASE_URL = "mysql+aiomysql://root:E7hZ5nq8FrmUL4iSeRP1bvel5cDkQVil@nozomi.proxy.rlwy.net:18384/railway"

# 🚀 MOTOR DE CONEXIÓN
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=10,
    max_overflow=15
)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# ==================================================
# 📚 ÁREAS DE INTERÉS
# ==================================================
AREAS_CONOCIMIENTO = [
    "informatica",
    "robotica",
    "neurociencia",
    "medicina",
    "electronica",
    "redes_neuronales",
    "redes_cuanticas",
    "programacion",
    "medicina_ancestral",
    "biotecnologia",
    "general"
]

# ==================================================
# 📋 TABLAS
# ==================================================
class ConsultasMedicas(Base):
    __tablename__ = "consultas_medicas"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    edad = Column(Integer, nullable=True)
    presion = Column(Integer, nullable=True)
    frecuencia = Column(Integer, nullable=True)
    saturacion = Column(Integer, nullable=True)
    hipertenso = Column(String(10), nullable=True)
    ubicacion = Column(String(100), nullable=True)
    nivel_riesgo = Column(String(50), nullable=True)
    fecha_registro = Column(TIMESTAMP, server_default=func.now())

class EnciclopediaNodos(Base):
    __tablename__ = "enciclopedia_nodos"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    area = Column(String(100), index=True, nullable=False, default="general")
    tema = Column(String(255), index=True, nullable=False)
    contenido = Column(Text, nullable=False)
    requisitos = Column(Text, nullable=True)
    fecha_guardado = Column(TIMESTAMP, server_default=func.now())

# ==================================================
# 🔌 FUNCIONES DE CONEXIÓN
# ==================================================
async def get_db():
    async with AsyncSessionLocal() as sesion:
        try:
            yield sesion
        finally:
            await sesion.close()

async def iniciar_base_datos():
    try:
        async with engine.begin() as conexion:
            await conexion.run_sync(Base.metadata.create_all)
        print("✅ [NÚCLEO]: Base de Datos conectada e inicializada.")
    except Exception as error_conexion:
        print(f"❌ [NÚCLEO ERROR]: {error_conexion}")
        os.environ["USAR_PUBLICO"] = "si"