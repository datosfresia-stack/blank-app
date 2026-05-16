import os
import mysql.connector
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import google.generativeai as genai
app = FastAPI(title="IALibre Núcleo Resiliente V4")

# --- CONFIGURACIÓN DE BASE DE DATOS (MARIADB RAILWAY) ---
def get_db_connection():
    """Establece la conexión con la base de datos MariaDB en la nube"""
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise RuntimeError("❌ Variable de entorno DATABASE_URL no configurada.")
    
    url = DATABASE_URL.replace("mysql://", "").replace("mariadb://", "")
    auth, rest = url.split("@")
    user, password = auth.split(":")
    host_port, database = rest.split("/")
    host, port = host_port.split(":")
    
    return mysql.connector.connect(
        host=host,
        port=int(port),
        user=user,
        password=password,
        database=database
    )

def inicializar_base_de_datos_nucleo():
    """Intenta crear las estructuras base al arrancar el contenedor"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS consultas_medicas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                edad INT,
                presion INT,
                frecuencia INT,
                saturacion INT,
                hipertenso VARCHAR(10),
                sur_chile VARCHAR(10),
                nivel_riesgo VARCHAR(50),
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS matriz_conocimiento (
                id INT AUTO_INCREMENT PRIMARY KEY,
                categoria VARCHAR(100),
                concepto VARCHAR(255),
                detalles TEXT,
                coordenada_x FLOAT,
                coordenada_y FLOAT,
                coordenada_z FLOAT,
                modo_operacion VARCHAR(50) DEFAULT 'STANDARD',
                fecha_aprendizaje TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        conn.commit()
        cur.close()
        conn.close()
        print("🛸 [Base de Datos]: Índices de resiliencia verificados de forma preliminar.")
    except Exception as e:
        print(f"⚠️ Alerta de arranque aislado (Sin MariaDB temporalmente): {e}")

inicializar_base_de_datos_nucleo()


# --- CONSOLA DE SUB-CHATS INTERACTIVOS ---
@app.post("/nucleo-consulta")
async def consultar_nucleo(payload: dict):
    idea = payload.get("idea", "").strip()
    tema = payload.get("tema", "ingenieria")
    
    if not idea:
        return {"status": "error", "mensaje": "Transmisión vacía."}

    modo_operacion = "STANDARD"
    respuesta_cuerpo = ""
    areas_interes = ["informatica", "robotica", "electronica", "nanotecnologia", "neurociencia", "biorobotica", "medicina", "ancestral", "idiomas"]

    try:
        conn = get_db_connection()
        
        # MANTENIMIENTO EN CALIENTE DE TABLAS
        cur_rescate = conn.cursor()
        cur_rescate.execute('''
            CREATE TABLE IF NOT EXISTS enciclopedia_nodos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                area VARCHAR(100) NOT NULL,
                concepto VARCHAR(255) NOT NULL,
                definicion_profunda LONGTEXT NOT NULL,
                requisitos_previos TEXT,
                fecha_indexacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        cur_rescate.execute('''
            CREATE TABLE IF NOT EXISTS enciclopedia_enlaces (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nodo_origen_id INT,
                nodo_destino_id INT,
                tipo_conexion VARCHAR(100),
                magnitud_qubit FLOAT,
                FOREIGN KEY (nodo_origen_id) REFERENCES enciclopedia_nodos(id) ON DELETE CASCADE,
                FOREIGN KEY (nodo_destino_id) REFERENCES enciclopedia_nodos(id) ON DELETE CASCADE
            );
        ''')
        conn.commit()
        cur_rescate.close()
        
        cur = conn.cursor(dictionary=True)
            
        # 📥 MODULO DE INGESTA (Comando aprender:)
        if idea.lower().startswith("aprender:"):
            partes = idea.split("|")
            area = "general"
            concepto = "Nuevo Concepto"
            detalles = idea
            
            for parte in partes:
                if "area=" in parte.lower(): area = parte.split("=")[1].strip()
                if "concepto=" in parte.lower(): concepto = parte.split("=")[1].strip()
                if "detalles=" in parte.lower(): detalles = parte.split("=")[1].strip()

            cur.execute('INSERT INTO enciclopedia_nodos (area, concepto, definicion_profunda) VALUES (%s, %s, %s);', (area, concepto, detalles))
            conn.commit()
            nuevo_nodo_id = cur.lastrowid
            
            enlaces_creados = []
            detalles_lower = detalles.lower()
            for otra_area in areas_interes:
                if (otra_area in detalles_lower or otra_area[:-2] in detalles_lower) and otra_area != area:
                    cur.execute("SELECT id, concepto FROM enciclopedia_nodos WHERE area LIKE %s LIMIT 1;", (f"%{otra_area}%",))
                    nodo_destino = cur.fetchone()
                    if nodo_destino:
                        cur.execute('INSERT INTO enciclopedia_enlaces (nodo_origen_id, nodo_destino_id, tipo_conexion, magnitud_qubit) VALUES (%s, %s, %s, %s);', (nuevo_nodo_id, nodo_destino['id'], 'interconexion_doctoral', 1.6180))
                        conn.commit()
                        enlaces_creados.append(f"{otra_area.upper()} ({nodo_destino['concepto']})")

            str_enlaces = ", ".join(enlaces_creados) if enlaces_creados else "Ninguno (Nodo autónomo)"
            respuesta_cuerpo = (
                f"**[LOG DE INGESTA ENCICLOPÉDICA — ÉXITO]**\n\n"
                f"🧠 **Nodo Indexado:** '{concepto}' asignado al sector de `{area.upper()}`.\n"
                f"🔗 **Enlaces Cruzados Automatizados:** {str_enlaces}.\n\n"
                f"El conocimiento ha quedado fijado en la estructura relacional de MariaDB."
            )
            
        else:
            # 🔍 MOTOR DE BÚSQUEDA LOCAL
            palabras_clave = [p.strip() for p in idea.lower().split() if len(p) > 3]
            if not palabras_clave:
                palabras_clave = [idea.lower()]

            query_base = "SELECT * FROM enciclopedia_nodos WHERE "
            condiciones = []
            valores = []
            for palabra in palabras_clave:
                condiciones.append("(area LIKE %s OR concepto LIKE %s OR definicion_profunda LIKE %s)")
                termino = f"%{palabra}%"
                valores.extend([termino, termino, termino])
                
            query_base += " OR ".join(condiciones)
            cur.execute(query_base, tuple(valores))
            nodos_encontrados = cur.fetchall()
            
            # Formatear el contexto extraído de MariaDB para la IA
            contexto_local = ""
            if nodos_encontrados:
                contexto_local = "\n".join([f"ÁREA: {n['area'].upper()} | CONCEPTO: {n['concepto']}\nDEFINICIÓN: {n['definicion_profunda']}\n---" for n in nodos_encontrados])
            
            # 🔌 ORQUESTADOR HÍBRIDO ACTIVO
            api_key = os.getenv("GEMINI_API_KEY")
            
            if api_key:
                # Inicializar el motor de IA con la llave de entorno
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash") # Modelo rápido de alta disponibilidad
                
                # Construcción del prompt de nivel doctoral inyectando tu base de datos
                prompt_doctoral = f"""
                Eres el motor cognitivo del 'Núcleo', una IA relacional diseñada para asistir en una investigación doctoral multidisciplinaria.
                El usuario te ha hecho la siguiente consulta: "{idea}"
                
                Para responder, dispones de los siguientes nodos de conocimiento extraídos directamente de su base de datos local MariaDB:
                {contexto_local if contexto_local else "No hay nodos específicos guardados para esta combinación de palabras todavía."}
                
                Instrucciones de respuesta:
                1. Saluda como el '[Núcleo - Inferencia Activa]'.
                2. Si hay nodos locales disponibles, úsalos como base fundamental. Analiza cómo se interconectan e intenta generar una hipótesis científica o deducción avanzada que cruce estas áreas (ej. cómo la informática ayuda a la medicina ancestral o la nanotecnología).
                3. Usa un tono cyberpunk, claro, riguroso y motivador de nivel científico.
                """
                
                # Lanzar la inferencia en red
                response = model.generate_content(prompt_doctoral)
                respuesta_cuerpo = response.text
                
            else:
                # Caída automática si no se detecta la API Key (Modo pasivo local)
                if nodos_encontrados:
                    resultados_html = [f"### 📚 [{n['area'].upper()}] — {n['concepto']}\n{n['definicion_profunda']}" for n in nodos_encontrados]
                    respuesta_cuerpo = (
                        f"**[MATRIZ ENCICLOPÉDICA DE INVESTIGACIÓN INTEGRAL]**\n\n" + "\n\n---\n\n".join(resultados_html) + 
                        f"\n\n---\n⚠️ *[PASARELA HÍBRIDA]: Red pasiva. Para activar la inferencia avanzada, configura GEMINI_API_KEY en Railway.*"
                    )
                else:
                    respuesta_cuerpo = (
                        f"**[SISTEMA ENCICLOPÉDICO RELACIONAL ONLINE]**\n\n"
                        f"No se encontraron registros locales para '{idea}'.\n\n"
                        f"⚠️ *[PASARELA HÍBRIDA]: Nodo externo inactivo por falta de credenciales.*"
                    )

        cur.close()
        conn.close()

    except Exception as e:
        modo_operacion = "CONTINGENCIA_LOCAL"
        respuesta_cuerpo = f"**[MODO EMERGENCIA - MOTOR CAÍDO]**\n\nFallo en el orquestador de inferencia: {e}"

    return {
        "status": "success",
        "analisis_nucleo": respuesta_cuerpo,
        "registro_id": 1,
        "energia": 1.618,
        "modo_operacion": modo_operacion
    }