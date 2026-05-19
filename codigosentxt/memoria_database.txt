import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Text, Float, TIMESTAMP, func

# 🌍 CONFIGURACIÓN DE RUTAS DINÁMICAS (LOCAL VS RAILWAY)
# Priorizamos MYSQL_URL de Railway con el driver asíncrono aiomysql
DATABASE_URL = os.getenv("MYSQL_URL")

if DATABASE_URL:
    # Corrección de protocolo para asegurar compatibilidad asíncrona en Railway
    if DATABASE_URL.startswith("mysql://"):
        DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+aiomysql://")
    elif DATABASE_URL.startswith("mariadb://"):
        DATABASE_URL = DATABASE_URL.replace("mariadb://", "mysql+aiomysql://")
else:
    # Entorno de desarrollo local aislado
    DATABASE_URL = "sqlite+aiosqlite:///./base_prueba.db"

# 🚀 MOTOR DE CONEXIÓN ASÍNCRONO DE ALTA DISPONIBILIDAD
engine = create_async_engine(
    DATABASE_URL, 
    echo=False, 
    pool_pre_ping=True,  # Verifica si la conexión sigue viva antes de usarla
    pool_recycle=300,    # Evita el timeout desconectando sockets caídos cada 5 min
    pool_size=10,        # Número máximo de conexiones simultáneas en horas pico
    max_overflow=20      # Conexiones extra permitidas en ráfagas de tráfico
)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


# 📋 SECTOR 1: MODELO PARA CONSULTAS MÉDICAS Y PARÁMETROS BIOMÉDRICOS
class ConsultasMedicas(Base):
    __tablename__ = "consultas_medicas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    edad = Column(Integer, nullable=True)
    presion = Column(Integer, nullable=True)
    frecuencia = Column(Integer, nullable=True)
    saturacion = Column(Integer, nullable=True)
    hipertenso = Column(String(10), nullable=True)
    sur_chile = Column(String(10), nullable=True)
    nivel_riesgo = Column(String(50), nullable=True)
    fecha = Column(TIMESTAMP, server_default=func.now())


# 📋 SECTOR 2: MODELO DE ENCICLOPEDIA RELACIONAL (RAG DE TUS 4 PESTAÑAS)
class EnciclopediaNodos(Base):
    __tablename__ = "enciclopedia_nodos"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    area = Column(String(100), index=True, nullable=False) # chat_directo, ingenieria, peliculas, evolucion
    concepto = Column(String(255), index=True, nullable=False)
    definicion_profunda = Column(Text, nullable=False) # Soporta textos largos y códigos fuentes masivos
    requisitos_previos = Column(Text, nullable=True)
    fecha_indexacion = Column(TIMESTAMP, server_default=func.now())


# 🔌 GENERADOR DE SESIONES ASÍNCRONAS PARA LOS ENDPOINTS
async def get_db():
    async with AsyncSessionLocal() as sesion:
        try:
            yield sesion
        finally:
            await sesion.close()


# 🛠️ INICIALIZADOR AUTOMÁTICO DE LA ESTRUCTURA COGNITIVA
async def init_db():
    """Crea las tablas asíncronas en MariaDB al arrancar el contenedor"""
    try:
        async with engine.begin() as conexion:
            await conexion.run_sync(Base.metadata.create_all)
        print("🛸 [Memoria Database]: Modelos relacionales asíncronos inicializados con éxito.")
    except Exception as e:
        print(f"⚠️ [Alerta Database]: No se pudieron sincronizar las tablas asíncronas: {e}")