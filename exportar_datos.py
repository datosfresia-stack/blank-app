import mysql.connector
import pandas as pd
from datetime import datetime

# Credenciales de MariaDB (reemplaza con tus datos)
config = {
    'host': 'nozomi.proxy.rlwy.net',
    'port': 18384,
    'user': 'root',
    'password': 'E7hZ5nq8FrmUL4iSeRP1bvel5cDkQVil',
    'database': 'railway'
}

try:
    # Conectar a la base de datos
    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    
    # Obtener lista de tablas
    cursor.execute("SHOW TABLES")
    tablas = cursor.fetchall()
    
    if not tablas:
        print("No hay tablas en la base de datos.")
    else:
        # Crear archivo Excel con múltiples hojas (una por tabla)
        archivo_excel = f"datos_mariadb_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        with pd.ExcelWriter(archivo_excel, engine='openpyxl') as writer:
            for tabla in tablas:
                nombre_tabla = tabla[0]
                print(f"Exportando tabla: {nombre_tabla}...")
                
                # Leer datos de la tabla
                query = f"SELECT * FROM {nombre_tabla}"
                df = pd.read_sql(query, conexion)
                
                # Escribir en Excel
                df.to_excel(writer, sheet_name=nombre_tabla, index=False)
        
        print(f"\n✅ Datos exportados a: {archivo_excel}")
    
    cursor.close()
    conexion.close()

except mysql.connector.Error as err:
    print(f"❌ Error de conexión: {err}")
except Exception as e:
    print(f"❌ Error: {e}")