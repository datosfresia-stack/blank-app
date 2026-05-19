import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Inicializamos FastAPI
app = FastAPI(title="IA Núcleo API")

# =====================================================================
# CONFIGURACIÓN DE LA BASE DE DATOS MARIADB (RAILWAY)
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

# Áreas de Interés Maestras
AREAS_INTERES = {
    "1": "Informática", "2": "Robótica", "3": "Nanotecnología",
    "4": "Neurociencia", "5": "Medicina", "6": "Medicina Ancestral",
    "7": "Redes Cuánticas", "8": "Electrónica", "9": "Biotecnología",
    "10": "Sinergia Humano-IA"
}

# Modelos de datos para las peticiones web
class ConsultaNodo(BaseModel):
    entrada: str

class RegistrarNodo(BaseModel):
    entrada: str
    seleccion_area: str  # El número del 1 al 10
    descripcion: str
    respuesta: str

# =====================================================================
# RUTAS DE LA API (Endpoints para interactuar con Núcleo)
# =====================================================================

@app.get("/")
def inicio():
    return {"status": "online", "sistema": "Núcleo"}

@app.post("/consultar")
def consultar_nucleo(datos: ConsultaNodo):
    """Ruta para consultar de forma invisible si Núcleo conoce un término."""
    entrada_limpia = datos.entrada.strip()
    if not entrada_limpia:
        raise HTTPException(status_code=400, detail="La entrada no puede estar vacía.")
        
    conexion = conectar_db()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión con el cerebro de MariaDB.")
        
    respuesta = None
    try:
        cursor = conexion.cursor()
        query = "SELECT respuesta_asociada FROM enciclopedia_nodos WHERE nodo_nombre = %s AND estado = 'Activo'"
        cursor.execute(query, (entrada_limpia,))
        resultado = cursor.fetchone()
        if resultado:
            respuesta = resultado[0]
    except Error:
        raise HTTPException(status_code=500, detail="Error interno al consultar la enciclopedia.")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
            
    if respuesta:
        return {"encontrado": True, "nodo": entrada_limpia, "respuesta": f"🤖 Núcleo: {respuesta}"}
    else:
        return {"encontrado": False, "nodo": entrada_limpia, "mensaje": "🤖 Núcleo: Concepto no registrado."}

@app.post("/aprender")
def aprender_concepto(datos: RegistrarNodo):
    """Ruta privada para inyectar conocimiento en tus áreas de interés."""
    conexion = conectar_db()
    if not conexion:
        raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos.")
        
    tipo_nodo = AREAS_INTERES.get(datos.seleccion_area.strip(), "General")
    exito = False
    
    try:
        cursor = conexion.cursor()
        query = """
            INSERT INTO enciclopedia_nodos 
            (nodo_nombre, tipo, descripcion, respuesta_asociada, fecha_creacion, estado) 
            VALUES (%s, %s, %s, %s, %s, 'Activo')
        """
        valores = (datos.entrada.strip(), tipo_nodo, datos.descripcion.strip(), datos.respuesta.strip(), datetime.now())
        cursor.execute(query, valores)
        conexion.commit()
        exito = True
    except Error as e:
        conexion.rollback()
        raise HTTPException(status_code=500, detail=f"Error al escribir en MariaDB: {e}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
            
    if exito:
        return {"status": "success", "mensaje": f"🤖 Núcleo: Aprendido con éxito bajo el área '{tipo_nodo}'."}