import os
import mysql.connector
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="IALibre Núcleo Autónomo V5.0")

# --- MODELO DE DATOS PARA APRENDIZAJE ---
class NuevoNodo(BaseModel):
    area: str
    concepto: str
    definicion: str
    requisitos: str = None

# --- CONEXIÓN DIRECTA A MARIADB ---
def get_db_connection():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        return None
    # Homologamos protocolos de Railway (mariadb:// -> mysql://)
    url = DATABASE_URL.replace("mariadb://", "mysql://").replace("mysql://", "")
    try:
        auth, rest = url.split("@")
        user, password = auth.split(":")
        host_port, database = rest.split("/")
        host, port = host_port.split(":")
        return mysql.connector.connect(
            host=host, port=int(port), user=user, password=password, database=database, connect_timeout=4
        )
    except:
        return None

# --- CONSOLA VISUAL MONOCROMÁTICA VERDE MATRIZ ---
@app.get("/nucleo-consola", response_class=HTMLResponse)
async def ver_consola_nucleo():
    contenido_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>🛸 NÚCLEO AUTÓNOMO — Consola DB</title>
        <style>
            body { background-color: #000000; color: #00ff66; font-family: monospace; margin: 0; padding: 15px; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
            .console-container { width: 100%; max-width: 950px; background: #050a05; border: 2px solid #00ff66; border-radius: 8px; display: flex; flex-direction: column; box-shadow: 0 0 20px rgba(0,255,102,0.3); }
            .tabs-bar { display: flex; background: #000000; border-bottom: 2px solid #00ff66; }
            .tab-btn { flex: 1; background: none; border: none; color: #00aa44; padding: 14px; cursor: pointer; font-family: monospace; font-weight: bold; text-transform: uppercase; font-size: 0.9em; border-right: 1px solid rgba(0, 255, 102, 0.3); }
            .tab-btn.active { color: #000000; background: #00ff66; }
            .console-log { height: 420px; padding: 15px; overflow-y: auto; background: #000000; border-bottom: 2px solid #00ff66; font-size: 0.95em; line-height: 1.5; }
            .log-entry { margin-bottom: 15px; border-left: 3px solid #00ff66; padding-left: 10px; white-space: pre-wrap; }
            .input-area { padding: 15px; background: #050a05; }
            textarea { width: 100%; height: 90px; background: #000000; color: #00ff66; border: 2px solid #00ff66; border-radius: 4px; padding: 10px; font-family: monospace; font-size: 1em; box-sizing: border-box; }
            button.send-btn { width: 100%; background: #00ff66; color: #000000; border: none; padding: 14px; font-size: 1em; font-weight: bold; font-family: monospace; cursor: pointer; margin-top: 8px; text-transform: uppercase; }
            button.send-btn:disabled { background: #003311; color: #00aa44; }
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
            <div class="log-entry" style="color: #00ff66;">🛸 [NÚCLEO AUTÓNOMO V5.0]: Desconectado de servidores externos. Operando puramente desde la base de datos MariaDB. Canal activo: #CHAT_DIRECTO.</div>
        </div>
        <div class="input-area">
            <textarea id="idea-input" placeholder="Escribe un concepto para buscar en la Base de Datos... Ej: python, html, matrix"></textarea>
            <button class="send-btn" id="btn-transmitir" onclick="transmitirAlNucleo()">Consultar Matriz DB</button>
        </div>
    </div>

    <script>
    let canalActual = 'chat_directo';

    function cambiarCanal(nuevoCanal, elemento) {
        canalActual = nuevoCanal;
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        elemento.classList.add('active');
        document.getElementById('console-log').innerHTML += `<div class="log-entry" style="color: #00aa44;">[SISTEMA]: Conmutando visor al sector #${nuevoCanal.toUpperCase()}.</div>`;
    }

    async function transmitirAlNucleo() {
        const input = document.getElementById('idea-input');
        const log = document.getElementById('console-log');
        const btn = document.getElementById('btn-transmitir');
        
        const idea = input.value.trim();
        if (!idea) return;

        log.innerHTML += `<div class="log-entry" style="color: #ffaa00;">📡 [Miguel]: Buscando '${idea}'...</div>`;
        input.value = '';
        log.scrollTop = log.scrollHeight;
        
        btn.disabled = true;
        btn.innerText = "EXTRAYENDO DE MARIADB...";

        try {
            const response = await fetch('/nucleo-consulta', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ idea: idea, tema: canalActual })
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                log.innerHTML += `<div class="log-entry" style="color: #00ff66;">🧠 [Núcleo - Inferencia Local]:\n${data.analisis_nucleo}</div>`;
            } else {
                log.innerHTML += `<div class="log-entry" style="color: #ff3333;">⚠️ [Error]: ${data.mensaje}</div>`;
            }
        } catch (error) {
            log.innerHTML += `<div class="log-entry" style="color: #ff3333;">⚠️ [Fallo de Enlace]: Asegúrate de que la DB en Railway esté activa.</div>`;
        }

        btn.disabled = false;
        btn.innerText = "Consultar Matriz DB";
        log.scrollTop = log.scrollHeight;
    }
    </script>
    </body>
    </html>
    """
    return HTMLResponse(content=contenido_html, status_code=200)


# --- MOTOR DE CONSULTA LOCAL Y BÚSQUEDA SEMÁNTICA ---
@app.post("/nucleo-consulta")
async def consultar_nucleo(payload: dict):
    idea = payload.get("idea", "").strip()
    tema = payload.get("tema", "chat_directo")
    
    if not idea:
        return {"status": "error", "mensaje": "Consulta vacía."}

    conn = get_db_connection()
    if not conn:
        return {
            "status": "success", 
            "analisis_nucleo": "❌ [ERROR CRÍTICO]: No hay conexión física con MariaDB. Verifica tus credenciales de Railway."
        }

    try:
        cur = conn.cursor(dictionary=True)
        # Buscamos coincidencias en el concepto o definición que pertenezcan a la pestaña actual
        query = "SELECT * FROM enciclopedia_nodos WHERE area = %s AND (concepto LIKE %s OR definicion_profunda LIKE %s) LIMIT 1"
        termino = f"%{idea.lower()}%"
        cur.execute(query, (tema, termino, termino))
        nodo = cur.fetchone()
        
        if nodo:
            # Si el concepto existe en la DB, construimos la respuesta local estructurada
            respuesta = (
                f"📊 CONCEPTO ENCONTRADO: {nodo['concepto'].upper()}\n"
                f"🗂️ SECTOR MATRIZ: {nodo['area'].upper()}\n"
                f"📌 REQUISITOS PREVIOS: {nodo['requisitos_previos'] or 'Ninguno'}\n"
                f"--------------------------------------------------\n"
                f"📖 DESARROLLO DE CONOCIMIENTO:\n{nodo['definicion_profunda']}"
            )
        else:
            # SI NO SABE LA RESPUESTA: Le enseña a Miguel cómo alimentar al Núcleo
            respuesta = (
                f"📭 [Cápsula de Información Vacía]: No tengo registros sobre '{idea}' en el sector #{tema.upper()}.\n\n"
                f"🛠️ CÓMO NUTRIR AL NÚCLEO:\n"
                f"Para enseñarme este concepto, ejecuta esta consulta directamente en tu cliente MariaDB/DBeaver:\n\n"
                f"INSERT INTO enciclopedia_nodos (area, concepto, definicion_profunda, requisitos_previos)\n"
                f"VALUES ('{tema}', '{idea}', 'Escribe aquí el código o texto largo que quieres que memorice', 'Requisitos opcionales');"
            )
            
        cur.close()
        conn.close()
        return {"status": "success", "analisis_nucleo": respuesta}
        
    except Exception as e:
        return {"status": "success", "analisis_nucleo": f"⚠️ Fallo al leer las tablas de MariaDB: {str(e)}"}