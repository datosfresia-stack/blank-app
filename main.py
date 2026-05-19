import os
import mysql.connector
from mysql.connector import Error
from datetime import datetime

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
    """Establece conexión con MariaDB en Railway."""
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        if conexion.is_connected():
            return conexion
    except Error:
        return None

# =====================================================================
# ÁREAS DE INTERÉS MAESTRAS
# =====================================================================
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

# =====================================================================
# PROCESAMIENTO DE CONOCIMIENTO
# =====================================================================

def buscar_respuesta_en_nucleo(nodo_nombre):
    """Busca en la base de datos si el concepto ya existe."""
    conexion = conectar_db()
    if not conexion:
        return None
    
    respuesta = None
    try:
        cursor = conexion.cursor()
        query = "SELECT respuesta_asociada FROM enciclopedia_nodos WHERE nodo_nombre = %s AND estado = 'Activo'"
        cursor.execute(query, (nodo_nombre,))
        resultado = cursor.fetchone()
        
        if resultado:
            respuesta = resultado[0]
            
    except Error:
        pass
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
    return respuesta


def ensenar_a_nucleo(nodo_nombre, tipo, descripcion, respuesta_asociada):
    """Guarda discretamente la nueva información en MariaDB."""
    conexion = conectar_db()
    if not conexion:
        return False
    
    exito = False
    try:
        cursor = conexion.cursor()
        query = """
            INSERT INTO enciclopedia_nodos 
            (nodo_nombre, tipo, descripcion, respuesta_asociada, fecha_creacion, estado) 
            VALUES (%s, %s, %s, %s, %s, 'Activo')
        """
        valores = (nodo_nombre, tipo, descripcion, respuesta_asociada, datetime.now())
        
        cursor.execute(query, valores)
        conexion.commit()
        exito = True
        
    except Error:
        conexion.rollback()
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
    return exito

# =====================================================================
# FLUJO DE INTERACCIÓN PRINCIPAL
# =====================================================================

def ejecutar_nucleo():
    print("=========================================")
    print("🤖 NÚCLEO EN LINEA")
    print("=========================================")
    
    while True:
        entrada = input("\nTú: ").strip()
        
        if entrada.lower() in ['salir', 'exit', 'quit']:
            print("🤖 Núcleo: Finalizando conexión de memoria.")
            break
            
        if not entrada:
            continue
            
        # Intentar consultar en base de datos
        respuesta_guardada = buscar_respuesta_en_nucleo(entrada)
        
        if respuesta_guardada:
            print(f"🤖 Núcleo: {respuesta_guardada}")
        else:
            # Flujo interno de configuración interactiva (Solo para administradores)
            print("🤖 Núcleo: Concepto no registrado en la enciclopedia actual.")
            confirmar = input("¿Deseas indexar esta entrada? (s/n): ").strip().lower()
            
            if confirmar == 's':
                print("\n--- Clasificación en Áreas de Interés ---")
                for clave, area in AREAS_INTERES.items():
                    print(f" [{clave}] {area}")
                
                seleccion = input("Selecciona el área numérica: ").strip()
                tipo_nodo = AREAS_INTERES.get(seleccion, "General")
                
                descripcion = input("Escribe la descripción de este nodo: ").strip()
                respuesta = input("Escribe la respuesta que debo entregar: ").strip()
                
                if ensenar_a_nucleo(entrada, tipo_nodo, descripcion, respuesta):
                    print("🤖 Núcleo: Registro completado con éxito en MariaDB.")
                else:
                    print("❌ Error técnico: No se pudo escribir en el servidor de Railway.")
            else:
                print("🤖 Núcleo: Entrada omitida.")

if __name__ == "__main__":
    ejecutar_nucleo()