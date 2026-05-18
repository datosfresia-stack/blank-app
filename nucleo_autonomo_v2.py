import os
import mysql.connector
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="NUCLEO")

# ⚙️ CONFIGURACIÓN
CONFIGURACION_NUCLEO = {
    "nombre_sistema": "NUCLEO",
    "estado": "ACTIVO EN RAILWAY",
    "modo": "OPERATIVO",
    "conexion": "BASE DE DATOS INTEGRADA"
}

# 🔌 CONEXIÓN MARIADB
def get_db_connection():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise RuntimeError("❌ Sin conexión al almacenamiento")
    url = DATABASE_URL.replace("mysql://", "").replace("mariadb://", "")
    auth, rest = url.split("@")
    user, password = auth.split(":")
    host_port, database = rest.split("/")
    host, port = host_port.split(":")
    return mysql.connector.connect(
        host=host, port=int(port), user=user, password=password, database=database
    )

def inicializar_base_de_datos_nucleo():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS matriz_conocimiento (
            id INT AUTO_INCREMENT PRIMARY KEY,
            categoria VARCHAR(100),
            concepto VARCHAR(255),
            detalles TEXT,
            coordenada_x FLOAT DEFAULT 0,
            coordenada_y FLOAT DEFAULT 0,
            coordenada_z FLOAT DEFAULT 0,
            modo_operacion VARCHAR(50) DEFAULT 'STANDARD',
            fecha_aprendizaje TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"⚠️ {e}")

# 🧠 LÓGICA DEL NÚCLEO
def procesar_informacion(mensaje: str):
    mensaje_min = mensaje.lower()
    if "resonancia" in mensaje_min:
        return "Resonancia activada: La información se conecta e integra al conocimiento existente."
    elif "quién eres" in mensaje_min or "qué eres" in mensaje_min:
        return "Soy NUCLEO, sistema autónomo activo en Railway. Proceso y guardo información de forma segura."
    elif "aprende" in mensaje_min or "registra" in mensaje_min:
        return "Conocimiento registrado e integrado en la matriz relacional."
    elif "estado" in mensaje_min:
        return f"Estado: {CONFIGURACION_NUCLEO['estado']} | Modo: {CONFIGURACION_NUCLEO['modo']}"
    else:
        return f"✅ Procesado: {mensaje}. Dato guardado en base de datos."

