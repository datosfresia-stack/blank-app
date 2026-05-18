import os
import mysql.connector
import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="IALibre Núcleo Autónomo V5.5")

# --- MOTOR DE CONEXIÓN CON RESPALDO INTEGRADO ---
def get_db_connection():
    """Intenta conectar a MariaDB en Railway; si falla, levanta un SQLite de respaldo"""
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    # Si la variable existe, intentamos el puente con MariaDB
    if DATABASE_URL:
        url = DATABASE_URL.replace("mariadb://", "mysql://").replace("mysql://", "")
        try:
            auth, rest = url.split("@")
            user, password = auth.split(":")
            host_port, database = rest.split("/")
            host, port = host_port.split(":")
            
            conn = mysql.connector.connect(
                host=host, 
                port=int(port), 
                user=user, 
                password=password, 
                database=database, 
                connect_timeout=2  # Tiempo de espera corto para evitar congelamientos
            )
            return conn, "MARIADB_PROD"
        except:
            pass # Si falla el parseo o la red, cae al bloque de abajo

    # 🛡️ RESPALDO SEGURO: Si MariaDB no responde, usamos la DB interna del contenedor
    try:
        conn_local = sqlite3.connect("base_emergencia.db")
        cursor_local = conn_local.cursor()
        # Creamos la tabla idéntica en el respaldo por si acaso
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
        return conn_local, "SQLITE_LOCAL"
    except:
        return None, "SIN_CONEXION"


