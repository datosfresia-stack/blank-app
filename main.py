import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Inicializamos FastAPI
app = FastAPI(title="IA Núcleo")

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

# Tus 10 Áreas de Interés Maestras para el mapeo de conocimiento
AREAS_INTERES = {
    "1": "Informática",
    "2": "Robótica",
    "3": "Nanotecnología",
    "4": "Neurociencia",
    "5": "Medicina",
    "6": "Medicina Ancestral",
    "7": "Redes Cuánticas",
    "8": "Electrónica",
    "9": "Biotecnología",
    "10": "Sinergia Humano-IA"
}

def conectar_db():
    """Conexión directa al motor MariaDB en Railway."""
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        if conexion.is_connected():
            return conexion
    except Error:
        return None

# Modelos estructurados para las peticiones de la API
class ConsultaRequest(BaseModel):
    entrada: str

class AprendizajeRequest(BaseModel):
    entrada: str
    seleccion_area: str
    descripcion: str
    respuesta: str

# =====================================================================
# ENDPOINTS DE LA API (SISTEMA DE CONSULTA Y APRENDIZAJE)
# =====================================================================

@app.get("/")
def estado_sistema():
    """Verificación rápida de que Núcleo está vivo en la web."""
    return {
        "status": "online", 
        "sistema": "Núcleo", 
        "arquitectura": "Independiente (Soberana)"
    }


@app.post("/consultar")
def procesar_consulta(datos: ConsultaRequest):
    """Consulta exclusiva en la enciclopedia indexada de MariaDB."""
    entrada_limpia = datos.entrada.strip()
    if not entrada_limpia:
        raise HTTPException(status_code=400, detail="La consulta no puede estar vacía.")

    conexion = conectar_db()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error crítico: El cerebro de MariaDB está desconectado.")

    respuesta_guardada = None
    try:
        cursor = conexion.cursor()
        query = "SELECT respuesta_asociada FROM enciclopedia_nodos WHERE nodo_nombre = %s AND estado = 'Activo'"
        cursor.execute(query, (entrada_limpia,))
        resultado = cursor.fetchone()
        if resultado:
            respuesta_guardada = resultado[0]
    except Error:
        raise HTTPException(status_code=500, detail="Error interno al leer los registros de la enciclopedia.")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

    # Si el nodo existe, entrega el conocimiento exacto que tú grabaste
    if respuesta_guardada:
        return {"encontrado": True, "respuesta": f"🤖 Núcleo: {respuesta_guardada}"}
    
    # Si no existe, avisa discretamente para activar la indexación
    return {"encontrado": False, "respuesta": "🤖 Núcleo: Concepto no registrado en la enciclopedia actual."}


@app.post("/aprender")
def registrar_conocimiento(datos: AprendizajeRequest):
    """Guarda una nueva instrucción vinculándola a tus macrotemas."""
    conexion = conectar_db()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de comunicación con el servidor de base de datos.")

    # Busca el área correspondiente (ej: si envían "6" guarda "Medicina Ancestral")
    tipo_nodo = AREAS_INTERES.get(datos.seleccion_area.strip(), "General")
    
    try:
        cursor = conexion.cursor()
        query = """
            INSERT INTO enciclopedia_nodos 
            (nodo_nombre, tipo, descripcion, respuesta_asociada, fecha_creacion, estado) 
            VALUES (%s, %s, %s, %s, %s, 'Activo')
        """
        valores = (
            datos.entrada.strip(), 
            tipo_nodo, 
            datos.descripcion.strip(), 
            datos.respuesta.strip(), 
            datetime.now()
        )
        cursor.execute(query, valores)
        conexion.commit()
        return {"status": "success", "mensaje": f"🤖 Núcleo: Conocimiento indexado en '{tipo_nodo}' de forma local."}
    except Error as e:
        conexion.rollback()
        raise HTTPException(status_code=500, detail=f"Fallo en la escritura de MariaDB: {e}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()