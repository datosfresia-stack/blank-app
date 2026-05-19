import os
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class EntradaFrase(BaseModel):
    frase: str
    respuesta: str = None

@app.get("/")
def estado():
    return {"status": "Online", "mensaje": "Prueba de vida de Nucleo sin librerias externas"}

@app.post("/nucleo")
def procesar_nucleo(datos: EntradaFrase):
    # Sin base de datos por ahora, solo responde de vuelta lo que le mandas
    return {
        "respuesta": f"🤖 Núcleo recibió: {datos.frase}. Modo de prueba activo."
    }

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=puerto, reload=False)