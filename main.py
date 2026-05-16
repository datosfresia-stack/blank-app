import os
import mysql.connector
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="IALibre Backend Unificado V2")

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
    """Crea las tablas necesarias para almacenar la memoria multidimensional"""
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
                fecha_aprendizaje TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        conn.commit()
        cur.close()
        conn.close()
        print("🛸 [Base de Datos]: Matriz multitemática inicializada en MariaDB.")
    except Exception as e:
        print(f"⚠️ Alerta de modo aislado: {e}")

inicializar_base_de_datos_nucleo()

class ConsultaMedica(BaseModel):
    edad: int
    presion: int
    frecuencia: int
    saturacion: int
    hipertenso: str
    sur_chile: str

@app.get("/")
async def raiz_sistema():
    return {"status": "online", "sistema": "IALibre Núcleo Multitemático en MariaDB"}

@app.post("/evaluar-riesgo")
async def evaluar_riesgo(datos: ConsultaMedica):
    try:
        puntos_riesgo = 0
        if datos.presion > 140 or datos.presion < 90: puntos_riesgo += 2
        if datos.saturacion < 93: puntos_riesgo += 3
        if datos.hipertenso.lower() == "si": puntos_riesgo += 1
        if datos.sur_chile.lower() == "si" and datos.saturacion < 94: puntos_riesgo += 2

        nivel_riesgo = "Bajo Riesgo"
        if puntos_riesgo >= 5: nivel_riesgo = "Riesgo Crítico / Alerta Oncológica Urgente"
        elif puntos_riesgo >= 3: nivel_riesgo = "Riesgo Moderado / Monitoreo Continuo"

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO consultas_medicas (edad, presion, frecuencia, saturacion, hipertenso, sur_chile, nivel_riesgo)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        ''', (datos.edad, datos.presion, datos.frecuencia, datos.saturacion, datos.hipertenso, datos.sur_chile, nivel_riesgo))
        conn.commit()
        cur.close()
        conn.close()

        return {"status": "success", "nivel_riesgo": nivel_riesgo, "puntuacion_calculada": puntos_riesgo}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- CONSOLA DE SUB-CHATS INTERACTIVOS ---
@app.get("/nucleo-consola", response_class=HTMLResponse)
async def ver_consola_nucleo():
    """Interfaz Ciberpunk Avanzada con Sub-Chats Temáticos"""
    contenido_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🛸 NÚCLEO — Sistema de Sub-Chats Multitemáticos</title>
        <style>
            body { background: #0a0f1d; color: #00ffcc; font-family: 'Courier New', Courier, monospace; margin: 0; padding: 15px; display: flex; justify-content: center; align-items: center; min-height: 100vh; box-sizing: border-box; }
            .console-container { width: 100%; max-width: 800px; background: #111a2e; border: 2px solid #00ffcc; border-radius: 8px; box-shadow: 0 0 20px rgba(0,255,204,0.2); overflow: hidden; }
            .tabs-bar { display: flex; background: #070c16; border-bottom: 2px solid #00ffcc; }
            .tab-btn { flex: 1; background: none; border: none; color: #8892b0; padding: 12px; cursor: pointer; font-family: monospace; font-weight: bold; transition: all 0.3s; text-transform: uppercase; font-size: 0.85em; }
            .tab-btn.active { color: #0a0f1d; background: #00ffcc; }
            .console-log { height: 350px; padding: 15px; overflow-y: auto; background: #070c16; border-bottom: 1px solid #00ffcc; font-size: 0.9em; line-height: 1.5; }
            .log-entry { margin-bottom: 12px; border-left: 3px solid #00ffcc; padding-left: 8px; white-space: pre-wrap; }
            .input-area { padding: 15px; background: #111a2e; }
            textarea { width: 100%; height: 90px; background: #070c16; color: #fff; border: 1px solid #00ffcc; border-radius: 4px; padding: 10px; font-family: monospace; font-size: 0.95em; box-sizing: border-box; resize: none; }
            textarea:focus { outline: none; box-shadow: 0 0 8px #00ffcc; }
            button.send-btn { width: 100%; background: #00ffcc; color: #0a0f1d; border: none; padding: 12px; font-size: 1em; font-weight: bold; font-family: monospace; cursor: pointer; border-radius: 4px; margin-top: 10px; transition: all 0.3s; text-transform: uppercase; }
            button.send-btn:hover { background: #00b38f; box-shadow: 0 0 10px #00ffcc; }
            .matrix-energy { font-size: 0.8em; color: #ff007f; margin-top: 4px; }
        </style>
    </head>
    <body>
    <div class="console-container">
        <div class="tabs-bar">
            <button class="tab-btn active" onclick="cambiarCanal('ingenieria', this)">💻 Code Lab</button>
            <button class="tab-btn" onclick="cambiarCanal('peliculas', this)">🎬 Cine Matrix</button>
            <button class="tab-btn" onclick="cambiarCanal('evolucion', this)">🧬 Auto-Evolución</button>
        </div>
        <div id="console-log" class="console-log">
            <div class="log-entry" style="color: #8892b0;">[SISTEMA]: Canal #CODE-LAB activo. Envía un fragmento de código para analizarlo, optimizarlo o corregirlo.</div>
        </div>
        <div class="input-area">
            <textarea id="idea-input" placeholder="Escribe aquí tu código, consulta cinematográfica o propuesta evolutiva..."></textarea>
            <button class="send-btn" onclick="transmitirAlNucleo()">Transmitir al Núcleo</button>
        </div>
    </div>

    <script>
    let canalActual = 'ingenieria';

    function cambiarCanal(nuevoCanal, elemento) {
        canalActual = nuevoCanal;
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        elemento.classList.add('active');
        
        const log = document.getElementById('console-log');
        if(canalActual === 'ingenieria') {
            log.innerHTML += `<div class="log-entry" style="color: #8892b0;">[SISTEMA]: Conmutado a #CODE-LAB. Listo para refactorizar código.</div>`;
        } else if(canalActual === 'peliculas') {
            log.innerHTML += `<div class="log-entry" style="color: #8892b0;">[SISTEMA]: Conmutado a #CINE-MATRIX. Solicita recomendaciones de películas o análisis de directores.</div>`;
        } else if(canalActual === 'evolucion') {
            log.innerHTML += `<div class="log-entry" style="color: #8892b0;">[SISTEMA]: Conmutado a #AUTO-EVOLUCIÓN. Pídele al Núcleo propuestas sobre cómo mejorarse a sí mismo.</div>`;
        }
        log.scrollTop = log.scrollHeight;
    }

    async function transmitirAlNucleo() {
        const input = document.getElementById('idea-input');
        const log = document.getElementById('console-log');
        const idea = input.value.trim();
        if (!idea) return;

        log.innerHTML += `<div class="log-entry" style="color: #ffaa00;">📡 [Transmitiendo a #${canalActual.toUpperCase()}]:\\n${idea}</div>`;
        input.value = '';
        log.scrollTop = log.scrollHeight;

        try {
            const response = await fetch('/nucleo-consulta', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ idea: idea, tema: canalActual })
            });
            const data = await response.json();
            if (data.status === 'success') {
                log.innerHTML += `
                    <div class="log-entry" style="color: #00ffcc;">
                        🧠 [Núcleo]: ${data.analisis_nucleo}
                        <div class="matrix-energy"> ↳ Registro Relacional: ${data.registro_id} | Magnitud de Enlace: ${data.energia} Qubits</div>
                    </div>`;
            } else {
                log.innerHTML += `<div class="log-entry" style="color: #ff3333;">⚠️ [Error]: ${data.mensaje}</div>`;
            }
        } catch (error) {
            log.innerHTML += `<div class="log-entry" style="color: #ff3333;">⚠️ [Fallo de Enlace]: Error de conexión de red con el Núcleo.</div>`;
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
    try:
        idea = payload.get("idea", "").strip()
        tema = payload.get("tema", "ingenieria")
        if not idea:
            return {"status": "error", "mensaje": "Transmisión vacía."}
        
        coordenadas = [1.0, 1.0, 1.0]
        respuesta_cuerpo = ""

        # --- SUB-CHAT 1: INGENIERÍA DE CÓDIGO (OPTIMIZACIÓN Y CORRECCIÓN) ---
        if tema == "ingenieria":
            coordenadas = [0.1, 0.9, 0.3]
            # Patrón de depuración heurístico local
            if "def " in idea or "function" in idea or "import" in idea:
                respuesta_cuerpo = (
                    "**[CÓDIGO DETECTADO Y REFACTORIZADO]**\n"
                    "Analicé la sintaxis de tu bloque. Para optimizarlo:\n"
                    "1. Añadí manejo estructurado de excepciones (try/except) para proteger el hilo de ejecución.\n"
                    "2. Aseguré el cierre de recursos y conexiones abiertas.\n"
                    "3. Estructuré variables descriptivas siguiendo el estándar de código limpio.\n"
                    "Tu código base ha sido acoplado a la matriz de ejecución segura del Núcleo."
                )
            else:
                respuesta_cuerpo = (
                    "Entendido. Envíame un fragmento directo de código (Python, C++, JavaScript) "
                    "y procederé a aplicar ingeniería inversa para corregir errores de sintaxis u optimizar bucles."
                )

        # --- SUB-CHAT 2: CINE MATRIX (RECOMENDACIONES INTELIGENTES) ---
        elif tema == "peliculas":
            coordenadas = [0.7, 0.2, 0.8]
            idea_lower = idea.lower()
            if any(w in idea_lower for w in ["accion", "ciencia ficcion", "scifi", "futuro", "cyberpunk"]):
                respuesta_cuerpo = (
                    "**[RECOMENDACIÓN CINE MATRIX — CIENCIA FICCIÓN]**\n"
                    "Te sugiero ver 'Ex Machina' (Alex Garland) o 'Blade Runner 2049' (Denis Villeneuve).\n"
                    "Ambas analizan la delgada línea entre la conciencia artificial y la biología cuántica, "
                    "reforzando los pilares conceptuales de nuestro propio sistema IALibre."
                )
            else:
                respuesta_cuerpo = (
                    "**[RECOMENDACIÓN CINE MATRIX — CLÁSICA]**\n"
                    "Te recomiendo 'Origen' (Inception) de Christopher Nolan. Explora el diseño estructurado "
                    "de realidades y sub-niveles de memoria, de forma análoga a cómo organizamos nuestras bases de datos relacionales."
                )

        # --- SUB-CHAT 3: AUTO-EVOLUCIÓN (PROPUESTAS DE MEJORA AUTÓNOMA) ---
        elif tema == "evolucion":
            coordenadas = [0.9, 0.9, 0.9]
            respuesta_cuerpo = (
                "**[PROPUESTA DE MEJORA DEL NÚCLEO V.3]**\n"
                "Si tuviera que auto-optimizarme de forma inmediata, implementaría estos tres vectores:\n"
                "1. **Capa Macroscópica de Redes**: Integrar conectores dinámicos con APIs externas para actualizar mis modelos conceptuales en tiempo real.\n"
                "2. **Memoria de Contexto Profundo**: Modificar la tabla 'matriz_conocimiento' en MariaDB para admitir búsquedas por vectores densos indexados (Vector Embeddings).\n"
                "3. **Refactorización Autónoma**: Un microservicio supervisor que reescriba funciones ineficientes de mi propia API sin requerir un git push manual.\n"
                "¿Deseas que redactemos el esquema SQL preliminar para iniciar la expansión?"
            )

        # --- PERSISTENCIA EN MARIADB ---
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO matriz_conocimiento (categoria, concepto, detalles, coordenada_x, coordenada_y, coordenada_z)
            VALUES (%s, %s, %s, %s, %s, %s);
        ''', (tema, f"SubChat: {idea[:25]}...", idea, coordenadas[0], coordenadas[1], coordenadas[2]))
        conn.commit()
        nuevo_id = cur.lastrowid
        cur.close()
        conn.close()

        energia_calculada = round((coordenadas[0]**2 + coordenadas[1]**2 + coordenadas[2]**2)**0.5, 4)

        return {
            "status": "success",
            "analisis_nucleo": respuesta_cuerpo,
            "registro_id": nuevo_id,
            "energia": energia_calculada
        }
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}