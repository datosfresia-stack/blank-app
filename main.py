<<<<<<< HEAD
from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

# Importamos nuestros módulos
from memoria_database import get_db, init_db, MatrizConocimiento
from memoria_nucleo import guardar_en_memoria, obtener_memoria

app = FastAPI(title="NUCLEO PRINCIPAL")

# 🧠 LÓGICA DE RESPUESTA
def procesar_informacion(mensaje: str):
    msg = mensaje.lower()
    if "resonancia" in msg:
        return "🔄 Resonancia activada: La información se conecta y refuerza todo el conocimiento."
    elif "quién eres" in msg or "qué eres" in msg:
        return "🤖 Soy NÚCLEO, sistema autónomo. Proceso, guardo y relaciono información."
    elif "estado" in msg:
        return "📊 Sistema OPERATIVO | Base de datos y Memoria conectadas."
    elif "hola" in msg:
        return "👋 Hola. Todo en orden. ¿Qué procesamos hoy?"
    elif "recuerdas" in msg or "memoria" in msg:
        return f"💾 {obtener_memoria()}"
    else:
        return f"✅ Procesado y guardado: '{mensaje}'."

# 🖥️ INTERFAZ
@app.get("/", response_class=HTMLResponse)
async def raiz():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

# 📡 ESTRUCTURA
class DatosEntrada(BaseModel):
    mensaje: str
    canal: str

# 📡 PROCESAMIENTO
@app.post("/transmitir")
async def recibir(datos: DatosEntrada, db: AsyncSession = Depends(get_db)):
    respuesta = procesar_informacion(datos.mensaje)
    guardar_en_memoria(datos.canal, datos.mensaje, respuesta)

    # Guardar en BD
    try:
        cat = {"ingenieria":"CODE_LAB", "peliculas":"CINE_MATRIX", "evolucion":"AUTO_EVOLUCION"}.get(datos.canal, "GENERAL")
        nuevo = MatrizConocimiento(categoria=cat, concepto=datos.mensaje, detalles=respuesta)
        db.add(nuevo)
        await db.commit()
        estado = "✅ Guardado en Base y Memoria"
    except Exception as e:
        estado = f"❌ Error: {str(e)}"

    return {"respuesta": respuesta, "estado": estado}

# 🚀 ARRANQUE
@app.on_event("startup")
async def inicio():
    await init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
=======
from nucleo_autonomo_v2 import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
>>>>>>> 99d5f15fbde2402e83541437908ff6bca135880d
