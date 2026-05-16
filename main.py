import os
import mysql.connector
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="IALibre Backend Unificado")

# --- CONFIGURACIÓN DE BASE DE DATOS (MARIADB RAILWAY) ---
def get_db_connection():
    """Establece la conexión con la base de datos MariaDB/MySQL en la nube"""
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise RuntimeError("❌ Variable de entorno DATABASE_URL no configurada.")
    
    # Adaptación heurística para parsear la URL estándar de MariaDB
    # Estructura esperada: mysql://user:password@host:port/database
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
    """Crea las tablas necesarias para almacenar la memoria en MariaDB si no existen"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 1. Tabla para las consultas médicas del Sur de Chile
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
        
        # 2. Cerebro relacional para códigos, neurociencia y metas doctorales
        cur.execute('''
            CREATE TABLE IF NOT EXISTS matriz_conocimiento (
                id INT AUTO_INCREMENT PRIMARY KEY,
                categoria VARCHAR(100),
                concepto VARCHAR(255),
                detalles TEXT,
                coordenada_x FLOAT,
                coordenada_y FLOAT,
                coordenada_z FLOAT,
                fecha_aprendizaje TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        conn.commit()
        cur.close()
        conn.close()
        print("🛸 [Base de Datos]: Matriz de conocimiento eterno verificada e inicializada en MariaDB.")
    except Exception as e:
        print(f"⚠️ No se pudo inicializar el almacenamiento del Núcleo: {e}")

# Ejecutamos la inicialización al arrancar el contenedor en Railway
inicializar_base_de_datos_nucleo()


# --- MODELOS DE DATOS (PYDANTIC) ---
class ConsultaMedica(BaseModel):
    edad: int
    presion: int
    frecuencia: int
    saturacion: int
    hipertenso: str
    sur_chile: str


# --- ENDPOINTS LÓGICA SANITARIA (SUR DE CHILE) ---
@app.get("/")
async def raiz_sistema():
    return {"status": "online", "sistema": "IALibre Frontend/Backend unificado operando en MariaDB"}

@app.post("/evaluar-riesgo")
async def evaluar_riesgo(datos: ConsultaMedica):
    try:
        puntos_riesgo = 0
        
        if datos.presion > 140 or datos.presion < 90:
            puntos_riesgo += 2
        if datos.saturacion < 93:
            puntos_riesgo += 3
        if datos.hipertenso.lower() == "si":
            puntos_riesgo += 1
            
        # Ponderación geográfica: Factor de aislamiento en el Sur de Chile
        if datos.sur_chile.lower() == "si" and datos.saturacion < 94:
            puntos_riesgo += 2

        nivel_riesgo = "Bajo Riesgo"
        if puntos_riesgo >= 5:
            nivel_riesgo = "Riesgo Crítico / Alerta Oncológica Urgente"
        elif puntos_riesgo >= 3:
            nivel_riesgo = "Riesgo Moderado / Monitoreo Continuo"

        # Guardar registro en MariaDB utilizando marcadores estandar de formato (%s)
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO consultas_medicas (edad, presion, frecuencia, saturacion, hipertenso, sur_chile, nivel_riesgo)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        ''', (datos.edad, datos.presion, datos.frecuencia, datos.saturacion, datos.hipertenso, datos.sur_chile, nivel_riesgo))
        conn.commit()
        cur.close()
        conn.close()

        return {
            "status": "success",
            "nivel_riesgo": nivel_riesgo,
            "puntuacion_calculada": puntos_riesgo,
            "contexto_geografico": "Evaluación adaptada para la Región de Los Lagos"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno en análisis clínico: {str(e)}")


# --- ENDPOINTS CONSOLA INTERACTIVA DEL NÚCLEO ---
@app.get("/nucleo-consola", response_class=HTMLResponse)
async def ver_consola_nucleo():
    """Interfaz visual ciberpunk integrada para el control universal autónomo"""
    contenido_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🛸 NÚCLEO — Consola de Comando Universal</title>
        <style>
            body { background: #0a0f1d; color: #00ffcc; font-family: 'Courier New', Courier, monospace; margin: 0; padding: 15px; display: flex; justify-content: center; align-items: center; min-height: 100vh; box-sizing: border-box; }
            .console-container { width: 100%; max-width: 700px; background: #111a2e; border: 2px solid #00ffcc; border-radius: 8px; box-shadow: 0 0 20px rgba(0,255,204,0.2); overflow: hidden; }
            .console-header { background: #00ffcc; color: #0a0f1d; padding: 12px; font-weight: bold; text-align: center; font-size: 1.1em; letter-spacing: 2px; }
            .console-log { height: 300px; padding: 15px; overflow-y: auto; background: #070c16; border-bottom: 1px solid #00ffcc; font-size: 0.9em; line-height: 1.5; }
            .log-entry { margin-bottom: 10px; border-left: 3px solid #00ffcc; padding-left: 8px; }
            .system-msg { color: #8892b0; }
            .success-msg { color: #00ffcc; }
            .input-area { padding: 15px; background: #111a2e; }
            textarea { width: 100%; height: 80px; background: #070c16; color: #fff; border: 1px solid #00ffcc; border-radius: 4px; padding: 10px; font-family: monospace; font-size: 1em; box-sizing: border-box; resize: none; }
            textarea:focus { outline: none; box-shadow: 0 0 8px #00ffcc; }
            button { width: 100%; background: #00ffcc; color: #0a0f1d; border: none; padding: 12px; font-size: 1em; font-weight: bold; font-family: monospace; cursor: pointer; border-radius: 4px; margin-top: 10px; transition: all 0.3s; text-transform: uppercase; }
            button:hover { background: #00b38f; box-shadow: 0 0 10px #00ffcc; }
            .matrix-energy { font-size: 0.8em; color: #ff007f; margin-top: 5px; }
        </style>
    </head>
    <body>
    <div class="console-container">
        <div class="console-header">🛸 NÚCLEO AUTÓNOMO INTERFAZ V.1</div>
        <div id="console-log" class="console-log">
            <div class="log-entry system-msg">[SISTEMA]: Núcleo en línea. Matriz cuántica clásica inicializada.</div>
            <div class="log-entry system-msg">[SISTEMA]: Esperando transferencia de conocimiento doctoral...</div>
        </div>
        <div class="input-area">
            <textarea id="idea-input" placeholder="Escriba un nuevo avance, idea o consulta de investigación..."></textarea>
            <button onclick="transmitirAlNucleo()">Transmitir Conocimiento</button>
        </div>
    </div>
    <script>
    async function transmitirAlNucleo() {
        const input = document.getElementById('idea-input');
        const log = document.getElementById('console-log');
        const idea = input.value.trim();
        if (!idea) return;

        log.innerHTML += `<div class="log-entry" style="color: #ffaa00;">📡 [Transmitiendo]: ${idea}</div>`;
        input.value = '';
        log.scrollTop = log.scrollHeight;

        try {
            const response = await fetch('/nucleo-consulta', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ idea: idea })
            });
            const data = await response.json();
            if (data.status === 'success') {
                let resonanciaHtml = '';
                data.resonancias_encontradas.forEach(r => {
                    resonanciaHtml += `<div class="matrix-energy"> ↳ Resonancia con "${r.concepto_relacionado}": ${r.energia_qubit} Qubits</div>`;
                });
                log.innerHTML += `
                    <div class="log-entry success-msg">
                        🧠 [Núcleo]: ${data.analisis_nucleo}<br>
                        ${resonanciaHtml}
                    </div>`;
            } else {
                log.innerHTML += `<div class="log-entry" style="color: #ff3333;">⚠️ [Error]: ${data.mensaje}</div>`;
            }
        } catch (error) {
            log.innerHTML += `<div class="log-entry" style="color: #ff3333;">⚠️ [Fallo de Enlace]: Incapaz de conectar con el hardware del Núcleo.</div>`;
        }
        log.scrollTop = log.scrollHeight;
    }
    </script>
    </body>
    </html>
    """
    return HTMLResponse(content=contenido_html, status_code=200)

