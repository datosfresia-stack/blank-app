import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymysql
from pymysql.cursors import DictCursor
from datetime import datetime

app = FastAPI(title="IA Núcleo", description="Backend Soberano para Chat, Núcleo, Cine y Autoevolución")

# =====================================================================
# CONFIGURACIÓN DE TU BASE DE DATOS MARIADB (RAILWAY)
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
        # PyMySQL se conecta directo y sin mañas de C
        conexion = pymysql.connect(**DB_CONFIG)
        return conexion
    except Exception:
        return None

# Modelos de datos
class ChatRequest(BaseModel):
    mensaje: str

class AprendizajeRequest(BaseModel):
    nodo: str
    area: str
    descripcion: str
    respuesta: str

# =====================================================================
# MODULOS PRINCIPALES (RUTAS CORREGIDAS PARA TU INTERFAZ)
# =====================================================================

# 1. 💬 MÓDULO: CHAT
@app.post("/nucleo-chat")
def modulo_chat(datos: ChatRequest):
    entrada = datos.mensaje.strip()
    if not entrada:
        return {"respuesta": "🤖 Núcleo: En espera de tu mensaje..."}
    
    conexion = conectar_db()
    if not conexion:
        return {"respuesta": "🤖 (Modo Contingencia): Conexión con MariaDB temporalmente interrumpida."}
        
    try:
        with conexion.cursor() as cursor:
            query = "SELECT respuesta_asociada FROM enciclopedia_nodos WHERE nodo_nombre LIKE %s AND estado = 'Activo' LIMIT 1"
            cursor.execute(query, (f"%{entrada}%",))
            resultado = cursor.fetchone()
        
        if resultado:
            return {"respuesta": resultado[0]}
        else:
            return {"respuesta": f"🤖 El concepto '{entrada}' no está indexado aún. ¿Quieres guardarlo en Autoevolución?"}
    except Exception:
        return {"respuesta": "🤖 Error al procesar la consulta en el cerebro local."}
    finally:
        conexion.close()

# 2. 🗂️ MÓDULO: NÚCLEO (Enciclopedia de Nodos)
@app.get("/nucleo-consola")
def modulo_nucleo(nodo: str = None):
    conexion = conectar_db()
    if not conexion:
        raise HTTPException(status_code=500, detail="Base de datos inaccesible.")
        
    try:
        # Usamos DictCursor para que devuelva formato JSON limpio como le gusta a tu web
        with conexion.cursor(DictCursor) as cursor:
            if nodo:
                cursor.execute("SELECT * FROM enciclopedia_nodos WHERE nodo_nombre = %s", (nodo,))
                resultado = cursor.fetchone()
                return resultado if resultado else {"mensaje": "Nodo no encontrado."}
            else:
                cursor.execute("SELECT id, nodo_nombre, tipo, descripcion FROM enciclopedia_nodos ORDER BY id DESC LIMIT 10")
                return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conexion.close()

# 3. 🎬 MÓDULO: CINE
@app.get("/nucleo-cine")
def modulo_cine():
    return {
        "modulo": "Cine & Multimedia",
        "estado": "Operativo",
        "descripcion": "Espacio de almacenamiento e indexación de narrativa visual y cinematográfica."
    }

# 4. 🧠 MÓDULO: AUTO EVOLUCIÓN (Aprender)
@app.post("/nucleo-autoevolucion")
def modulo_autoevolucion(datos: AprendizajeRequest):
    conexion = conectar_db()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de enlace con el almacenamiento.")
        
    try:
        with conexion.cursor() as cursor:
            query = """
                INSERT INTO enciclopedia_nodos 
                (nodo_nombre, tipo, descripcion, respuesta_asociada, fecha_creacion, estado) 
                VALUES (%s, %s, %s, %s, %s, 'Activo')
            """
            valores = (datos.nodo.strip(), datos.area.strip(), datos.descripcion.strip(), datos.respuesta.strip(), datetime.now())
            cursor.execute(query, valores)
        return {"status": "success", "mensaje": f"🤖 Autoevolución: Nuevo conocimiento indexado con éxito bajo el área {datos.area}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la autoevolución: {e}")
    finally:
        conexion.close()

@app.get("/")
def home():
    return {"sistema": "Núcleo v2", "modulos": ["Chat", "Núcleo", "Cine", "Autoevolución"], "status": "Ready"}