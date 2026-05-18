import os
import mysql.connector
import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI(title="Núcleo Autónomo V7.0")

# --- MOTOR DE CONEXIÓN HERMÉTICO ---
def get_db_connection():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL:
        url = DATABASE_URL.replace("mariadb://", "mysql://").replace("mysql://", "")
        try:
            auth, rest = url.split("@")
            user, password = auth.split(":")
            host_port, database = rest.split("/")
            host, port = host_port.split(":")
            
            return mysql.connector.connect(
                host=host, port=int(port), user=user, password=password, database=database, connect_timeout=2
            ), "PROD"
        except:
            pass

    try:
        conn_local = sqlite3.connect("base_emergencia.db")
        cursor_local = conn_local.cursor()
        cursor_local.execute('''
            CREATE TABLE IF NOT EXISTS enciclopedia_nodos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                area TEXT NOT NULL,
                concepto TEXT NOT NULL,
                definicion_profunda TEXT NOT NULL,
                requisitos_previos TEXT
            )
        ''')
        conn_local.commit()
        return conn_local, "LOCAL"
    except:
        return None, "ERROR"


# --- INTERFAZ MONOCROMÁTICA ULTRA-RESPONSIVA ---
@app.get("/nucleo-consola", response_class=HTMLResponse)
async def ver_consola_nucleo():
    contenido_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🛸 NÚCLEO — Terminal</title>
        <style>
            body { 
                background-color: #000000; 
                color: #ffffff; 
                font-family: 'Courier New', Courier, monospace; 
                margin: 0; 
                padding: 10px; 
                display: flex; 
                justify-content: center; 
                align-items: center; 
                min-height: 100vh; 
                box-sizing: border-box;
            }
            .console-container { 
                width: 100%; 
                max-width: 480px; /* Tamaño ideal y compacto para celulares */
                background: #000000; 
                border: 2px solid #444444; 
                border-radius: 6px; 
                display: flex; 
                flex-direction: column; 
                box-shadow: 0 0 15px rgba(255,255,255,0.02); 
                box-sizing: border-box;
            }
            .tabs-bar { 
                display: flex; 
                background: #111111; 
                border-bottom: 2px solid #444444; 
                flex-wrap: wrap;
            }
            .tab-btn { 
                flex: 1; 
                min-width: 45%; /* Permite que se acomoden en cuadrícula limpia en pantallas chicas */
                background: none; 
                border: none; 
                color: #888888; 
                padding: 12px 6px; 
                cursor: pointer; 
                font-family: monospace; 
                font-weight: bold; 
                text-transform: uppercase; 
                font-size: 0.8em; 
                border-bottom: 1px solid #222222;
                box-sizing: border-box;
            }
            .tab-btn.active { 
                color: #000000; 
                background: #ffffff; 
                border-bottom: 1px solid #ffffff;
            }
            .console-log { 
                height: 380px; 
                padding: 12px; 
                overflow-y: auto; 
                background: #000000; 
                border-bottom: 2px solid #444444; 
                font-size: 0.9em; 
                line-height: 1.4; 
                box-sizing: border-box;
            }
            .log-entry { 
                margin-bottom: 12px; 
                border-left: 2px solid #888888; 
                padding-left: 8px; 
                white-space: pre-wrap; 
            }
            .input-area { 
                padding: 12px; 
                background: #111111; 
                box-sizing: border-box;
            }
            textarea { 
                width: 100%; 
                height: 75px; 
                background: #000000; 
                color: #ffffff; 
                border: 2px solid #444444; 
                border-radius: 4px; 
                padding: 8px; 
                font-family: monospace; 
                font-size: 0.95em; 
                box-sizing: border-box; 
                resize: none;
            }
            textarea:focus {
                outline: none;
                border-color: #888888;
            }
            button.send-btn { 
                width: 100%; 
                background: #ffffff; 
                color: #000000; 
                border: none; 
                padding: 12px; 
                font-size: 0.95em; 
                font-weight: bold; 
                font-family: monospace; 
                cursor: pointer; 
                margin-top: 6px; 
                text-transform: uppercase; 
                border-radius: 4px;
            }
            button.send-btn:disabled { 
                background: #222222; 
                color: #555555; 
            }
        </style>
    </head>
    <body>
    <div class="console-container">
        <div class="tabs-bar">
            <button class="tab-btn active" onclick="cambiarCanal('chat_directo', this)">💬 Chat</button>
            <button class="tab-btn" onclick="cambiarCanal('nucleo', this)">🧠 Núcleo</button>
            <button class="tab-btn" onclick="cambiarCanal('peliculas', this)">🎬 Cine</button>
            <button class="tab-btn" onclick="cambiarCanal('evolucion', this)">🧬 Evolución</button>
        </div>
        
        <div id="console-log" class="console-log">
            <div class="log-entry" style="color: #ffffff;">🛸 [SISTEMA]: Interfaz integrada activa. Canal: #CHAT. Preparado para la transmisión.</div>
        </div>
        
        <div class="input-area">
            <textarea id="idea-input" placeholder="Escribe aquí... Enseña usando 'aprende: frase = respuesta'"></textarea>
            <button class="send-btn" id="btn-transmitir" onclick="transmitirAlNucleo()">Enviar</button>
        </div>
    </div>

    <script>
    let canalActual = 'chat_directo';

    function cambiarCanal(nuevoCanal, elemento) {
        canalActual = nuevoCanal;
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        elemento.classList.add('active');
        document.getElementById('console-log').innerHTML += `<div class="log-entry" style="color: #888888;">[SISTEMA]: Canal cambiado a #${nuevoCanal.toUpperCase()}.</div>`;
        const log = document.getElementById('console-log');
        log.scrollTop = log.scrollHeight;
    }

    async function transmitirAlNucleo() {
        const input = document.getElementById('idea-input');
        const log = document.getElementById('console-log');
        const btn = document.getElementById('btn-transmitir');
        
        const idea = input.value.trim();
        if (!idea) return;

        log.innerHTML += `<div class="log-entry" style="color: #ffffff; border-left-color: #ffffff;">📡 Transmisión: ${idea}</div>`;
        input.value = '';
        log.scrollTop = log.scrollHeight;
        
        btn.disabled = true;

        try {
            const response = await fetch('/nucleo-consulta', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ idea: idea, tema: canalActual })
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                log.innerHTML += `<div class="log-entry" style="color: #ffffff;">🧠 [IA - Núcleo Autónoma]:\n${data.analisis_nucleo}</div>`;
            } else {
                log.innerHTML += `<div class="log-entry" style="color: #888888;">⚠️ Restableciendo canal...</div>`;
            }
        } catch (error) {
            log.innerHTML += `<div class="log-entry" style="color: #888888;">⚠️ Transmisión interrumpida.</div>`;
        }

        btn.disabled = false;
        log.scrollTop = log.scrollHeight;
    }
    </script>
    </body>
    </html>
    """
    return HTMLResponse(content=contenido_html, status_code=200)


# --- PROCESADOR DE INTELIGENCIA HERMÉTICO ---
@app.post("/nucleo-consulta")
async def consultar_nucleo(payload: dict):
    idea = payload.get("idea", "").strip()
    tema = payload.get("tema", "chat_directo")
    
    if not idea:
        return {"status": "error", "mensaje": "Datos vacíos."}

    db_pack = get_db_connection()
    conn = db_pack[0]
    capa_datos = db_pack[1]

    if not conn:
        return {"status": "success", "analisis_nucleo": "Sincronización interna pendiente."}

    try:
        # ────────────── MÓDULO DE INTEGRACIÓN DE CONOCIMIENTO (APRENDIZAJE) ──────────────
        if idea.lower().startswith("aprende:"):
            bloque_aprendizaje = idea[8:].strip()
            if "=" in bloque_aprendizaje:
                concepto, definicion = bloque_aprendizaje.split("=", 1)
                concepto = concepto.strip().lower()
                definicion = definicion.strip()
                
                cur = conn.cursor()
                if capa_datos == "PROD":
                    cur.execute("DELETE FROM enciclopedia_nodos WHERE area = %s AND concepto = %s", (tema, concepto))
                    query_ins = "INSERT INTO enciclopedia_nodos (area, concepto, definicion_profunda, requisitos_previos) VALUES (%s, %s, %s, %s)"
                    cur.execute(query_ins, (tema, concepto, definicion, "Asimilado"))
                else:
                    cur.execute("DELETE FROM enciclopedia_nodos WHERE area = ? AND concepto = ?", (tema, concepto))
                    query_ins = "INSERT INTO enciclopedia_nodos (area, concepto, definicion_profunda, requisitos_previos) VALUES (?, ?, ?, ?)"
                    cur.execute(query_ins, (tema, concepto, definicion, "Asimilado"))
                
                conn.commit()
                cur.close()
                conn.close()
                
                return {
                    "status": "success",
                    "analisis_nucleo": f"✨ [CONOCIMIENTO INTEGRADO]: He asimilado la frase para el sector #{tema.upper()}.\nResponderé con esta información cada vez que se consulte."
                }
            else:
                return {
                    "status": "success",
                    "analisis_nucleo": "Para expandir mi conocimiento usa la estructura:\naprende: frase = respuesta"
                }

        # ────────────── MÓDULO DE INFERENCIA HERMÉTICA ──────────────
        nodo = None
        termino = f"%{idea.lower()}%"
        
        if capa_datos == "PROD":
            cur = conn.cursor(dictionary=True)
            query = "SELECT * FROM enciclopedia_nodos WHERE area = %s AND (concepto = %s OR concepto LIKE %s OR definicion_profunda LIKE %s) LIMIT 1"
            cur.execute(query, (tema, idea.lower(), termino, termino))
            nodo = cur.fetchone()
            cur.close()
        else:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            query = "SELECT * FROM enciclopedia_nodos WHERE area = ? AND (concepto = ? OR concepto LIKE ? OR definicion_profunda LIKE ?) LIMIT 1"
            cur.execute(query, (tema, idea.lower(), termino, termino))
            nodo = cur.fetchone()
            cur.close()
            
        conn.close()

        if nodo:
            respuesta = f"{nodo['definicion_profunda']}"
        else:
            respuesta = (
                f"La frase '{idea}' no se encuentra registrada en el sector #{tema.upper()}.\n\n"
                f"Puedes integrarla ahora mismo escribiendo:\n"
                f"aprende: {idea} = respuesta que deseas que entregue."
            )
            
        return {"status": "success", "analisis_nucleo": respuesta}
        
    except Exception as e:
        return {"status": "success", "analisis_nucleo": "Procesando flujo de información de respaldo..."}