@app.post("/nucleo-consulta")
async def consultar_nucleo(payload: dict):
    """
    Endpoint del Núcleo: Clasifica, analiza y almacena notas doctorales 
    e ingeniería en la base de datos MariaDB de forma permanente.
    """
    try:
        idea = payload.get("idea", "").strip()
        if not idea:
            return {"status": "error", "mensaje": "La transmisión está vacía."}
        
        print(f"🛸 [Procesando Conocimiento]: '{idea}'")
        
        # --- MOTOR HEURÍSTICO LOCAL: Clasificación por Palabras Clave ---
        idea_minuscula = idea.lower()
        categoria = "ingenieria"
        coordenadas = [1.0, 1.0, 1.0]
        
        if any(w in idea_minuscula for w in ["c++", "código", "python", "fastapi", "git", "backend", "servidor"]):
            categoria = "codigo"
            coordenadas = [0.1, 0.9, 0.2]
        elif any(w in idea_minuscula for w in ["neuro", "cerebro", "neuronal", "mente", "biologica"]):
            categoria = "neurociencia"
            coordenadas = [0.9, 0.1, 0.4]
        elif any(w in idea_minuscula for w in ["nano", "carbono", "molecula", "atomo", "qubit"]):
            categoria = "nanotecnologia"
            coordenadas = [0.3, 0.4, 0.9]
        elif any(w in idea_minuscula for w in ["medicina", "salud", "presion", "riesgo", "paciente", "oncologico"]):
            categoria = "medicina"
            coordenadas = [0.8, 0.7, 0.1]

        # --- PERSISTENCIA EN MARIADB (Memoria Eterna) ---
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO matriz_conocimiento (categoria, concepto, detalles, coordenada_x, coordenada_y, coordenada_z)
            VALUES (%s, %s, %s, %s, %s, %s);
        ''', (categoria, f"Nota Doc: {idea[:30]}...", idea, coordenadas[0], coordenadas[1], coordenadas[2]))
        
        conn.commit()
        nuevo_id = cur.lastrowid  # Captura el ID auto-incremental nativo en MariaDB
        cur.close()
        conn.close()

        # --- RESPUESTA DE EXPANSIÓN COGNITIVA AUTÓNOMA ---
        guias_autonomas = {
            "codigo": "Lógica registrada. Recuerda: En FastAPI, el control de errores (try/except) y el manejo asíncrono evitan la caída del contenedor en Railway.",
            "neurociencia": "Análisis bio-conceptual sellado. Las redes neuronales artificiales emulan la suma ponderada de las dendritas biológicas. Siguiente hito: funciones de activación no lineales.",
            "nanotecnologia": "Dimensión molecular capturada. Las estructuras de carbono permiten la miniaturización de sensores biomédicos de alta conductividad.",
            "medicina": "Variables sanitarias acopladas. Recuerda correlacionar la saturación de oxígeno con los factores de aislamiento climático del Sur de Chile.",
            "ingenieria": "Meta de ingeniería procesada. Continúa estructurando tus diagramas de flujo antes de compilar."
        }

        return {
            "status": "success",
            "analisis_nucleo": f"[REGISTRO ETERNO N° {nuevo_id} - CAT: {categoria.upper()}]: {guias_autonomas[categoria]}",
            "resonancias_encontradas": [
                {"concepto_relacionado": f"Matriz Cuántica ({categoria.upper()})", "energia_qubit": round((coordenadas[0]**2 + coordinates_y := coordenadas[1]**2 + coordenadas[2]**2)**0.5, 4)}
            ]
        }
        
    except Exception as e:
        print(f"💥 Error crítico en almacenamiento: {str(e)}")
        return {"status": "error", "mensaje": f"Fallo en enlace relacional: {str(e)}"}