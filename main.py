# ==================================================
# 🧠 NÚCLEO IA - ARCHIVO PRINCIPAL
# ==================================================
import os
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# ✅ IMPORTACIÓN CORRECTA (Solo desde el otro archivo)
from memoria_database import get_db, iniciar_base_datos, EnciclopediaNodos, AREAS_CONOCIMIENTO

# ⚙️ CONFIGURACIÓN
app = FastAPI(title="Núcleo IA", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🚀 ARRANQUE
@app.on_event("startup")
async def encender_sistema():
    print("🛸 Iniciando NÚCLEO...")
    await iniciar_base_datos()
    print("✅ Sistema listo.")

# 🗺️ RUTAS
@app.get("/")
def ir_a_terminal():
    return RedirectResponse(url="/terminal")

@app.get("/terminal", response_class=HTMLResponse)
def mostrar_consola():
    ruta_archivo = os.path.join(os.path.dirname(__file__), "index.html")
    return FileResponse(ruta_archivo)

# 📥 ESTRUCTURA
class EntradaUsuario(BaseModel):
    mensaje: str

# 🧠 LÓGICA
@app.post("/nucleo-procesar")
async def procesar_entrada(datos: EntradaUsuario, db: AsyncSession = Depends(get_db)):
    texto_recibido = datos.mensaje.strip()

    # MODO GUARDAR
    if "---" in texto_recibido:
        try:
            partes = texto_recibido.split("---", 1)
            tema_a_guardar = partes[0].strip()
            contenido_a_guardar = partes[1].strip()

            nuevo_conocimiento = EnciclopediaNodos(
                area="general",
                tema=tema_a_guardar,
                contenido=contenido_a_guardar
            )
            db.add(nuevo_conocimiento)
            await db.commit()
            await db.refresh(nuevo_conocimiento)

            return {
                "respuesta": f"✅ GUARDADO\n📌 Tema: {tema_a_guardar}\n💾 ID: {nuevo_conocimiento.id}",
                "estado": "exitoso"
            }
        except Exception as e:
            return {"respuesta": f"❌ Error: {str(e)}", "estado": "error"}

    # MODO BUSCAR
    else:
        try:
            busqueda = select(EnciclopediaNodos).where(
                EnciclopediaNodos.tema.ilike(f"%{texto_recibido}%")
            ).limit(1)

            resultado = await db.execute(busqueda)
            dato_encontrado = resultado.scalar_one_or_none()

            if dato_encontrado:
                return {
                    "respuesta": f"🧠 NÚCLEO:\n\n{dato_encontrado.contenido}",
                    "estado": "encontrado"
                }
            else:
                return {
                    "respuesta": f"❌ No tengo datos de: '{texto_recibido}'\n\n💡 Enseñame así:\nTema --- Información...",
                    "estado": "sin_datos"
                }
        except Exception as e:
            return {"respuesta": f"⚠️ Error: {str(e)}", "estado": "error"}

# 🚀 SERVIDOR
if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=puerto, reload=False)