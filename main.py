import os
import pymysql
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymysql.cursors import DictCursor
from datetime import datetime
import uvicorn

app = FastAPI(title="IA Núcleo", description="Chat, Núcleo, Cine y Auto Evolución")

# =====================================================================
# CONEXIÓN DIRECTA A TU MARIADB DE RAILWAY
# =====================================================================
DB_CONFIG = {
    'host': 'nozomi.proxy.rlwy.net',
    'port': 18384,
    'user': 'root',
    'password': 'E7hZ5nq8FrmUL4iSeRP1bvel5cDkQVil',
    'database': 'railway',
    'autocommit': True
}

def conectar_db():
    try:
        return pymysql.connect(**DB_CONFIG)
    except Exception:
        return None

# Modelos para recibir los datos de tu interfaz
class MensajeChat(BaseModel):
    mensaje: str

class RegistroNodo(BaseModel):
    nodo: str
    area: str
    descripcion: str
    respuesta: str

# =====================================================================
# RUTAS DE TU INTERFAZ (CHAT, NÚCLEO, CINE, AUTO EVOLUCIÓN)
# =====================================================================

@app.post("/chat")
def seccion_chat(datos: MensajeChat):
    entrada = datos.mensaje.strip()
    if not entrada:
        return {"respuesta": "🤖 Núcleo: En espera de transmisión..."}
        
    conexion = conectar_db()
    if not conexion:
        return {"respuesta": "🤖 Núcleo: Almacenamiento local desconectado."}
        
    try:
        with conexion.cursor() as cursor:
            query = "SELECT respuesta_asociada FROM enciclopedia_nodos WHERE nodo_nombre LIKE %s AND estado = 'Activo' LIMIT 1"
            cursor.execute(query, (f"%{entrada}%",))
            resultado = cursor.fetchone()
            
        if resultado:
            return {"respuesta": resultado[0]}
        else:
            return {"respuesta": f"🤖 Concepto '{entrada}' no indexado. Registra este nodo en la pestaña de Auto Evolución para que pueda recordarlo."}
    except Exception:
        return {"respuesta": "🤖 Error en los canales de memoria interna."}
    finally:
        conexion.close()

@app.get("/nucleo")
def seccion_nucleo(buscar: str = None):
    conexion = conectar_db()
    if not conexion:
        raise HTTPException(status_code=500, detail="Cerebro MariaDB fuera de línea.")
        
    try:
        with conexion.cursor(DictCursor) as cursor:
            if buscar:
                cursor.execute("SELECT * FROM enciclopedia_nodos WHERE nodo_nombre = %s", (buscar,))
                return cursor.fetchone() or {"mensaje": "Nodo no encontrado."}
            else:
                cursor.execute("SELECT id, nodo_nombre, tipo, descripcion FROM enciclopedia_nodos ORDER BY id DESC")
                return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conexion.close()

@app.get("/cine")
def seccion_cine():
    return {
        "seccion": "Cine",
        "estado": "Activo",
        "descripcion": "Repositorio y análisis de narrativa cinematográfica y guiones."
    }

@app.post("/auto-evolucion")
def seccion_auto_evolucion(datos: RegistroNodo):
    conexion = conectar_db()
    if not conexion:
        raise HTTPException(status_code=500, detail="No se pudo enlazar el almacenamiento.")
        
    try:
        with conexion.cursor() as cursor:
            query = """
                INSERT INTO_enciclopedia_nodos 
                (nodo_nombre, tipo, descripcion, respuesta_asociada, fecha_creacion, estado) 
                VALUES (%s, %s, %s, %s, %s, 'Activo')
            """
            valores = (datos.nodo.strip(), datos.area.strip(), datos.descripcion.strip(), datos.respuesta.strip(), datetime.now())
            cursor.execute(query, valores)
        return {"status": "success", "mensaje": "🤖 Núcleo ha evolucionado. Conocimiento grabado con éxito."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fallo en la indexación: {e}")
    finally:
        conexion.close()

@app.get("/")
def estado():
    return {"sistema": "Núcleo", "modo": "Soberano", "status": "Online"}

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=puerto, reload=False)