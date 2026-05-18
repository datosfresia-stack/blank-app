import os
import mysql.connector
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import google.generativeai as genai

app = FastAPI(title="IALibre Núcleo Resiliente V4.2")

# --- MEMORIA VOLÁTIL DE ALTA CAPACIDAD ---
HISTORIAL_NUCLEO = []

# --- CONFIGURACIÓN DE BASE DE DATOS (MARIADB RAILWAY) ---
def get_db_connection():
    """Establece la conexión con la base de datos MariaDB en la nube"""
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise RuntimeError("❌ Variable de entorno DATABASE_URL no configurada.")
    
    # Normalizamos el string de conexión por si viene como mariadb://
    url = DATABASE_URL.replace("mariadb://", "mysql://")
    url = url.replace("mysql://", "")
    
    try:
        auth, rest = url.split("@")
        user, password = auth.split(":")
        host_port, database = rest.split("/")
        host, port = host_port.split(":")
        
        return mysql.connector.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database,
            connect_timeout=5
        )
    except Exception as e:
        print(f"⚠️ [Error al procesar URL de Base de Datos]: {e}")
        return None

def inicializar_base_de_datos_nucleo():
    """Crea las estructuras base de manera segura al arrancar"""
    try:
        conn = get_db_connection()
        if not conn:
            print("⚠️ [Arranque Aislado]: No se pudo conectar a MariaDB. Se reintentará en las consultas.")
            return
            
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
            CREATE TABLE IF NOT EXISTS enciclopedia_nodos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                area VARCHAR(100) NOT NULL,
                concepto VARCHAR(255) NOT NULL,
                definicion_profunda LONGTEXT NOT NULL,
                requisitos_previos TEXT,
                fecha_indexacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        conn.commit()
        cur.close()
        conn.close()
        print("🛸 [Base de Datos]: Tablas e índices verificados con éxito.")
    except Exception as e:
        print(f"⚠️ [Alerta de Arranque]: Conexión MariaDB pendiente: {e}")

inicializar_base_de_datos_nucleo()