# --- CONSOLA INDUSTRIAL MONOCROMÁTICA (GRIS, PLOMO Y BLANCO) ---
@app.get("/nucleo-consola", response_class=HTMLResponse)
async def ver_consola_nucleo():
    contenido_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>🛸 NÚCLEO AUTÓNOMO — Terminal</title>
        <style>
            body { 
                background-color: #000000; 
                color: #ffffff; 
                font-family: 'Courier New', Courier, monospace; 
                margin: 0; 
                padding: 15px; 
                display: flex; 
                justify-content: center; 
                align-items: center; 
                min-height: 100vh; 
            }
            .console-container { 
                width: 100%; 
                max-width: 950px; 
                background: #000000; 
                border: 2px solid #444444; 
                border-radius: 6px; 
                display: flex; 
                flex-direction: column; 
                box-shadow: 0 0 15px rgba(255,255,255,0.05); 
            }
            .tabs-bar { 
                display: flex; 
                background: #111111; 
                border-bottom: 2px solid #444444; 
            }
            .tab-btn { 
                flex: 1; 
                background: none; 
                border: none; 
                color: #888888; 
                padding: 14px; 
                cursor: pointer; 
                font-family: monospace; 
                font-weight: bold; 
                text-transform: uppercase; 
                font-size: 0.9em; 
                border-right: 1px solid #222222; 
            }
            .tab-btn:hover {
                color: #cccccc;
                background: #1a1a1a;
            }
            .tab-btn.active { 
                color: #000000; 
                background: #ffffff; 
            }
            .console-log { 
                height: 420px; 
                padding: 15px; 
                overflow-y: auto; 
                background: #000000; 
                border-bottom: 2px solid #444444; 
                font-size: 0.95em; 
                line-height: 1.5; 
            }
            .log-entry { 
                margin-bottom: 15px; 
                border-left: 3px solid #888888; 
                padding-left: 10px; 
                white-space: pre-wrap; 
            }
            .input-area { 
                padding: 15px; 
                background: #111111; 
            }
            textarea { 
                width: 100%; 
                height: 90px; 
                background: #000000; 
                color: #ffffff; 
                border: 2px solid #444444; 
                border-radius: 4px; 
                padding: 10px; 
                font-family: monospace; 
                font-size: 1em; 
                box-sizing: border-box; 
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
                padding: 14px; 
                font-size: 1em; 
                font-weight: bold; 
                font-family: monospace; 
                cursor: pointer; 
                margin-top: 8px; 
                text-transform: uppercase; 
            }
            button.send-btn:hover {
                background: #cccccc;
            }
            button.send-btn:disabled { 
                background: #222222; 
                color: #555555; 
            }
            .matrix-energy {
                font-size: 0.8em;
                color: #888888;
                margin-top: 5px;
            }
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
            <div class="log-entry" style="color: #ffffff;">🛸 [SISTEMA]: Núcleo Autónomo operacional. Interfaz monocromática gris y blanca activa. Listo para la consulta, Miguel.</div>
        </div>
        
        <div class="input-area">
            <textarea id="idea-input" placeholder="Escribe un concepto para buscar en tu base de conocimiento..."></textarea>
            <button class="send-btn" id="btn-transmitir" onclick="transmitirAlNucleo()">Consultar Nodo</button>
        </div>
    </div>

    <script>
    let canalActual = 'chat_directo';

    function cambiarCanal(nuevoCanal, elemento) {
        canalActual = nuevoCanal;
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        elemento.classList.add('active');
        document.getElementById('console-log').innerHTML += `<div class="log-entry" style="color: #888888;">[SISTEMA]: Visor conmutado al sector #${nuevoCanal.toUpperCase()}.</div>`;
    }

    async function transmitirAlNucleo() {
        const input = document.getElementById('idea-input');
        const log = document.getElementById('console-log');
        const btn = document.getElementById('btn-transmitir');
        
        const idea = input.value.trim();
        if (!idea) return;

        log.innerHTML += `<div class="log-entry" style="color: #ffffff; border-left-color: #ffffff;">📡 [Miguel]: Buscando '${idea}'...</div>`;
        input.value = '';
        log.scrollTop = log.scrollHeight;
        
        btn.disabled = true;
        btn.innerText = "ESCANEANDO MATRIZ DE DATOS...";

        try {
            const response = await fetch('/nucleo-consulta', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ idea: idea, tema: canalActual })
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                log.innerHTML += `
                    <div class="log-entry" style="color: #ffffff;">
                        🧠 [Núcleo - Inferencia Local]:\n${data.analisis_nucleo}
                        <div class="matrix-energy">↳ Capa Física: ${data.capa_datos} | Registro unificado</div>
                    </div>`;
            } else {
                log.innerHTML += `<div class="log-entry" style="color: #888888;">⚠️ [Error]: ${data.mensaje}</div>`;
            }
        } catch (error) {
            log.innerHTML += `<div class="log-entry" style="color: #888888;">⚠️ [Fallo de Enlace]: Error de red con el contenedor.</div>`;
        }

        btn.disabled = false;
        btn.innerText = "Consultar Nodo";
        log.scrollTop = log.scrollHeight;
    }
    </script>
    </body>
    </html>
    """
    return HTMLResponse(content=contenido_html, status_code=200)


# --- MOTOR DE INTELIGENCIA LOCAL (MARIADB CON CAÍDA A SQLITE) ---
@app.post("/nucleo-consulta")
async def consultar_nucleo(payload: dict):
    idea = payload.get("idea", "").strip()
    tema = payload.get("tema", "chat_directo")
    
    if not idea:
        return {"status": "error", "mensaje": "Consulta vacía."}

    # Ejecutamos el extractor con doble capa física
    db_pack = get_db_connection()
    conn = db_pack[0]
    capa_datos = db_pack[1]

    if not conn:
        return {
            "status": "success", 
            "analisis_nucleo": "❌ [ERROR TOTAL]: No se pudo levantar ninguna capa de base de datos.",
            "capa_datos": "NINGUNA"
        }

    try:
        nodo = None
        termino = f"%{idea.lower()}%"
        
        if capa_datos == "MARIADB_PROD":
            cur = conn.cursor(dictionary=True)
            query = "SELECT * FROM enciclopedia_nodos WHERE area = %s AND (concepto LIKE %s OR definicion_profunda LIKE %s) LIMIT 1"
            cur.execute(query, (tema, termino, termino))
            nodo = cur.fetchone()
            cur.close()
        else:
            # Si estamos operando bajo el SQLite de emergencia (los campos se extraen por índice)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            query = "SELECT * FROM enciclopedia_nodos WHERE area = ? AND (concepto LIKE ? OR definicion_profunda LIKE ?) LIMIT 1"
            cur.execute(query, (tema, termino, termino))
            nodo = cur.fetchone()
            cur.close()
            
        conn.close()

        # Construcción de la Inferencia de Respuesta Basada en Datos
        if nodo:
            respuesta = (
                f"📊 CONCEPTO: {nodo['concepto'].upper()}\n"
                f"🗂️ SECTOR: {nodo['area'].upper()}\n"
                f"📌 REQUISITOS PREVIOS: {nodo['requisitos_previos'] or 'Ninguno'}\n"
                f"--------------------------------------------------\n"
                f"📖 CONOCIMIENTO INDEXADO:\n{nodo['definicion_profunda']}"
            )
        else:
            # Si la cápsula está vacía, le armamos el script listo para su inyección
            respuesta = (
                f"📭 [Cápsula de Información Vacía]: No tengo registros sobre '{idea}' en #{tema.upper()}.\n\n"
                f"🛠️ CONSULTA PARA ALIMENTAR AL NÚCLEO:\n"
                f"Inserta tu información con esta estructura SQL:\n\n"
                f"INSERT INTO enciclopedia_nodos (area, concepto, definicion_profunda, requisitos_previos)\n"
                f"VALUES ('{tema}', '{idea}', 'Tu texto o código fuente largo aquí', 'Ninguno');"
            )
            
        return {
            "status": "success", 
            "analisis_nucleo": respuesta,
            "capa_datos": "MariaDB Nube" if capa_datos == "MARIADB_PROD" else "SQLite Emergencia (Local)"
        }
        
    except Exception as e:
        return {
            "status": "success", 
            "analisis_nucleo": f"⚠️ Fallo en la lectura del nodo relacional: {str(e)}",
            "capa_datos": capa_datos
        }