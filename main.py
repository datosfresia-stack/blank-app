# ==================================================
# 🧠 NÚCLEO IA - SERVIDOR PRINCIPAL
# ==================================================
import os
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Importación correcta
from memoria_database import get_db, iniciar_base_datos, EnciclopediaNodos, AREAS_CONOCIMIENTO

# Iniciar App
app = FastAPI(title="Núcleo IA")

# Reglas de acceso
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Arranque
@app.on_event("startup")
async def encender():
    print("🚀 Iniciando Sistema...")
    await iniciar_base_datos()
    print("✅ Sistema Listo")

# Rutas
@app.get("/")
def raiz():
    return RedirectResponse(url="/terminal")

@app.get("/terminal", response_class=HTMLResponse)
def ver_terminal():
    ruta = os.path.join(os.path.dirname(__file__), "index.html")
    return FileResponse(ruta)

# Estructura datos
class DatoEntrada(BaseModel):
    mensaje: str

# Lógica Inteligencia
@app.post("/nucleo-procesar")
async def procesar(datos: DatoEntrada, db: AsyncSession = Depends(get_db)):
    texto = datos.mensaje.strip()

    # ENSEÑAR
    if "---" in texto:
        try:
            partes = texto.split("---", 1)
            tema = partes[0].strip()
            info = partes[1].strip()

            nuevo = EnciclopediaNodos(area="general", tema=tema, contenido=info)
            db.add(nuevo)
            await db.commit()
            await db.refresh(nuevo)

            return {"respuesta": f"✅ GUARDADO\n📌 Tema: {tema}\n💾 ID: {nuevo.id}"}
        except Exception as e:
            return {"respuesta": f"❌ Error: {str(e)}"}

    # CONSULTAR
    else:
        try:
            resultado = await db.execute(
                select(EnciclopediaNodos).where(EnciclopediaNodos.tema.ilike(f"%{texto}%")).limit(1)
            )
            dato = resultado.scalar_one_or_none()

            if dato:
                return {"respuesta": f"🧠 NÚCLEO:\n\n{dato.contenido}"}
            else:
                return {"respuesta": f"❌ No sé sobre: '{texto}'\n\nEnseñame así:\nTema --- Explicación..."}
        except Exception as e:
            return {"respuesta": f"⚠️ Error: {str(e)}"}

# Puerto Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)