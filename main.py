import os
import pymysql
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import uvicorn

app = FastAPI()

class EntradaFrase(BaseModel):
    frase: str
    respuesta: str = None

@app.get("/")
def estado():
    return {"status": "Online", "sistema": "Núcleo", "modo": "Paso a Paso de Miguel"}

@app.post("/nucleo")
def procesar_nucleo(datos: EntradaFrase):
    frase_limpia = datos.frase.strip()
    if not frase_limpia:
        return {"respuesta": "🤖 Núcleo: Transmisión vacía."}

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
        return {"respuesta": f"🤖 Núcleo: Error de conexión con MariaDB: {e}"}

    try:
        with conexion.cursor() as cursor:
            # APRENDER (si mandas frase + respuesta)
            if datos.respuesta:
                query_insert = """
                    INSERT INTO enciclopedia_nodos 
                    (nodo_nombre, tipo, descripcion, respuesta_asociada, fecha_creacion, estado) 
                    VALUES (%s, 'General', 'Aprendizaje Directo', %s, %s, 'Activo')
                """
                cursor.execute(query_insert, (frase_limpia, datos.respuesta.strip(), datetime.now()))
                return {"respuesta": f"🤖 Núcleo: He aprendido la frase '{frase_limpia}'."}
            
            # CONSULTAR (si mandas solo frase)
            else:
                query_select = "SELECT respuesta_asociada FROM enciclopedia_nodos WHERE nodo_nombre = %s AND estado = 'Activo' LIMIT 1"
                cursor.execute(query_select, (frase_limpia,))
                resultado = cursor.fetchone()
                
                if resultado:
                    return {"respuesta": f"🤖 Núcleo: {resultado[0]}"}
                return {"respuesta": f"🤖 Núcleo: No conozco la frase '{frase_limpia}'."}
    except Exception as error:
        return {"respuesta": f"🤖 Núcleo: Error interno: {error}"}
    finally:
        conexion.close()

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=puerto, reload=False)