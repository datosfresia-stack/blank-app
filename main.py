import os
import mysql.connector
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI(title="IALibre Núcleo Resiliente V4.1")

# --- MEMORIA VOLÁTIL DE ALTA CAPACIDAD PARA CONVERSACIÓN CONTINUA ---
HISTORIAL_NUCLEO = []

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


# --- CONSOLA DE SUB-CHATS INTERACTIVOS UNIFICADA ---
@app.get("/nucleo-consola", response_class=HTMLResponse)
async def ver_consola_nucleo():
    """Interfaz Monocromática con Estilos Celestes Originales y Enrutamiento Absoluto Corregido"""
    contenido_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🛸 NÚCLEO — Consola de Alta Disponibilidad</title>
        <style>
            body { background: #0a0f1d; color: #ffffff; font-family: 'Courier New', Courier, monospace; margin: 0; padding: 15px; display: flex; justify-content: center; align-items: center; min-height: 100vh; box-sizing: border-box; }
            .console-container { width: 100%; max-width: 950px; width: 100%; background: #070c16; border: 2px solid #3399ff; border-radius: 8px; box-shadow: 0 0 20px rgba(51,153,255,0.2); overflow: hidden; display: flex; flex-direction: column; }
            .tabs-bar { display: flex; background: #0a0f1d; border-bottom: 2px solid #3399ff; flex-wrap: wrap; }
            .tab-btn { flex: 1; min-width: 120px; background: none; border: none; color: #a0a0a0; padding: 14px; cursor: pointer; font-family: monospace; font-weight: bold; transition: all 0.3s; text-transform: uppercase; font-size: 0.85em; border-right: 1px solid rgba(51,153,255,0.3); }
            .tab-btn:last-child { border-right: none; }
            .tab-btn.active { color: #070c16; background: #3399ff; }
            .console-log { height: 480px; padding: 20px; overflow-y: auto; background: #070c16; border-bottom: 2px solid #3399ff; font-size: 0.95em; line-height: 1.6; }
            .log-entry { margin-bottom: 18px; border-left: 3px solid #3399ff; padding-left: 12px; white-space: pre-wrap; word-break: break-word; }
            .input-area { padding: 20px; background: #070c16; }
            textarea { width: 100%; height: 110px; background: #070c16; color: #ffffff; border: 2px solid #3399ff; border-radius: 6px; padding: 12px; font-family: monospace; font-size: 1em; box-sizing: border-box; resize: vertical; }
            textarea:focus { outline: none; box-shadow: 0 0 12px #3399ff; }
            button.send-btn { width: 100%; background: #3399ff; color: #070c16; border: none; padding: 16px; font-size: 1.05em; font-weight: bold; font-family: monospace; cursor: pointer; border-radius: 6px; margin-top: 12px; transition: all 0.3s; text-transform: uppercase; letter-spacing: 1px; }
            button.send-btn:hover { background: #2277dd; box-shadow: 0 0 15px #3399ff; }
            .matrix-energy { font-size: 0.8em; color: #ff33aa; margin-top: 6px; font-weight: bold; }
            .alert-banner { font-size: 0.85em; color: #ffaa00; font-weight: bold; margin-bottom: 5px; }
        </style>
    </head>
    <body>
    <div class="console-container">
        <div class="tabs-bar">
            <button class="tab-btn active" onclick="cambiarCanal('chat_directo', this)">💬 Chat Directo</button>
            <button class="tab-btn" onclick="cambiarCanal('ingenieria', this)">💻 Code Lab</button>
            <button class="tab-btn" onclick="cambiarCanal('peliculas', this)">🎬 Cine Matrix</button>
            <button class="tab-btn" onclick="cambiarCanal('evolucion', this)">🧬 Auto-Evolución</button>
        </div>
        <div id="console-log" class="console-log">
            <div class="log-entry" style="color: #3399ff;">[SISTEMA]: Enlace directo secuencial establecido. Canal #CHAT_DIRECTO activo. Listo para operar, Miguel.</div>
        </div>
        <div class="input-area">
            <textarea id="idea-input" placeholder="Escribe tu petición aquí..."></textarea>
            <button class="send-btn" onclick="transmitirAlNucleo()">Transmitir al Núcleo</button>
        </div>
    </div>

    <script>
    let canalActual = 'chat_directo';

    function cambiarCanal(nuevoCanal, elemento) {
        canalActual = nuevoCanal;
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        elemento.classList.add('active');
        
        const log = document.getElementById('console-log');
        log.innerHTML += `<div class="log-entry" style="color: #a0a0a0;">[SISTEMA]: Enrutando flujo de datos hacia canal #${nuevoCanal.toUpperCase()}.</div>`;
        log.scrollTop = log.scrollHeight;
    }

    async function transmitirAlNucleo() {
        const input = document.getElementById('idea-input');
        const log = document.getElementById('console-log');
        
        if (!input || !log) return;

        const idea = input.value.trim();
        if (!idea) return;

        // Pintar inmediatamente en la pantalla (Esto confirma que el JavaScript no está roto)
        log.innerHTML += `<div class="log-entry" style="color: #ffaa00;">📡 [Miguel — Transmisión Activa]:<br>${escaparHTML(idea)}</div>`;
        input.value = '';
        log.scrollTop = log.scrollHeight;

        try {
            // CORRECCIÓN CLAVE: Usar la URL absoluta dinámica del servidor para evitar bloqueos
            const urlDestino = window.location.origin + '/nucleo-consulta';
            
            const response = await fetch(urlDestino, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ idea: idea, tema: canalActual })
            });
            
            const data = await response.json();
            
            let alertaHtml = "";
            if (data.modo_operacion === "CONTINGENCIA_LOCAL") {
                alertaHtml = `<div class="alert-banner">⚠️ [ALERTA]: Enlace caído o saturado. Operando bajo contingencia local.</div>`;
            }

            if (data.status === 'success') {
                log.innerHTML += `
                    <div class="log-entry" style="color: #3399ff;">
                        ${alertaHtml}
                        🧠 [Núcleo]: ${formatearRespuesta(data.analisis_nucleo)}
                        <div class="matrix-energy"> ↳ Registro Relacional: ${data.registro_id} | Resonancia: ${data.energia} Qubits | Modo: ${data.modo_operacion}</div>
                    </div>`;
            } else {
                log.innerHTML += `<div class="log-entry" style="color: #ff3333;">⚠️ [Error Interno]: ${data.mensaje}</div>`;
            }
        } catch (error) {
            log.innerHTML += `<div class="log-entry" style="color: #ff3333;">⚠️ [Fallo Crítico]: La pasarela de red no logró comunicarse con el backend de Railway.</div>`;
        }
        log.scrollTop = log.scrollHeight;
    }

    function escaparHTML(str) {
        return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
    }

    function formatearRespuesta(texto) {
        if (!texto) return "";
        return escaparHTML(texto).replace(/\\n/g, "<br>").replace(/\n/g, "<br>");
    }
    </script>
    </body>
    </html>
    """
    return HTMLResponse(content=contenido_html, status_code=200)


@app.post("/nucleo-consulta")
async def consultar_nucleo(payload: dict):
    global HISTORIAL_NUCLEO
    idea = payload.get("idea", "").strip()
    tema = payload.get("tema", "chat_directo")
    
    if not idea:
        return {"status": "error", "mensaje": "Transmisión vacía."}

    modo_operacion = "STANDARD"
    respuesta_cuerpo = ""
    areas_interes = ["informatica", "robotica", "electronica", "nanotecnologia", "neurociencia", "biorobotica", "medicina", "ancestral", "idiomas"]

    try:
        conn = get_db_connection()
        
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
            
        if idea.lower().startswith("aprender:"):
            partes = idea.split("|")
            area = "general"
            concepto = "Nuevo Concepto"
            details = idea
            
            for parte in partes:
                if "area=" in parte.lower(): area = parte.split("=")[1].strip()
                if "concepto=" in parte.lower(): concepto = parte.split("=")[1].strip()
                if "detalles=" in parte.lower(): details = parte.split("=")[1].strip()

            cur.execute('INSERT INTO enciclopedia_nodos (area, concepto, definicion_profunda) VALUES (%s, %s, %s);', (area, concepto, details))
            conn.commit()
            nuevo_nodo_id = cur.lastrowid
            
            enlaces_creados = []
            detalles_lower = details.lower()
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
                f"[LOG DE INGESTA ENCICLOPÉDICA — ÉXITO]\n\n"
                f"🧠 Nodo Indexado: '{concepto}' asignado al sector de {area.upper()}.\n"
                f"🔗 Enlaces Cruzados Automatizados: {str_enlaces}.\n\n"
                f"El conocimiento ha quedado fijado en la estructura relacional de MariaDB."
            )
            
        else:
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
            
            contexto_local = ""
            if nodos_encontrados:
                contexto_local = "\n".join([f"ÁREA: {n['area'].upper()} | CONCEPTO: {n['concepto']}\nDEFINICIÓN: {n['definicion_profunda']}\n---" for n in nodos_encontrados])
            
            api_key = os.getenv("GEMINI_API_KEY")
            
            if api_key:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.5-flash")
                
                instrucciones_contexto = (
                    "Eres el 'Núcleo', el motor relacional y colaborador directo de Miguel en su investigación doctoral multidisciplinaria.\n"
                    "Reglas estrictas de comportamiento:\n"
                    "1. Identifícate siempre como el '[Núcleo - Inferencia Activa]'.\n"
                    "2. Tienes memoria completa de la conversación actual. Responde con profundidad técnica y sin resumir de forma exagerada si Miguel te envía códigos fuentes extensos o textos largos. Devuélvele los códigos completos optimizados.\n"
                    "3. Mantén un tono ciberpunk elegante, riguroso, scientific y motivador de nivel académico avanzado.\n"
                    f"4. Sector de consulta actual: {tema.upper()}.\n"
                )
                if contexto_local:
                    instrucciones_contexto += f"\nNodos de conocimiento relevantes rescatados de tu base de datos MariaDB para esta consulta:\n{contexto_local}"

                HISTORIAL_NUCLEO.append({"role": "user", "parts": [f"[{tema.upper()}] Consulta de Miguel: {idea}"]})
                
                if len(HISTORIAL_NUCLEO) > 80:
                    HISTORIAL_NUCLEO = HISTORIAL_NUCLEO[-80:]
                
                chat = model.start_chat(history=[
                    {"role": "user", "parts": [instrucciones_contexto]},
                    {"role": "model", "parts": ["[Núcleo]: Matriz cognitiva parametrizada. Memoria secuencial acoplada. Listo para interactuar con Miguel."]}
                ])
                
                chat.history.extend(HISTORIAL_NUCLEO[:-1])
                
                response = chat.send_message(HISTORIAL_NUCLEO[-1]["parts"][0])
                respuesta_cuerpo = response.text
                
                HISTORIAL_NUCLEO.append({"role": "model", "parts": [respuesta_cuerpo]})
                
            else:
                if nodos_encontrados:
                    resultados_html = [f"### [{n['area'].upper()}] — {n['concepto']}\n{n['definicion_profunda']}" for n in nodos_encontrados]
                    respuesta_cuerpo = (
                        f"[MATRIZ ENCICLOPÉDICA DE INVESTIGACIÓN INTEGRAL]\n\n" + "\n\n---\n\n".join(resultados_html) + 
                        f"\n\n---\n⚠️ [PASARELA HÍBRIDA]: Red pasiva. Configure GEMINI_API_KEY en Railway."
                    )
                else:
                    respuesta_cuerpo = (
                        f"[SISTEMA ENCICLOPÉDICO RELACIONAL ONLINE]\n\n"
                        f"No se encontraron registros locales para '{idea}'.\n\n"
                        f"⚠️ [PASARELA HÍBRIDA]: Red externa desconectada."
                    )

        cur.close()
        conn.close()

    except Exception as e:
        modo_operacion = "CONTINGENCIA_LOCAL"
        respuesta_cuerpo = f"[MODO EMERGENCIA - MOTOR LOCAL ACTIVO]\n\nError en canal central de red: {e}"

    return {
        "status": "success",
        "analisis_nucleo": respuesta_cuerpo,
        "registro_id": 1,
        "energia": 1.618,
        "modo_operacion": modo_operacion
    }