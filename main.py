import os
import pymysql
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from datetime import datetime
import uvicorn

app = FastAPI(
    title="IA Núcleo - Core Sólido", 
    description="Backend optimizado, seguro y protegido contra fallas de conexión."
)

# Configuración central de acceso
DB_CONFIG = {
    'host': 'nozomi.proxy.rlwy.net',
    'port': 18384,
    'user': 'root',
    'password': 'E7hZ5nq8FrmUL4iSeRP1bvel5cDkQVil',
    'database': 'railway'
}

# =====================================================================
# VALIDACIÓN DE ENTRADAS (Escudo contra textos corruptos o vacíos)
# =====================================================================
class EntradaFrase(BaseModel):
    # Validamos que la frase tenga entre 1 y 255 caracteres
    frase: str = Field(..., min_length=1, max_length=255, description="La frase o concepto a consultar/aprender")
    respuesta: str = Field(None, max_length=1000, description="La respuesta asociada (solo para modo aprendizaje)")

# Función centralizada para conectar. Si falla, el error se captura limpiamente.
def obtener_conexion():
    try:
        return pymysql.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database'],
            autocommit=True,
            connect_timeout=5  # Si en 5 segundos no conecta, aborta para no congelar la app
        )
    except pymysql.MySQLError as e:
        print(f"⚠️ Error crítico de infraestructura MariaDB: {e}")
        return None

# =====================================================================
# RUTAS DEL SISTEMA
# =====================================================================

@app.get("/")
def estado_sistema():
    return {
        "status": "Online",
        "sistema": "IA Núcleo V2",
        "seguridad": "Alta (Validación activa)",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/nucleo", status_code=status.HTTP_200_OK)
def procesar_nucleo(datos: EntradaFrase):
    frase_limpia = datos.frase.strip()
    
    conexion = obtener_conexion()
    if not conexion:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="🤖 Núcleo: Los canales de memoria (MariaDB) están temporalmente saturados. Reintenta en unos instantes."
        )

    try:
        # Usamos DictCursor para que los resultados se organicen solitos como diccionarios limpios
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            
            # 🧠 MODO APRENDIZAJE: Si viene con respuesta, guardamos el conocimiento
            if datos.respuesta:
                respuesta_limpia = datos.respuesta.strip()
                
                query_insert = """
                    INSERT INTO enciclopedia_nodos 
                    (nodo_nombre, tipo, descripcion, respuesta_asociada, fecha_creacion, estado) 
                    VALUES (%s, 'General', 'Aprendizaje Robustecido', %s, %s, 'Activo')
                """
                cursor.execute(query_insert, (frase_limpia, respuesta_limpia, datetime.now()))
                return {
                    "estatus": "success",
                    "mensaje": f"🤖 Núcleo: El concepto '{frase_limpia}' ha sido indexado correctamente en la matriz de conocimiento."
                }
            
            # 🔍 MODO CONSULTA: Si no trae respuesta, buscamos en la base de datos
            else:
                query_select = """
                    SELECT id, nodo_nombre, tipo, descripcion, respuesta_asociada, fecha_creacion, estado 
                    FROM enciclopedia_nodos 
                    WHERE nodo_nombre LIKE %s AND estado = 'Activo' 
                    LIMIT 1
                """
                cursor.execute(query_select, (f"%{frase_limpia}%",))
                nodo_encontrado = cursor.fetchone()
                
                if nodo_encontrado:
                    return {
                        "estatus": "found",
                        "datos_nodo": nodo_encontrado,
                        "respuesta": f"🤖 Núcleo: {nodo_encontrado['respuesta_asociada']}"
                    }
                
                return {
                    "estatus": "not_found",
                    "respuesta": f"🤖 Núcleo: El concepto '{frase_limpia}' no se encuentra en mis registros actuales."
                }

    except pymysql.MySQLError as error_db:
        # Si la consulta falla por sintaxis o problemas de tabla, lo atrapamos aquí sin tumbar la app
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"🤖 Núcleo: Error interno al leer la matriz de datos: {error_db}"
        )
    finally:
        conexion.close()

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=puerto, reload=False)