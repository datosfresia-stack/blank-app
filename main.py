from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
import os
import uvicorn

# Importamos solo lo que necesitamos
from memoria_database import get_db, iniciar_base_datos, EnciclopediaNodos

# Iniciar Servidor
app = FastAPI()

# Arranque del sistema
@app.on_event("startup")
async def encender():
    print("🚀 INICIANDO...")
    await iniciar_base_datos()
    print("✅ SISTEMA LISTO")

# Rutas Web
@app.get("/")
def ir():
    return RedirectResponse(url="/terminal")

@app.get("/terminal", response_class=HTMLResponse)
def ver_chat():
    return FileResponse("index.html")

# Formato de lo que escribe el usuario
class DatoEntrada(BaseModel):
    mensaje: str

# Lógica: Guardar y Responder
@app.post("/nucleo-procesar")
async def procesar(datos: DatoEntrada, db: AsyncSession = Depends(get_db)):
    texto = datos.mensaje.strip()

    # ENSEÑAR: Si tiene ---
    if "---" in texto:
        try:
            partes = texto.split("---", 1)
            tema = partes[0].strip()
            contenido = partes[1].strip()

            nuevo = EnciclopediaNodos(tema=tema, contenido=contenido)
            db.add(nuevo)
            await db.commit()
            return {"respuesta": f"✅ GUARDADO\n📌 Tema: {tema}"}
        except Exception as e:
            return {"respuesta": f"❌ ERROR: {str(e)}"}

    # PREGUNTAR: Buscar en la base
    else:
        resultado = await db.execute(
            select(EnciclopediaNodos).where(EnciclopediaNodos.tema.ilike(f"%{texto}%")).limit(1)
        )
        dato = resultado.scalar_one_or_none()

        if dato:
            return {"respuesta": f"🧠 NÚCLEO:\n\n{dato.contenido}"}
        else:
            return {"respuesta": f"❌ No sé sobre: '{texto}'\n\nEnseña así:\nTema --- Explicación"}

# Puerto para Railway
if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=puerto)