# --- CONSOLA VISUAL MONOCROMÁTICA VERDE MATRIZ ---
@app.get("/nucleo-consola", response_class=HTMLResponse)
async def ver_consola_nucleo():
    contenido_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🛸 NÚCLEO — Consola de Alta Disponibilidad</title>
        <style>
            body { background-color: #000000; color: #00ff66; font-family: 'Courier New', Courier, monospace; margin: 0; padding: 15px; display: flex; justify-content: center; align-items: center; min-height: 100vh; box-sizing: border-box; }
            .console-container { width: 100%; max-width: 950px; background: #050a05; border: 2px solid #00ff66; border-radius: 8px; box-shadow: 0 0 25px rgba(0, 255, 102, 0.25); overflow: hidden; display: flex; flex-direction: column; }
            .tabs-bar { display: flex; background: #000000; border-bottom: 2px solid #00ff66; flex-wrap: wrap; }
            .tab-btn { flex: 1; min-width: 120px; background: none; border: none; color: #00aa44; padding: 14px; cursor: pointer; font-family: monospace; font-weight: bold; transition: all 0.3s; text-transform: uppercase; font-size: 0.9em; border-right: 1px solid rgba(0, 255, 102, 0.3); }
            .tab-btn:last-child { border-right: none; }
            .tab-btn.active { color: #000000; background: #00ff66; text-shadow: 0 0 5px rgba(0,0,0,0.5); }
            .console-log { height: 480px; padding: 20px; overflow-y: auto; background: #000000; border-bottom: 2px solid #00ff66; font-size: 0.95em; line-height: 1.6; }
            .log-entry { margin-bottom: 18px; border-left: 3px solid #00ff66; padding-left: 12px; white-space: pre-wrap; word-break: break-word; }
            .input-area { padding: 20px; background: #050a05; }
            textarea { width: 100%; height: 110px; background: #000000; color: #00ff66; border: 2px solid #00ff66; border-radius: 6px; padding: 12px; font-family: 'Courier New', monospace; font-size: 1em; box-sizing: border-box; resize: vertical; }
            textarea:focus { outline: none; box-shadow: 0 0 15px #00ff66; }
            .button-row { display: flex; gap: 10px; margin-top: 12px; }
            button.send-btn { flex: 4; background: #00ff66; color: #000000; border: none; padding: 16px; font-size: 1.05em; font-weight: bold; font-family: monospace; cursor: pointer; border-radius: 6px; transition: all 0.3s; text-transform: uppercase; letter-spacing: 1px; }
            button.send-btn:hover { background: #00cc55; box-shadow: 0 0 15px #00ff66; }
            .hint-text { color: #00aa44; font-size: 0.75em; margin-top: 4px; font-family: monospace; }
            .matrix-energy { font-size: 0.8em; color: #00ff66; opacity: 0.7; margin-top: 6px; font-weight: bold; }
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
            <div class="log-entry" style="color: #00ff66;">[SISTEMA]: Enlace directo secuencial establecido. Canal #CHAT_DIRECTO activo. Listo para operar, Miguel.</div>
        </div>
        <div class="input-area">
            <textarea id="idea-input" placeholder="Escribe tu petición aquí... (Soporta múltiples líneas)"></textarea>
            <div class="hint-text">💡 Consejo: Puedes usar Ctrl + Enter como atajo rápido para transmitir.</div>
            <div class="button-row">
                <button class="send-btn" onclick="transmitirAlNucleo()">Transmitir al Núcleo</button>
            </div>
        </div>
    </div>

    <script>
    let canalActual = 'chat_directo';

    function cambiarCanal(nuevoCanal, elemento) {
        canalActual = nuevoCanal;
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        elemento.classList.add('active');
        
        const log = document.getElementById('console-log');
        log.innerHTML += `<div class="log-entry" style="color: #00aa44;">[SISTEMA]: Enrutando flujo de datos hacia canal #${nuevoCanal.toUpperCase()}.</div>`;
        log.scrollTop = log.scrollHeight;
    }

    document.getElementById('idea-input').addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.ctrlKey) {
            e.preventDefault();
            transmitirAlNucleo();
        }
    });

    async function transmitirAlNucleo() {
        const input = document.getElementById('idea-input');
        const log = document.getElementById('console-log');
        
        if (!input || !log) return;

        const idea = input.value.trim();
        if (!idea) return;

        log.innerHTML += `<div class="log-entry" style="color: #ffaa00;">📡 [Miguel — Transmisión Activa]:<br>${escaparHTML(idea)}</div>`;
        input.value = '';
        log.scrollTop = log.scrollHeight;

        try {
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
                    <div class="log-entry" style="color: #00ff66;">
                        ${alertaHtml}
                        🧠 [Núcleo]: ${formatearRespuesta(data.analisis_nucleo)}
                        <div class="matrix-energy"> ↳ Registro Relacional: ${data.registro_id} | Resonancia: ${data.energia} Qubits | Modo: ${data.modo_operacion}</div>
                    </div>`;
            } else {
                log.innerHTML += `<div class="log-entry" style="color: #ff3333;">⚠️ [Error Interno]: ${data.mensaje}</div>`;
            }
        } catch (error) {
            log.innerHTML += `<div class="log-entry" style="color: #ff3333;">⚠️ [Fallo Crítico]: Conexión rechazada por el backend de la aplicación.</div>`;
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
    contexto_local = ""

    try:
        conn = get_db_connection()
        if conn:
            cur = conn.cursor(dictionary=True)
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
            
            if nodos_encontrados:
                contexto_local = "\n".join([f"ÁREA: {n['area'].upper()} | CONCEPTO: {n['concepto']}\nDEFINICIÓN: {n['definicion_profunda']}\n---" for n in nodos_encontrados])
            
            cur.close()
            conn.close()
    except Exception as e:
        print(f"⚠️ [Consulta local omitida temporalmente]: {e}")

    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")
            
            instrucciones_contexto = (
                "Eres el 'Núcleo', el motor relacional y colaborador directo de Miguel en su investigación doctoral multidisciplinaria.\n"
                "Reglas estrictas de comportamiento:\n"
                "1. Identifícate siempre como el '[Núcleo - Inferencia Activa]'.\n"
                "2. Tienes memoria completa de la conversación actual. Responde con profundidad técnica y devuelve códigos optimizados.\n"
                "3. Mantén un tono ciberpunk elegante, riguroso y científico.\n"
                f"4. Sector de consulta actual: {tema.upper()}.\n"
            )
            if contexto_local:
                instrucciones_contexto += f"\nNodos MariaDB:\n{contexto_local}"

            HISTORIAL_NUCLEO.append({"role": "user", "parts": [f"[{tema.upper()}] Consulta de Miguel: {idea}"]})
            if len(HISTORIAL_NUCLEO) > 80:
                HISTORIAL_NUCLEO = HISTORIAL_NUCLEO[-80:]
            
            chat = model.start_chat(history=[
                {"role": "user", "parts": [instrucciones_contexto]},
                {"role": "model", "parts": ["[Núcleo]: Matriz cognitiva parametrizada. Listo."]}
            ])
            chat.history.extend(HISTORIAL_NUCLEO[:-1])
            
            response = chat.send_message(HISTORIAL_NUCLEO[-1]["parts"][0])
            respuesta_cuerpo = response.text
            HISTORIAL_NUCLEO.append({"role": "model", "parts": [respuesta_cuerpo]})
        else:
            respuesta_cuerpo = f"⚠️ [PASARELA HÍBRIDA]: Falta la variable GEMINI_API_KEY en Railway.\nIdea: {idea}"
    except Exception as api_err:
        modo_operacion = "CONTINGENCIA_LOCAL"
        respuesta_cuerpo = f"[MODO EMERGENCIA - MOTOR ACTIVO]\n\nFallo de pasarela: {api_err}"

    return {
        "status": "success",
        "analisis_nucleo": respuesta_cuerpo,
        "registro_id": 1,
        "energia": 1.618,
        "modo_operacion": modo_operacion
    }