# 🖥️ INTERFAZ ORIGINAL COMPLETA (DISEÑO OSCURO + PESTAÑAS)
@app.get("/", response_class=HTMLResponse)
@app.get("/nucleo-consola", response_class=HTMLResponse)
async def ver_consola_nucleo():
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🛸 NÚCLEO — Consola de Comando</title>
        <style>
            body { background: #0a0f1d; color: #00ffcc; font-family: 'Courier New', monospace; margin: 0; padding: 15px; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
            .console-container { width: 100%; max-width: 800px; background: #111a2e; border: 2px solid #00ffcc; border-radius: 8px; overflow: hidden; }
            .tabs-bar { display: flex; background: #070c16; border-bottom: 2px solid #00ffcc; }
            .tab-btn { flex:1; background:none; border:none; color:#a0a0a0; padding:12px; cursor:pointer; font-family:monospace; font-weight:bold; transition:all 0.3s; text-transform:uppercase; font-size:0.85em; }
            .tab-btn.active { color:#0a0f1d; background:#00ffcc; }
            .console-log { height:350px; padding:15px; overflow-y:auto; background:#070c16; border-bottom:1px solid #00ffcc; font-size:0.9em; line-height:1.5; }
            .log-entry { margin-bottom:12px; border-left:3px solid #00ffcc; padding-left:8px; white-space:pre-wrap; }
            .input-area { padding:15px; background:#111a2e; }
            textarea { width:100%; height:90px; background:#070c16; color:#fff; border:1px solid #00ffcc; border-radius:4px; padding:10px; font-family:monospace; font-size:0.95em; box-sizing:border-box; resize:none; }
            textarea:focus { outline:none; box-shadow:0 0 8px #00ffcc; }
            .send-btn { width:100%; background:#00ffcc; color:#0a0f1d; border:none; padding:12px; font-size:1em; font-weight:bold; font-family:monospace; cursor:pointer; border-radius:4px; margin-top:10px; transition:all 0.3s; text-transform:uppercase; }
            .send-btn:hover { background:#00b38f; box-shadow:0 0 10px #00ffcc; }
            .matrix-energy { font-size:0.8em; color:#ff007f; margin-top:4px; }
            .alert-banner { font-size:0.85em; color:#00ff88; font-weight:bold; }
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
                <div class="log-entry alert-banner">[SISTEMA]: 🛸 NÚCLEO | ACTIVO EN RAILWAY</div>
                <div class="log-entry">[ESTADO]: Conectado a base de datos. Esperando transferencia...</div>
            </div>

            <div class="input-area">
                <textarea id="idea-input" placeholder="Escribe tu petición, enseñanza o pregunta aquí..."></textarea>
                <button class="send-btn" onclick="transmitirAlNucleo()">Transmitir al Núcleo</button>
                <div class="matrix-energy" id="estado-matriz"></div>
            </div>
        </div>

        <script>
            let canalActual = 'ingenieria';
            function cambiarCanal(nuevoCanal, el) {
                canalActual = nuevoCanal;
                document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
                el.classList.add('active');
                agregarEntrada(`[SISTEMA]: Cambiado a ${nuevoCanal.toUpperCase()}.`);
            }
            function agregarEntrada(texto, usuario=false) {
                const log = document.getElementById('console-log');
                const div = document.createElement('div');
                div.className = 'log-entry';
                div.style.color = usuario ? '#00ff88' : '#fff';
                div.textContent = texto;
                log.appendChild(div);
                log.scrollTop = log.scrollHeight;
            }
            async function transmitirAlNucleo() {
                const input = document.getElementById('idea-input');
                const mensaje = input.value.trim();
                if (!mensaje) return;
                agregarEntrada(`[TÚ]: ${mensaje}`, true);
                input.value = '';
                document.getElementById('estado-matriz').textContent = "⚛️ Proces...";
                try {
                    const res = await fetch('/transmitir', {
                        method:'POST',
                        headers:{'Content-Type':'application/json'},
                        body:JSON.stringify({mensaje, canal:canalActual})
                    });
                    const data = await res.json();
                    agregarEntrada(`[NÚCLEO]: ${data.respuesta}`);
                    document.getElementById('estado-matriz').textContent = `🔋 ${data.estado}`;
                } catch(e) {
                    agregarEntrada(`[ERROR]: ${e}`);
                    document.getElementById('estado-matriz').textContent = "❌ Error";
                }
            }
        </script>
    </body>
    </html>
    """)

# 📡 ENDPOINT DE GUARDADO
class PeticionUsuario(BaseModel):
    mensaje: str
    canal: str

@app.post("/transmitir")
async def recibir_peticion(peticion: PeticionUsuario):
    respuesta_texto = procesar_informacion(peticion.mensaje)
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cat = {"ingenieria":"CODE_LAB", "peliculas":"CINE_MATRIX", "evolucion":"AUTO_EVOLUCION"}.get(peticion.canal, "GENERAL")
        cur.execute('INSERT INTO matriz_conocimiento (categoria, concepto, detalles) VALUES (%s,%s,%s)',
                    (cat, peticion.mensaje, respuesta_texto))
        conn.commit()
        cur.close()
        conn.close()
        estado = "✅ Guardado en Memoria Relacional"
    except Exception as e:
        estado = f"⚠️ Guardado fallido: {e}"
    return {"respuesta": respuesta_texto, "estado": estado}

# 🚀 ARRANQUE
if __name__ == "__main__":
    inicializar_base_de_datos_nucleo()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
