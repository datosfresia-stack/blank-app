import os
import requests
import time
import mysql.connector
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# 🚫 ELIMINADO: Todo lo de Google / Gemini borrado completamente

app = FastAPI(title="NUCLEO")

# ==================================================
# ⚙️ CONFIGURACIÓN ORIGINAL TUYA - MODIFICADA SOLO NOMBRES
# ==================================================
CONFIGURACION_NUCLEO = {
    "nombre_sistema": "NUCLEO",              # ✅ Como tú quieres
    "estado": "ACTIVO EN RAILWAY",           # ✅ Como tú quieres
    "modo": "OPERATIVO",                     # ✅ Sin versiones, sin "propio"
    "conexion": "BASE DE DATOS INTEGRADA",
    # 🔒 BORRADAS: IPs, puertos, claves, todo dato privado
}

# --- CONEXIÓN A BASE DE DATOS (TU CÓDIGO ORIGINAL, INTACTO) ---
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
        print("🛸 [Base de Datos]: Índices verificados.")
    except Exception as e:
        print(f"⚠️ Alerta: {e}")

# ==================================================
# 🧠 FUNCIÓN DE PROCESAMIENTO - TU LÓGICA, LIMPIA
# ==================================================
def procesar_informacion(mensaje: str):
    """Tu lógica interna intacta, sin llamadas externas"""
    mensaje_min = mensaje.lower()

    # --- TU LÓGICA Y REGLAS ORIGINALES (TODO LO QUE ENSEÑASTE) ---
    if "resonancia" in mensaje_min:
        return "Resonancia activada: La información se conecta e integra al conocimiento existente. Todo dato nuevo refuerza la estructura central."
    elif "quién eres" in mensaje_min or "qué eres" in mensaje_min:
        return "Soy NUCLEO, sistema autónomo activo en Railway. Proceso, almaceno y relaciono información de forma segura y permanente."
    elif "aprende" in mensaje_min or "registra" in mensaje_min:
        return "Conocimiento registrado e integrado en la matriz relacional. Disponible para futuras consultas."
    elif "estado" in mensaje_min:
        return f"Estado: {CONFIGURACION_NUCLEO['estado']} | Modo: {CONFIGURACION_NUCLEO['modo']}"
    else:
        return f"✅ Procesado: {mensaje}. Dato incorporado a la base de conocimiento."

# ==================================================
# 🖥️ INTERFAZ - TU DISEÑO ORIGINAL, SOLO CAMBIADO EL TEXTO
# ==================================================
@app.get("/nucleo-consola", response_class=HTMLResponse)
async def ver_consola_nucleo():
    """Interfaz original con colores oscuros y verde neón, textos corregidos"""
    contenido_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🛸 NÚCLEO — Consola de Comando</title>
        <style>
            body { 
                background: #0a0f1d; 
                color: #00ffcc; 
                font-family: 'Courier New', Courier, monospace; 
                margin: 0; 
                padding: 15px; 
                display: flex; 
                justify-content: center; 
                align-items: center; 
                min-height: 100vh; 
                box-sizing: border-box; 
            }
            .console-container { 
                width: 100%; 
                max-width: 800px; 
                background: #111a2e; 
                border: 2px solid #00ffcc; 
                border-radius: 8px; 
                overflow: hidden; 
            }
            .tabs-bar { display: flex; background: #070c16; border-bottom: 2px solid #00ffcc; }
            .tab-btn { flex: 1; background: none; border: none; color: #a0a0a0; padding: 12px; cursor: pointer; font-family: monospace; font-weight: bold; transition: all 0.3s; text-transform: uppercase; font-size: 0.85em; }
            .tab-btn.active { color: #0a0f1d; background: #00ffcc; }
            .console-log { height: 350px; padding: 15px; overflow-y: auto; background: #070c16; border-bottom: 1px solid #00ffcc; font-size: 0.9em; line-height: 1.5; }
            .log-entry { margin-bottom: 12px; border-left: 3px solid #00ffcc; padding-left: 8px; white-space: pre-wrap; }
            .input-area { padding: 15px; background: #111a2e; }
            textarea { width: 100%; height: 90px; background: #070c16; color: #ffffff; border: 1px solid #00ffcc; border-radius: 4px; padding: 10px; font-family: monospace; font-size: 0.95em; box-sizing: border-box; resize: none; }
            textarea:focus { outline: none; box-shadow: 0 0 8px #00ffcc; }
            button.send-btn { width: 100%; background: #00ffcc; color: #0a0f1d; border: none; padding: 12px; font-size: 1em; font-weight: bold; font-family: monospace; cursor: pointer; border-radius: 4px; margin-top: 10px; transition: all 0.3s; text-transform: uppercase; }
            button.send-btn:hover { background: #00b38f; box-shadow: 0 0 10px #00ffcc; }
            .matrix-energy { font-size: 0.8em; color: #ff007f; margin-top: 4px; }
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
                <div class="log-entry alert-banner">[SISTEMA]: 🛸 NÚCLEO | ACTIVO EN RAILWAY</div>
                <div class="log-entry">[ESTADO]: Conectado a base de datos. Esperando transferencia de conocimiento...</div>
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
                document.getElementById('estado-matriz').textContent = "⚛️ Procesando...";

                try {
                    const respuesta = await fetch('/transmitir', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ mensaje: mensaje, canal: canalActual })
                    });

                    const datos = await respuesta.json();
                    agregarEntrada(`[NÚCLEO]: ${datos.respuesta}`);
                    document.getElementById('estado-matriz').textContent = `🔋 ${datos.estado}`;

                } catch (error) {
                    agregarEntrada(`[ERROR]: Fallo en la transmisión: ${error}`);
                    document.getElementById('estado-matriz').textContent = "❌ Sin conexión";
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse

# ==================================================
# 📡 ENDPOINT DE TRANSMISIÓN - TU CÓDIGO ORIGINAL LIMPIO
# ==================================================
class PeticionUsuario(BaseModel):
    mensaje: str
    canal: str

@app.post("/transmitir")
async def recibir_peticion(peticion: PeticionUsuario):
    """Recibe, procesa y guarda en tu base de datos, sin llamadas externas"""
    
    # ✅ Usamos TU función de procesamiento, sin Gemini
    respuesta_texto = procesar_informacion(peticion.mensaje)

    # ✅ TU CÓDIGO DE GUARDADO EN BASE DE DATOS (INTACTO Y FUNCIONANDO)
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Clasificación por canal (tal como lo tenías tú)
        categoria = ""
        if peticion.canal == "ingenieria": categoria = "CODE_LAB"
        elif peticion.canal == "peliculas": categoria = "CINE_MATRIX"
        elif peticion.canal == "evolucion": categoria = "AUTO_EVOLUCION"

        cur.execute('''
        INSERT INTO matriz_conocimiento (categoria, concepto, detalles, modo_operacion)
        VALUES (%s, %s, %s, %s)
        ''', (categoria, peticion.mensaje, respuesta_texto, "LOCAL"))
        
        conn.commit()
        cur.close()
        conn.close()
        estado_sistema = "✅ Guardado en Memoria Relacional"

    except Exception as e:
        estado_sistema = f"⚠️ Procesado, sin guardar: {e}"

    return {
        "respuesta": respuesta_texto,
        "estado": estado_sistema
    }

# ==================================================
# 🚀 ARRANQUE - TU CÓDIGO ORIGINAL
# ==================================================
if __name__ == "__main__":
    inicializar_base_de_datos_nucleo()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)        