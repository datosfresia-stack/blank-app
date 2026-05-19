import os
import pymysql
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import uvicorn

app = FastAPI(title="IA Núcleo")

DB_CONFIG = {
    'host': 'nozomi.proxy.rlwy.net',
    'port': 18384,
    'user': 'root',
    'password': 'E7hZ5nq8FrmUL4iSeRP1bvel5cDkQVil',
    'database': 'railway',
    'autocommit': True
}

class EntradaFrase(BaseModel):
    frase: str
    respuesta: str = None  # Si viene con respuesta, aprende. Si no, consulta.

# Ruta única para el funcionamiento de Núcleo
@app.post("/nucleo")
def procesar_nucleo(datos: EntradaFrase):
    frase_limpia = datos.frase.strip()
    if not frase_limpia:
        return {"respuesta": "🤖 Núcleo: Transmisión vacía."}

    try:
        conexion = pymysql.Connect(
            host=DB_CONFIG['host'], port=DB_CONFIG['port'],
            user=DB_CONFIG['user'], password=DB_CONFIG['password'],
            database=DB_CONFIG['database'], autocommit=DB_CONFIG['autocommit']
        )
    except Exception:
        return {"respuesta": "🤖 Núcleo: Error de conexión con MariaDB."}

    try:
        with conexion.cursor() as cursor:
            # MODO APRENDIZAJE: Si le envías una respuesta junto con la frase
            if datos.respuesta:
                query_insert = """
                    INSERT INTO enciclopedia_nodos 
                    (nodo_nombre, tipo, descripcion, respuesta_asociada, fecha_creacion, estado) 
                    VALUES (%s, 'General', 'Aprendizaje Directo', %s, %s, 'Activo')
                """
                cursor.execute(query_insert, (frase_limpia, datos.respuesta.strip(), datetime.now()))
                return {"respuesta": f"🤖 Núcleo: He aprendido la frase '{frase_limpia}'."}
            
            # MODO CONSULTA: Si solo envías la frase, busca qué responder
            else:
                query_select = "SELECT respuesta_asociada FROM enciclopedia_nodos WHERE nodo_nombre = %s AND estado = 'Activo' LIMIT 1"
                cursor.execute(query_select, (frase_limpia,))
                resultado = cursor.fetchone()
                
                if resultado:
                    return {"respuesta": f"🤖 Núcleo: {resultado[0]}"}
                return {"respuesta": f"🤖 Núcleo: No conozco la frase '{frase_limpia}'. Envíala con una respuesta para guardarla."}
    except Exception as e:
        return {"respuesta": f"🤖 Núcleo: Error interno en el proceso: {e}"}
    finally:
        conexion.close()

@app.get("/")
def estado():
    return {"sistema": "Núcleo", "modo": "Paso a Paso", "status": "Online"}

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=puerto, reload=False)