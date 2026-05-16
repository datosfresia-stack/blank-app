import os
import mysql.connector
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

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
            <div class="log-entry" style="color: #8892b0;">[SISTEMA]: Enciclopedia Relacional Doctorada V4. Motor híbrido flexible offline operativo.</div>
        </div>
        <div class="input-area">
            <textarea id="idea-input" placeholder="Escribe tu petición aquí..."></textarea>
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
        log.innerHTML += `<div class="log-entry" style="color: #8892b0;">[SISTEMA]: Conmutado a canal #${canalActual.toUpperCase()}.</div>`;
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
                alertaHtml = `<div class="alert-banner">⚠️ [ALERTA]: Enlace caído. Activado motor analógico de contingencia.</div>`;
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
            log.innerHTML += `<div class="log-entry" style="color: #ff3333;">⚠️ [Fallo Crítico]: Servidor inalcanzable.</div>`;
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
    
    # Ecosistema de áreas doctorales prioritarias
    areas_interes = ["informatica", "robotica", "electronica", "nanotecnologia", "neurociencia", "biorobotica", "medicina", "ancestral", "idiomas"]

    try:
        conn = get_db_connection()
        
        # 🔧 PARCHE DE INYECCIÓN FORZADA EN CALIENTE (Garantiza que las tablas existan siempre)
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
            
        # 📥 DETECTOR DE INGESTA ENCICLOPÉDICA MULTIDISCIPLINARIA
        if idea.lower().startswith("aprender:"):
            partes = idea.split("|")
            area = "general"
            concepto = "Nuevo Concepto"
            detalles = idea
            
            for parte in partes:
                if "area=" in parte.lower(): area = parte.split("=")[1].strip()
                if "concepto=" in parte.lower(): concepto = parte.split("=")[1].strip()
                if "detalles=" in parte.lower(): detalles = parte.split("=")[1].strip()

            # 1. Insertar Nodo Principal
            cur.execute('''
                INSERT INTO enciclopedia_nodos (area, concepto, definicion_profunda)
                VALUES (%s, %s, %s);
            ''', (area, concepto, detalles))
            conn.commit()
            nuevo_nodo_id = cur.lastrowid
            
            # 2. Generar Enlaces Cruzados Inteligentes Flexibles
            enlaces_creados = []
            detalles_lower = detalles.lower()
            
            for otra_area in areas_interes:
                # Modificado: Detecta aproximaciones de áreas en el texto
                if (otra_area in detalles_lower or otra_area[:-2] in detalles_lower) and otra_area != area:
                    cur.execute("SELECT id, concepto FROM enciclopedia_nodos WHERE area LIKE %s LIMIT 1;", (f"%{otra_area}%",))
                    nodo_destino = cur.fetchone()
                    
                    if nodo_destino:
                        cur.execute('''
                            INSERT INTO enciclopedia_enlaces (nodo_origen_id, nodo_destino_id, tipo_conexion, magnitud_qubit)
                            VALUES (%s, %s, %s, %s);
                        ''', (nuevo_nodo_id, nodo_destino['id'], 'interconexion_doctoral', 1.6180))
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
            # 🔍 MODO LECTURA EVOLUCIONADO: Búsqueda Semántica Flexible por aproximación (LIKE)
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
            
            resultados_html = []
            for nodo in nodos_encontrados:
                resultados_html.append(
                    f"### 📚 [{nodo['area'].upper()}] — {nodo['concepto']}\n{nodo['definicion_profunda']}"
                )
            
            if resultados_html:
                respuesta_cuerpo = f"**[MATRIZ ENCICLOPÉDICA DE INVESTIGACIÓN INTEGRAL]**\n\n" + "\n\n---\n\n".join(resultados_html)
            else:
                respuesta_cuerpo = (
                    f"**[SISTEMA ENCICLOPÉDICO RELACIONAL ONLINE]**\n\n"
                    f"No se encontraron nodos que coincidan con '{idea}'.\n\n"
                    f"Prueba expandiendo los detalles con términos más amplios."
                )

        cur.close()
        conn.close()

    except Exception as e:
        modo_operacion = "CONTINGENCIA_LOCAL"
        respuesta_cuerpo = f"**[MODO EMERGENCIA - MOTOR CAÍDO]**\n\nFallo en el escáner flexible: {e}"

    return {
        "status": "success",
        "analisis_nucleo": respuesta_cuerpo,
        "registro_id": 1,
        "energia": 1.618,
        "modo_operacion": modo_operacion
    }