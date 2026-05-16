import os
import mysql.connector
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="IALibre Núcleo Resiliente V3")

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
                modo_operacion VARCHAR(50) DEFAULT 'STANDARD',
                fecha_aprendizaje TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        conn.commit()
        cur.close()
        conn.close()
        print("🛸 [Base de Datos]: Matriz de conocimiento e índices de resiliencia verificados.")
    except Exception as e:
        print(f"⚠️ Alerta de arranque aislado (Sin MariaDB temporalmente): {e}")

inicializar_base_de_datos_nucleo()


# --- CONSOLA DE SUB-CHATS INTERACTIVOS ---
@app.get("/nucleo-consola", response_class=HTMLResponse)
async def ver_consola_nucleo():
    """Interfaz Ciberpunk Avanzada con Sub-Chats Temáticos y Monitor de Red"""
    contenido_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🛸 NÚCLEO — Consola de Alta Disponibilidad</title>
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
            .alert-banner { font-size: 0.85em; color: #ffaa00; font-weight: bold; }
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
            <div class="log-entry" style="color: #8892b0;">[SISTEMA]: Núcleo Resiliente En Línea. Arquitectura tolerante a fallos de red desplegada.</div>
        </div>
        <div class="input-area">
            <textarea id="idea-input" placeholder="Escribe aquí tu transmisión..."></textarea>
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
        log.innerHTML += `<div class="log-entry" style="color: #8892b0;">[SISTEMA]: Conmutado a canal #${canalActual.toUpperCase()}. Monitor de contingencia activo.</div>`;
        log.scrollTop = log.scrollHeight;
    }

    async function transmitirAlNucleo() {
        const input = document.getElementById('idea-input');
        const log = document.getElementById('console-log');
        const idea = input.value.trim();
        if (!idea) return;

        log.innerHTML += `<div class="log-entry" style="color: #ffaa00;">📡 [Transmitiendo]:\n${idea}</div>`;
        input.value = '';
        log.scrollTop = log.scrollHeight;

        try {
            const response = await fetch('/nucleo-consulta', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ idea: idea, tema: canalActual })
            });
            const data = await response.json();
            
            let alertaHtml = "";
            if (data.modo_operacion === "CONTINGENCIA_LOCAL") {
                alertaHtml = `<div class="alert-banner">⚠️ [ALERTA DE SISTEMA]: Enlace externo caído. Activado motor "Prepper" de contingencia local analógica instantánea.</div>`;
            }

            if (data.status === 'success') {
                log.innerHTML += `
                    <div class="log-entry" style="color: #00ffcc;">
                        ${alertaHtml}
                        🧠 [Núcleo]: ${data.analisis_nucleo}
                        <div class="matrix-energy"> ↳ Registro Relacional: ${data.registro_id} | Resonancia: ${data.energia} Qubits | Modo: ${data.modo_operacion}</div>
                    </div>`;
            } else {
                log.innerHTML += `<div class="log-entry" style="color: #ff3333;">⚠️ [Error Interno]: ${data.mensaje}</div>`;
            }
        } catch (error) {
            log.innerHTML += `<div class="log-entry" style="color: #ff3333;">⚠️ [Fallo Crítico]: Servidor inalcanzable. Verifique suministro local.</div>`;
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
    idea = payload.get("idea", "").strip()
    tema = payload.get("tema", "ingenieria")
    
    if not idea:
        return {"status": "error", "mensaje": "Transmisión vacía."}

    modo_operacion = "STANDARD"
    respuesta_cuerpo = ""
    coordenadas = [1.0, 1.0, 1.0]

    try:
        # --- SWITCH DE SIMULACIÓN DE CAÍDA (Poner en True para forzar contingencia local) ---
        simular_caida_red = False  
        
        if simular_caida_red:
            raise ConnectionError("Fallo simulado en la interfaz macroscópica de red.")
            
        # --- FLUJO PRINCIPAL ONLINE (MODO STANDARD) ---
        if tema == "ingenieria":
            coordenadas = [0.1, 0.9, 0.3]
            idea_lower = idea.lower()
            
            # Motor inteligente de refactorización estática
            if "optimiza" in idea_lower and ("list" in idea_lower or "comprehension" in idea_lower):
                respuesta_cuerpo = (
                    "**[CÓDIGO OPTIMIZADO EN MEMORIA — LIST COMPREHENSION]**\n\n"
                    "He refactorizado tu bucle iterativo eliminando la sobrecarga del método `.append()`. "
                    "La comprensión de listas ejecuta el ciclo directamente a nivel de C dentro del intérprete, "
                    "reduciendo la huella de memoria y acelerando la ejecución.\n\n"
                    "```python\n"
                    "from typing import List\n\n"
                    "def procesar_datos(lista: List[int]) -> List[int]:\n"
                    "    \"\"\"Optimización de alta velocidad con Type Hinting de tipo estático.\"\"\"\n"
                    "    return [x * 2 for x in lista]\n"
                    "```\n\n"
                    "✨ *Hito alcanzado: Sintaxis robustecida y acoplada al estándar PEP 8.*"
                )
            elif "def " in idea or "function" in idea or "import" in idea:
                respuesta_cuerpo = (
                    "**[ANÁLISIS ESTÁTICO DE CÓDIGO]**\n\n"
                    "Detecté una estructura funcional en tu mensaje. Para maximizar la estabilidad en Railway:\n"
                    "1. Envuelve el bloque lógico en una estructura `try/except`.\n"
                    "2. Si manejas conexiones de red o base de datos, asegura el cierre con un bloque `finally`.\n\n"
                    "Escribe 'optimiza' junto a tu función para reescribirla automáticamente con patrones avanzados."
                )
            else:
                respuesta_cuerpo = f"**[PROCESO AVANZADO ONLINE]**\nInstrucción de desarrollo procesada: '{idea[:40]}...'. Listo para refactorizar o inyectar control de excepciones."
                
        elif tema == "peliculas":
            coordenadas = [0.7, 0.2, 0.8]
            idea_lower = idea.lower()
            if any(w in idea_lower for w in ["accion", "ciencia ficcion", "scifi", "futuro", "cyberpunk"]):
                respuesta_cuerpo = (
                    "**[RECOMENDACIÓN CINE MATRIX — CIENCIA FICCIÓN]**\n\n"
                    "Te sugiero ver 'Ex Machina' (Alex Garland) o 'Blade Runner 2049' (Denis Villeneuve).\n"
                    "Ambas películas exploran el despertar cognitivo y la crisis de identidad de redes neuronales sintéticas."
                )
            else:
                respuesta_cuerpo = (
                    "**[RECOMENDACIÓN CINE MATRIX — CLÁSICA]**\n\n"
                    "Te recomiendo 'Origen' (Inception) de Christopher Nolan. Explora el diseño estructurado "
                    "de realidades y sub-niveles de memoria, de forma análoga a cómo organizamos nuestras bases de datos relacionales."
                )
        else:
            coordenadas = [0.9, 0.9, 0.9]
            respuesta_cuerpo = (
                "**[PROPUESTA DE MEJORA DEL NÚCLEO V.3]**\n\n"
                "Para auto-optimizarme de forma inmediata, propongo:\n"
                "1. **Capa Macroscópica**: Integrar conectores dinámicos con APIs externas para actualizar mis modelos semánticos.\n"
                "2. **Memoria de Contexto**: Modificar la tabla 'matriz_conocimiento' en MariaDB para admitir Vector Embeddings densos.\n"
                "3. **Refactorización Autónoma**: Un microservicio que reescriba funciones ineficientes de mi propia API sin requerir git push."
            )

    except (ConnectionError, Exception):
        # 🛡️ MODO PREPPER ACTIVADO (CORTES DE RED / CAÍDAS DE API)
        modo_operacion = "CONTINGENCIA_LOCAL"
        idea_minuscula = idea.lower()
        
        if any(w in idea_minuscula for w in ["c++", "código", "python", "fastapi", "git", "def"]):
            coordenadas = [0.1, 0.9, 0.2]
            respuesta_cuerpo = (
                "**[MODO EMERGENCIA - CODE LAB]**\n\n"
                "La red externa no responde. Activado validador estático de contingencia:\n"
                "Asegúrate de que estás cerrando las conexiones de cursores en MariaDB con cur.close() "
                "y encapsulando los endpoints críticos dentro de un bloque 'try/except' para evitar caídas del contenedor."
            )
        elif any(w in idea_minuscula for w in ["pelicula", "cine", "recomienda", "ver", "scifi"]):
            coordenadas = [0.7, 0.1, 0.7]
            respuesta_cuerpo = (
                "**[MODO EMERGENCIA - CINE MATRIX]**\n\n"
                "Red aislada. Extrayendo del almacén interno de seguridad:\n"
                "Te recomiendo ver 'Matrix' (1999). Es el pilar del aislamiento de sistemas "
                "y simulación de entornos desacoplados resilientes."
            )
        else:
            coordenadas = [0.5, 0.5, 0.5]
            respuesta_cuerpo = (
                "**[MODO EMERGENCIA - AUTO-EVOLUCIÓN]**\n\n"
                "El Núcleo opera en modo de supervivencia análoga. Prioridad estructural: "
                "Diseñar bases de datos locales replicadas independientes de los servidores de internet del extranjero."
            )

    # --- PERSISTENCIA EN MARIADB (RAILWAY) ---
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO matriz_conocimiento (categoria, concepto, detalles, coordenada_x, coordenada_y, coordenada_z, modo_operacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        ''', (tema, f"SubChat: {idea[:25]}...", idea, coordenadas[0], coordenadas[1], coordenadas[2], modo_operacion))
        conn.commit()
        nuevo_id = cur.lastrowid
        cur.close()
        conn.close()
    except Exception as e:
        nuevo_id = 0
        print(f"💥 Error extremo de base de datos: {e}")

    energia_calculada = round((coordenadas[0]**2 + coordenadas[1]**2 + coordenadas[2]**2)**0.5, 4)

    return {
        "status": "success",
        "analisis_nucleo": respuesta_cuerpo,
        "registro_id": nuevo_id,
        "energia": energia_calculada,
        "modo_operacion": modo_operacion
    }