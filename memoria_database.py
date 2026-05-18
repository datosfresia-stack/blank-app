from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# ✅ USAMOS LA URL QUE RAILWAY YA CREÓ POR TI (ES LA MÁS SEGURA)
# Detecta si está en la nube o en tu PC
if os.getenv("RAILWAY_ENVIRONMENT"):
    # En Railway: usamos la variable que ya existe (la que ves en pantalla)
    DATABASE_URL = os.getenv("MYSQL_URL", "").replace("mysql://", "mysql+aiomysql://")
else:
    # En tu PC: dirección local
    DATABASE_URL = "mysql+aiomysql://root@localhost:3306/prueba"

# ⚙️ MOTOR DE CONEXIÓN AJUSTADO PARA NO DESCONECTARSE
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"connect_timeout": 10}
)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# 📦 MODELO DE DATOS (IGUAL QUE ANTES)
class MatrizConocimiento(Base):
    __tablename__ = "matriz_conocimiento"
    id = Base.Column(Base.Integer, primary_key=True, index=True)
    categoria = Base.Column(Base.String(50), index=True)
    concepto = Base.Column(Base.Text)
    detalles = Base.Column(Base.Text)

# 🔌 CONEXIÓN
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# 🛠️ CREAR TABLAS
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)