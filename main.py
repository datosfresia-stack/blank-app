import os
import pymysql
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class EntradaFrase(BaseModel):
    frase: str
    respuesta: str = None

@app.get("/")
def estado():
    # Esta ruta es limpia y rápida para mantener a Railway en verde permanente
    return {"status": "Online", "sistema": "Núcleo Base"}

@app.post("/nucleo")
def procesar_nucleo(datos: EntradaFrase):
    frase_limpia = datos.frase.strip()
    if not frase_limpia:
        return {"respuesta": "🤖 Transmisión vacía."}

    # La conexión se define e intenta solo al recibir una petición
    try:
        conexion = pymysql.connect(
            host='nozomi.proxy.rlwy.net',
            port=18384,
            user='root',
            password='E7hZ5nq8FrmUL4iSeRP1bvel5cDkQVil',
            database='railway',
            autocommit=True
        )
    except Exception as e:
        return {"respuesta": f"🤖 Error de enlace con MariaDB: {e}"}

    try:
        with conexion.cursor() as cursor:
            if datos.respuesta:
                # Aprender
                query = "INSERT INTO enciclopedia_nodos (nodo_nombre, tipo, descripcion, respuesta_asociada, estado) VALUES (%s, 'General', 'Base', %s, 'Activo')"
                cursor.execute(query, (frase_limpia, datos.respuesta.strip()))
                return {"respuesta": f"🤖 Aprendido: '{frase_limpia}'."}
            else:
                # Consultar
                query = "SELECT respuesta_asociada FROM enciclopedia_nodos WHERE nodo_nombre = %s AND estado = 'Activo' LIMIT 1"
                cursor.execute(query, (frase_limpia,))
                resultado = cursor.fetchone()
                if resultado:
                    return {"respuesta": f"🤖 Núcleo: {resultado[0]}"}
                return {"respuesta": f"🤖 No conozco: '{frase_limpia}'."}
    except Exception as error:
        return {"respuesta": f"🤖 Error de lectura: {error}"}
    finally:
        conexion.close()

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=puerto, reload=False)