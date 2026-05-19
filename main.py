import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import google.generativeai as genai

# Inicializamos FastAPI
app = FastAPI(title="IA Núcleo")

# =====================================================================
# CONFIGURACIONES DE ENTORNO (MARIADB & GEMINI)
# =====================================================================
DB_CONFIG = {
    'host': 'nozomi.proxy.rlwy.net',
    'port': 18384,
    'user': 'root',
    'password': 'E7hZ5nq8FrmUL4iSeRP1bvel5cDkQVil',
    'database': 'railway'
}

# Configuración segura de Gemini (Evita el error de NoneType)
API_KEY_GEMINI = os.environ.get("GEMINI_API_KEY", "TU_API_KEY_POR_DEFECTO")
genai.configure(api_key=API_KEY_GEMINI)

# Inicializamos el modelo de forma limpia
try:
    modelo_ia = genai.GenerativeModel('gemini-pro')
except Exception as e:
    modelo_ia = None

# Tus 10 Áreas de Interés Maestras
AREAS_INTERES = {
    "1": "Informática", "2": "Robótica", "3": "Nanotecnología",
    "4": "Neurociencia", "5": "Medicina", "6": "Medicina Ancestral",
    "7": "Redes Cuánticas", "8": "Electrónica", "9": "Biotecnología",
    "10": "Sinergia Humano-IA"
}

# Conector nativo a la Base de Datos
def conectar_db():
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        if conexion.is_connected():
            return conexion
    except Error:
        return None

# Modelos de datos para recibir peticiones HTTP
class ConsultaRequest(BaseModel):
    entrada: str

class AprendizajeRequest(BaseModel):
    entrada: str
    seleccion_area: str
    descripcion: str
    respuesta: str

# =====================================================================
# ENDPOINTS DE LA API (PROCESAMIENTO DE NÚCLEO)
# =====================================================================

@app.get("/")
def estado_sistema():
    return {"status": "online", "sistema": "Núcleo", "ia_motor": "Conectado"}


@app.post("/consultar")
def procesar_consulta(datos: ConsultaRequest):
    """Cerebro híbrido: Busca en MariaDB; si no sabe, usa Gemini."""
    entrada_limpia = datos.entrada.strip()
    if not entrada_limpia:
        raise HTTPException(status_code=400, detail="La entrada está vacía.")

    # 1. Intentar buscar conocimiento específico en MariaDB
    conexion = conectar_db()
    respuesta_guardada = None
    
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "SELECT respuesta_asociada FROM enciclopedia_nodos WHERE nodo_nombre = %s AND estado = 'Activo'"
            cursor.execute(query, (entrada_limpia,))
            resultado = cursor.fetchone()
            if resultado:
                respuesta_guardada = resultado[0]
        except Error:
            pass
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    # Si encontramos una respuesta estructurada por ti, se entrega de inmediato
    if respuesta_guardada:
        return {"fuente": "MariaDB", "respuesta": f"🤖 Núcleo: {respuesta_guardada}"}

    # 2. Si no está mapeado en la base de datos, entra Gemini a responder como respaldo
    if modelo_ia:
        try:
            # Le damos contexto a Gemini para que sepa quién es
            prompt_contexto = f"Eres Núcleo, una IA avanzada experta en ciencias y convergencia tecnológica. Responde a esto brevemente: {entrada_limpia}"
            response = modelo_ia.generate_content(prompt_contexto)
            return {"fuente": "Gemini", "respuesta": f"🤖 Núcleo: {response.text}"}
        except Exception:
            return {"fuente": "Fallback", "respuesta": "🤖 Núcleo: Concepto en desarrollo. No tengo conexión a mi red cognitiva."}
            
    return {"fuente": "Fallback", "respuesta": "🤖 Núcleo: Concepto no indexado."}


@app.post("/aprender")
def registrar_conocimiento(datos: AprendizajeRequest):
    """Guarda discretamente una instrucción en tus áreas de interés."""
    conexion = conectar_db()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión con MariaDB.")

    tipo_nodo = AREAS_INTERES.get(datos.seleccion_area.strip(), "General")
    
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
        return {"status": "success", "mensaje": f"🤖 Núcleo: Nodo indexado en '{tipo_nodo}' con éxito."}
    except Error as e:
        conexion.rollback()
        raise HTTPException(status_code=500, detail=f"Error en base de datos: {e}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()