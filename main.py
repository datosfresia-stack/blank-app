import os
import pymysql
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import uvicorn

app = FastAPI()

DB_CONFIG = {
    'host': 'nozomi.proxy.rlwy.net',
    'port': 18384,
    'user': 'root',
    'password': 'E7hZ5nq8FrmUL4iSeRP1bvel5cDkQVil',
    'database': 'railway'
}

class EntradaFrase(BaseModel):
    frase: str
    respuesta: str = None

@app.post("/nucleo")
def procesar_nucleo(datos: EntradaFrase):
    frase_limpia = datos.frase.strip()
    if not frase_limpia:
        return {"respuesta": "🤖 Núcleo: Transmisión vacía."}

    try:
        # CORREGIDO: 'connect' completamente en minúsculas para evitar caídas
        conexion = pymysql.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database'],
            autocommit=True
        )
    except Exception:
        return {"respuesta": "🤖 Núcleo: Error de conexión con MariaDB."}

    try:
        with conexion.cursor() as cursor:
            # Si envías una respuesta junto con la frase, la guarda (Aprende)
            if datos.respuesta:
                query_insert = """
                    INSERT INTO enciclopedia_nodos 
                    (nodo_nombre, tipo, descripcion, respuesta_asociada, fecha_creacion, estado) 
                    VALUES (%s, 'General', 'Aprendizaje Directo', %s, %s, 'Activo')
                """
                cursor.execute(query_insert, (frase_limpia, datos.respuesta.strip(), datetime.now()))
                return {"respuesta": f"🤖 Núcleo: He aprendido la frase '{frase_limpia}'."}
            
            # Si solo envías la frase, busca qué responder (Consulta)
            else:
                query_select = "SELECT respuesta_asociada FROM enciclopedia_nodos WHERE nodo_nombre = %s AND estado = 'Activo' LIMIT 1"
                cursor.execute(query_select, (frase_limpia,))
                resultado = cursor.fetchone()
                
                if resultado:
                    return {"respuesta": f"🤖 Núcleo: {resultado[0]}"}
                return {"respuesta": f"🤖 Núcleo: No conozco la frase '{frase_limpia}'."}
    except Exception as e:
        return {"respuesta": f"🤖 Núcleo: Error en proceso: {e}"}
    finally:
        conexion.close()

@app.get("/")
def estado():
    return {"status": "Online", "sistema": "Núcleo Simplificado"}

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=puerto, reload=False)