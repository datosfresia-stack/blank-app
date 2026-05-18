import os
import mysql.connector
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import google.generativeai as genai

app = FastAPI(title="IALibre Núcleo Resiliente V4.3")

# --- MEMORIA VOLÁTIL ---
HISTORIAL_NUCLEO = []

def get_db_connection():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        return None
    url = DATABASE_URL.replace("mariadb://", "mysql://").replace("mysql://", "")
    try:
        auth, rest = url.split("@")
        user, password = auth.split(":")
        host_port, database = rest.split("/")
        host, port = host_port.split(":")
        return mysql.connector.connect(
            host=host, port=int(port), user=user, password=password, database=database, connect_timeout=3
        )
    except:
        return None

# --- CONSOLA VISUAL CORREGIDA (PROCESAMIENTO SEGURO) ---
@app.get("/nucleo-consola", response_class=HTMLResponse)
async def ver_consola_nucleo():
    contenido_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>🛸 NÚCLEO — Consola</title>
        <style>
            body { background-color: #000000; color: #00ff66; font-family: monospace; margin: 0; padding: 15px; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
            .console-container { width: 100%; max-width: 900px; background: #050a05; border: 2px solid #00ff66; border-radius: 8px; display: flex; flex-direction: column; }
            .tabs-bar { display: flex; background: #000000; border-bottom: 2px solid #00ff66; }
            .tab-btn { flex: 1; background: none; border: none; color: #00aa44; padding: 12px; cursor: pointer; font-family: monospace; font-weight: bold; text-transform: uppercase; font-size: 0.9em; border-right: 1px solid rgba(0, 255, 102, 0.3); }
            .tab-btn.active { color: #000000; background: #00ff66; }
            .console-log { height: 400px; padding: 15px; overflow-y: auto; background: #000000; border-bottom: 2px solid #00ff66; font-size: 0.95em; }
            .log-entry { margin-bottom: 12px; border-left: 3px solid #00ff66; padding-left: 10px; white-space: pre-wrap; }
            .input-area { padding: 15px; background: #050a05; }
            textarea { width: 100%; height: 80px; background: #000000; color: #00ff66; border: 2px solid #00ff66; border-radius: 4px; padding: 10px; font-family: monospace; font-size: 1em; box-sizing: border-box; }
            button.send-btn { width: 100%; background: #00ff66; color: #000000; border: none; padding: 12px; font-size: 1em; font-weight: bold; font-family: monospace; cursor: pointer; margin-top: 8px; text-transform: uppercase; }
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
            <div class="log-entry" style="color: #00ff66;">[SISTEMA]: Sistema en línea. Listo para operar, Miguel.</div>
        </div>
        <div class="input-area">
            <textarea id="idea-input" placeholder="Escribe tu mensaje aquí..."></textarea>
            <button class="send-btn" id="btn-transmitir" onclick="transmitirAlNucleo()">Transmitir al Núcleo</button>
        </div>
    </div>

    <script>
    let canalActual = 'chat_directo';

    function cambiarCanal(nuevoCanal, elemento) {
        canalActual = nuevoCanal;
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        elemento.classList.add('active');
        document.getElementById('console-log').innerHTML += `<div class="log-entry" style="color: #00aa44;">[SISTEMA]: Canal #${nuevoCanal.toUpperCase()} activo.</div>`;
    }

    async function transmitirAlNucleo() {
        const input = document.getElementById('idea-input');
        const log = document.getElementById('console-log');
        const btn = document.getElementById('btn-transmitir');
        
        const idea = input.value.trim();
        if (!idea) return;

        // 1. Mostrar inmediatamente en pantalla lo que escribiste (Confirmación de JavaScript vivo)
        log.innerHTML += `<div class="log-entry" style="color: #ffaa00;">📡 [Miguel]: ${idea}</div>`;
        input.value = '';
        log.scrollTop = log.scrollHeight;
        
        // Bloquear botón temporalmente para evitar doble clic
        btn.disabled = true;
        btn.innerText = "PROCESANDO TRANSMISIÓN...";

        try {
            // Usamos ruta relativa directa, que es la más limpia y compatible en Railway
            const response = await fetch('/nucleo-consulta', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ idea: idea, tema: canalActual })
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                log.innerHTML += `<div class="log-entry" style="color: #00ff66;">🧠 [Núcleo]: ${data.analisis_nucleo}</div>`;
            } else {
                log.innerHTML += `<div class="log-entry" style="color: #ff3333;">⚠️ [Error del Servidor]: ${data.mensaje}</div>`;
            }
        } catch (error) {
            log.innerHTML += `<div class="log-entry" style="color: #ff3333;">⚠️ [Fallo de Red]: No se pudo conectar con el backend. Detalle: ${error.message}</div>`;
        }

        // Desbloquear botón
        btn.disabled = false;
        btn.innerText = "Transmitir al Núcleo";
        log.scrollTop = log.scrollHeight;
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

    contexto_local = ""
    try:
        conn = get_db_connection()
        if conn:
            cur = conn.cursor(dictionary=True)
            termino = f"%{idea.lower()}%"
            cur.execute("SELECT * FROM enciclopedia_nodos WHERE concepto LIKE %s OR definicion_profunda LIKE %s LIMIT 2", (termino, termino))
            nodos = cur.fetchall()
            if nodos:
                contexto_local = "\n".join([f"CONCEPTO: {n['concepto']}\nDEFINICION: {n['definicion_profunda']}" for n in nodos])
            cur.close()
            conn.close()
    except:
        pass

    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")
            
            instrucciones = (
                f"Eres el '[Núcleo - Inferencia Activa]'. Colaborador ciberpunk de Miguel. "
                f"Sector actual: {tema.upper()}. Responde con amplio detalle técnico."
            )
            if contexto_local:
                instrucciones += f"\nInformación local:\n{contexto_local}"

            HISTORIAL_NUCLEO.append({"role": "user", "parts": [idea]})
            if len(HISTORIAL_NUCLEO) > 40:
                HISTORIAL_NUCLEO = HISTORIAL_NUCLEO[-40:]
                
            chat = model.start_chat(history=[
                {"role": "user", "parts": [instrucciones]},
                {"role": "model", "parts": ["[Núcleo]: Conectado."]}
            ])
            chat.history.extend(HISTORIAL_NUCLEO[:-1])
            response = chat.send_message(HISTORIAL_NUCLEO[-1]["parts"][0])
            respuesta_cuerpo = response.text
            HISTORIAL_NUCLEO.append({"role": "model", "parts": [respuesta_cuerpo]})
        else:
            respuesta_cuerpo = f"⚠️ Falta la variable GEMINI_API_KEY en Railway. Mensaje recibido: {idea}"
    except Exception as e:
        respuesta_cuerpo = f"⚠️ Error en motor de Inteligencia: {str(e)}"

    return {
        "status": "success",
        "analisis_nucleo": respuesta_cuerpo
    }