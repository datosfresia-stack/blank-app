import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
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
    'database': 'railway'
}

def conectar_db():
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        if conexion.is_connected():
            return conexion
    except Error:
        return None

# Modelos de datos para recibir las peticiones desde tu interfaz
class ChatRequest(BaseModel):
    mensaje: str

class AprendizajeRequest(BaseModel):
    nodo: str
    area: str
    descripcion: str
    respuesta: str

# =====================================================================
# MODULOS PRINCIPALES (RUTAS PARA TU MENÚ)
# =====================================================================

# 1. 💬 MÓDULO: CHAT
@app.post("/nucleo-chat")
def modulo_chat(datos: ChatRequest):
    """Maneja la conversación fluida del chat buscando respuestas en la base de datos."""
    entrada = datos.mensaje.strip()
    if not entrada:
        return {"respuesta": "🤖 Núcleo: En espera de tu mensaje..."}
    
    conexion = conectar_db()
    if not conexion:
        return {"respuesta": "🤖 (Modo Contingencia): Conexión con MariaDB temporalmente interrumpida."}
        
    try:
        cursor = conexion.cursor()
        # Buscamos si hay alguna respuesta directa para esta entrada en la enciclopedia
        query = "SELECT respuesta_asociada FROM enciclopedia_nodos WHERE nodo_nombre LIKE %s AND estado = 'Activo' LIMIT 1"
        cursor.execute(query, (f"%{entrada}%",))
        resultado = cursor.fetchone()
        
        if resultado:
            return {"respuesta": resultado[0]}
        else:
            return {"respuesta": f"🤖 Interesante propuesta. El concepto '{entrada}' no está indexado aún. ¿Quieres guardarlo en Autoevolución?"}
    except Error:
        return {"respuesta": "🤖 Error al procesar la consulta en el cerebro local."}
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

# 2. 🗂️ MÓDULO: NÚCLEO (Enciclopedia de Nodos)
@app.get("/nucleo-consola")
def modulo_nucleo(nodo: str = None):
    """Módulo de consulta general de la estructura de nodos."""
    conexion = conectar_db()
    if not conexion:
        raise HTTPException(status_code=500, detail="Base de datos inaccesible.")
        
    try:
        cursor = conexion.cursor(dictionary=True)
        if nodo:
            cursor.execute("SELECT * FROM enciclopedia_nodos WHERE nodo_nombre = %s", (nodo,))
            resultado = cursor.fetchone()
            return resultado if resultado else {"mensaje": "Nodo no encontrado."}
        else:
            # Si no pide uno específico, muestra los últimos nodos agregados
            cursor.execute("SELECT id, nodo_nombre, tipo, descripcion FROM enciclopedia_nodos ORDER BY id DESC LIMIT 10")
            return cursor.fetchall()
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

# 3. 🎬 MÓDULO: CINE
@app.get("/nucleo-cine")
def modulo_cine():
    """Espacio reservado para la gestión multimedia, guiones o análisis de cine."""
    # Por ahora responde un estado básico para que tu interfaz no tire 404 al hacer clic
    return {
        "modulo": "Cine & Multimedia",
        "estado": "Operativo",
        "descripcion": "Espacio de almacenamiento e indexación de narrativa visual y cinematográfica."
    }

# 4. 🧠 MÓDULO: AUTO EVOLUCIÓN (Aprender/Grabar)
@app.post("/nucleo-autoevolucion")
def modulo_autoevolucion(datos: AprendizajeRequest):
    """Permite al sistema expandir su base de datos de manera autónoma."""
    conexion = conectar_db()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de enlace con el almacenamiento.")
        
    try:
        cursor = conexion.cursor()
        query = """
            INSERT INTO enciclopedia_nodos 
            (nodo_nombre, tipo, descripcion, respuesta_asociada, fecha_creacion, estado) 
            VALUES (%s, %s, %s, %s, %s, 'Activo')
        """
        valores = (datos.nodo.strip(), datos.area.strip(), datos.descripcion.strip(), datos.respuesta.strip(), datetime.now())
        cursor.execute(query, valores)
        conexion.commit()
        return {"status": "success", "mensaje": f"🤖 Autoevolución: Nuevo conocimiento indexado con éxito bajo el área {datos.area}."}
    except Error as e:
        conexion.rollback()
        raise HTTPException(status_code=500, detail=f"Error en la autoevolución: {e}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

# Ruta raíz por cortesía del servidor
@app.get("/")
def home():
    return {"sistema": "Núcleo v2", "modulos": ["Chat", "Núcleo", "Cine", "Autoevolución"], "status": "Ready"}