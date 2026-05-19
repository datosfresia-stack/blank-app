import os
import pymysql
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import uvicorn

app = FastAPI(title="IA Núcleo - Paso a Paso")

# Configuración de los datos de acceso a tu MariaDB en Railway
DB_CONFIG = {
    'host': 'nozomi.proxy.rlwy.net',
    'port': 18384,
    'user': 'root',
    'password': 'E7hZ5nq8FrmUL4iSeRP1bvel5cDkQVil',
    'database': 'railway',
    'autocommit': True
}

# El modelo de datos que espera recibir el endpoint
class EntradaFrase(BaseModel):
    frase: str
    respuesta: str = None  # Es opcional. Si viene, el sistema aprende.

# =====================================================================
# RUTA PRINCIPAL: Para que la URL pública muestre que está vivo
# =====================================================================
@app.get("/")
def bienvenida():
    return {
        "status": "Online",
        "sistema": "IA Núcleo",
        "mensaje": "El motor central está operativo y listo para conectar con la interfaz."
    }

# =====================================================================
# RUTA NÚCLEO: Consulta y Aprendizaje interactivo
# =====================================================================
@app.post("/nucleo")
def procesar_nucleo(datos: EntradaFrase):
    frase_limpia = datos.frase.strip()
    if not frase_limpia:
        return {"respuesta": "🤖 Núcleo: Transmisión vacía."}

    # Intentamos abrir la conexión a MariaDB solo cuando llega la petición
    try:
        conexion = pymysql.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database'],
            autocommit=DB_CONFIG['autocommit']
        )
    except Exception as e:
        return {"respuesta": f"🤖 Núcleo: Error de conexión con MariaDB: {e}"}

    try:
        with conexion.cursor() as cursor:
            # MODO 1: APRENDER (Si envías una frase junto con una respuesta)
            if datos.respuesta:
                query_insert = """
                    INSERT INTO enciclopedia_nodos 
                    (nodo_nombre, tipo, descripcion, respuesta_asociada, fecha_creacion, estado) 
                    VALUES (%s, 'General', 'Aprendizaje Directo', %s, %s, 'Activo')
                """
                cursor.execute(query_insert, (frase_limpia, datos.respuesta.strip(), datetime.now()))
                return {"respuesta": f"🤖 Núcleo: Entendido. He indexado y aprendido la frase '{frase_limpia}'."}
            
            # MODO 2: CONSULTAR (Si sólo envías la frase para saber qué responder)
            else:
                query_select = """
                    SELECT respuesta_asociada 
                    FROM enciclopedia_nodos 
                    WHERE nodo_nombre LIKE %s AND estado = 'Activo' 
                    LIMIT 1
                """
                # Usamos LIKE con % para que busque coincidencias aunque no sea idéntico
                cursor.execute(query_select, (f"%{frase_limpia}%",))
                resultado = cursor.fetchone()
                
                if resultado:
                    return {"respuesta": f"🤖 Núcleo: {resultado[0]}"}
                return {"respuesta": f"🤖 Núcleo: No tengo registros de la frase '{frase_limpia}'."}
                
    except Exception as error:
        return {"respuesta": f"🤖 Núcleo: Error interno en la base de datos: {error}"}
    finally:
        conexion.close()

# Servidor de arranque estándar para Railway
if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=puerto, reload=False)