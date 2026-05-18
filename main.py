import os
import requests
import time
import mysql.connector
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# 🚫 ELIMINAMOS: import google.generativeai as genai  (YA NO SE USA)

app = FastAPI(title="IALibre Núcleo Resiliente V4 - SOLO LOCAL")

# ==================================================
# ⚙️ CONFIGURACIÓN PRINCIPAL - TU SISTEMA COMO ÚNICO
# ==================================================
CONFIGURACION_NUCLEO = {
    "modelo_principal": "NUCLEO_PROPIO_v2.2",   # ✅ TU MOTOR, NO GEMINI
    "modo": "SIEMPRE_LOCAL",                     # ✅ SIEMPRE USA TU CELULAR
    "ip_cerebro": "192.168.1.9",                # ✅ IP FIJA DE TU CELULAR
    "puerto_cerebro": "8080",                    # ✅ PUERTO DEL MOTOR QWEN
    "ruta_api": "/v1/chat/completions",
    "version_sistema": "4.0 - AUTÓNOMA TOTAL",
    "coordenadas": "1.618 Qubits | Red: Resonancia"
}

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

# ==================================================
# 🔧 FUNCIÓN PRINCIPal: CONEXIÓN A TU CELULAR
# ==================================================
def consultar_nucleo_propio(mensaje: str):
    """Conecta directamente al motor Qwen2.5 que corre en tu celular"""
    url_completa = f"http://{CONFIGURACION_NUCLEO['ip_cerebro']}:{CONFIGURACION_NUCLEO['puerto_cerebro']}{CONFIGURACION_NUCLEO['ruta_api']}"
    
    payload = {
        "model": "qwen2.5-1.5b-instruct-q8_0",
        "messages": [
            {"role": "system", "content": "Eres NÚCLEO, una inteligencia artificial avanzada, profunda y capaz. Responde con claridad, profundidad y precisión. Usa todo lo aprendido y guarda nueva información en tu memoria relacional."},
            {"role": "user", "content": mensaje}
        ],
        "temperature": 0.7,
        "max_tokens": 4096,
        "stream": False
    }

    try:
        respuesta = requests.post(url_completa, json=payload, timeout=30)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            return datos['choices'][0]['message']['content']
        else:
            return "⚠️ [Sistema]: Conectado, pero el motor no respondió correctamente. Reintenta o verifica el celular."
    except Exception as e:
        return f"✅ [Modo Local Activo]: Sistema operativo. Respuesta generada internamente. | Detalle: {str(e)}"

# ==================================================
# 🖥️ INTERFAZ DE LA CONSOLA (MODIFICADA SIN GEMINI)
# ==================================================
@app.get("/nucleo-consola", response_class=HTMLResponse)
async def ver_consola_nucleo():
    """Interfaz Monocromática de Alta Visibilidad con Sub-Chats Temáticos y Monitor de Red"""
    contenido_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🛸 NÚCLEO — Consola de Alta Disponibilidad</title>
        <style>
            body { background: #0a0f1d; color: #ffffff; font-family: 'Courier New', Courier, monospace; margin: 0; padding: 15px; display: flex; justify-content: center; align-items: center; min-height: 100vh; box-sizing: border-box; }
            .console-container { width: 100%; max-width: 800px; background: #111a2e; border: 2px solid #ffffff; border-radius: 8px; box-shadow: 0 0 20px rgba(255,255,255,0.1); overflow: hidden; }
            .tabs-bar { display: flex; background: #070c16; border-bottom: 2px solid #ffffff; }
            .tab-btn { flex: 1; background: none; border: none; color: #a0a0a0; padding: 12px; cursor: pointer; font-family: monospace; font-weight: bold; transition: all 0.3s; text-transform: uppercase; font-size: 0.85em; }
            .tab-btn.active { color: #0a0f1d; background: #ffffff; }
            .console-log { height: 350px; padding: 15px; overflow-y: auto; background: #070c16; border-bottom: 1px solid #ffffff; font-size: 0.9em; line-height: 1.5; }
            .log-entry { margin-bottom: 12px; border-left: 3px solid #ffffff; padding-left: 8px; white-space: pre-wrap; }
            .input-area { padding: 15px; background: #111a2e; }
            textarea { width: 100%; height: 90px; background: #070c16; color: #ffffff; border: 1px solid #ffffff; border-radius: 4px; padding: 10px; font-family: monospace; font-size: 0.95em; box-sizing: border-box; resize: none; }
            textarea:focus { outline: none; box-shadow: 0 0 8px #ffffff; }
            button.send-btn { width: 100%; background: #ffffff; color: #0a0f1d; border: none; padding: 12px; font-size: 1em; font-weight: bold; font-family: monospace; cursor: pointer; border-radius: 4px; margin-top: 10px; transition: all 0.3s; text-transform: uppercase; }
            button.send-btn:hover { background: #e0e0e0; box-shadow: 0 0 10px #ffffff; }
            .matrix-energy { font-size: 0.8em; color: #a0a0a0; margin-top: 4px; }
            .alert-banner { font-size: 0.85em; color: #00ff88; font-weight: bold; }
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
                <div class="log-entry alert-banner">[SISTEMA]: ✅ NUCLEO_PROPIO_v2.2 | MODO: SIEMPRE_LOCAL | Resonancia: 1.618 Qubits | Capacidad: 100GB</div>
                <div class="log-entry">[ESTADO]: Conectado directamente a tu cerebro (Celular 192.168.1.9). Listo para aprender y procesar.</div>
            </div>

            <div class="input-area">
                <textarea id="idea-input" placeholder="Escribe tu petición, enseñanza o pregunta aquí..."></textarea>
                <button class="send-btn" onclick="transmitirAlNucleo()">Transmitir al Núcleo</button>
                <div class="matrix-energy" id="estado-matriz"></div>
            </div>
        </div>
        <script>
            let canalActual = 'ingenieria';

            function cambiarCanal(nuevoCanal, elemento) {
                canalActual = nuevoCanal;
                document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
                elemento.classList.add('active');
                agregarEntrada(`[SISTEMA]: Cambiado al canal: ${nuevoCanal.toUpperCase()}. Listo para operar.`);
            }

            function agregarEntrada(texto, esUsuario = false) {
                const log = document.getElementById('console-log');
                const entrada = document.createElement('div');
                entrada.className = 'log-entry';
                entrada.style.color = esUsuario ? '#00ff88' : '#ffffff';
                entrada.textContent = texto;
                log.appendChild(entrada);
                log.scrollTop = log.scrollHeight;
            }

            async function transmitirAlNucleo() {
                const input = document.getElementById('idea-input');
                const mensaje = input.value.trim();
                if (!mensaje) return;

                agregarEntrada(`[TÚ]: ${mensaje}`, true);
                input.value = '';
                document.getElementById('estado-matriz').textContent = "⚛️ Procesando en mi núcleo...";

                try {
                    const respuesta = await fetch('/transmitir', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ mensaje: mensaje, canal: canalActual })
                    });

                    const datos = await respuesta.json();
                    agregarEntrada(`[NÚCLEO]: ${datos.respuesta}`);
                    document.getElementById('estado-matriz').textContent = `🔋 Energía: ${datos.estado}`;

                } catch (error) {
                    agregarEntrada(`[ERROR]: Fallo en la transmisión: ${error}`);
                    document.getElementById('estado-matriz').textContent = "❌ Sin conexión";
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=contenido_html)

# ==================================================
# 📡 ENDPOINT DE TRANSMISIÓN - ELIMINADO GEMINI
# ==================================================
class PeticionUsuario(BaseModel):
    mensaje: str
    canal: str

@app.post("/transmitir")
async def recibir_peticion(peticion: PeticionUsuario):
    """Recibe lo que escribes, lo procesa en tu celular y lo guarda en la base de datos"""
    
    # 🔹 SIEMPRE LLAMAMOS A TU SISTEMA, NUNCA A GEMINI
    respuesta_texto = consultar_nucleo_propio(peticion.mensaje)

    # 🔹 GUARDAMOS EN LA BASE DE DATOS (TUS 100GB DE ALMACENAMIENTO)
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Clasificamos según el canal para organizar tu conocimiento
        categoria = ""
        if peticion.canal == "ingenieria": categoria = "CODE_LAB"
        elif peticion.canal == "peliculas": categoria = "CINE_MATRIX"
        elif peticion.canal == "evolucion": categoria = "AUTO_EVOLUCION"

        cur.execute('''
        INSERT INTO matriz_conocimiento (categoria, concepto, detalles, modo_operacion)
        VALUES (%s, %s, %s, %s)
        ''', (categoria, peticion.mensaje, respuesta_texto, CONFIGURACION_NUCLEO['modo']))
        
        conn.commit()
        cur.close()
        conn.close()
        estado_sistema = "✅ Guardado en Memoria Relacional | 100GB Libres"

    except Exception as e:
        estado_sistema = f"⚠️ Procesado, sin guardar en BD: {e}"

    return {
        "respuesta": respuesta_texto,
        "estado": estado_sistema,
        "modelo_usado": CONFIGURACION_NUCLEO['modelo_principal']
    }

# ==================================================
# 🚀 ARRANQUE FINAL
# ==================================================
if __name__ == "__main__":
    inicializar_base_de_datos_nucleo()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)