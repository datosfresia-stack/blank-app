import os
import mysql.connector
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI(title="IALibre Núcleo Resiliente V4.1")

# --- MEMORIA VOLÁTIL DE ALTA CAPACIDAD PARA CONVERSACIÓN CONTINUA ---
# Almacena el historial completo de la sesión de chat para mantener la continuidad
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
    """Interfaz Monocromática con Chat de Sesión Continuo y Canales Doctorales"""
    contenido_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🛸 NÚCLEO — Consola de Alta Disponibilidad</title>
        <style>
            body { background: #0a0f1d; color: #ffffff; font-family: 'Courier New', Courier, monospace; margin: 0; padding: 15px; display: flex; justify-content: center; align-items: center; min-height: 100vh; box-sizing: border-box; }
            .console-container { width: 100%; max-width: 900px; width: 100%; background: #111a2e; border: 2px solid #ffffff; border-radius: 8px; box-shadow: 0 0 20px rgba(255,255,255,0.1); overflow: hidden; display: flex; flex-direction: column; }
            .tabs-bar { display: flex; background: #070c16; border-bottom: 2px solid #ffffff; flex-wrap: wrap; }
            .tab-btn { flex: 1; min-width: 120px; background: none; border: none; color: #a0a0a0; padding: 12px; cursor: pointer; font-family: monospace; font-weight: bold; transition: all 0.3s; text-transform: uppercase; font-size: 0.85em; }
            .tab-btn.active { color: #0a0f1d; background: #ffffff; }
            .console-log { height: 450px; padding: 15px; overflow-y: auto; background: #070c16; border-bottom: 1px solid #ffffff; font-size: 0.9em; line-height: 1.5; }
            .log-entry { margin-bottom: 15px; border-left: 3px solid #ffffff; padding-left: 10px; white-space: pre-wrap; word-break: break-word; }
            .input-area { padding: 15px; background: #111a2e; }
            textarea { width: 100%; height: 110px; background: #070c16; color: #ffffff; border: 1px solid #ffffff; border-radius: 4px; padding: 10px; font-family: monospace; font-size: 0.95em; box-sizing: border-box; resize: vertical; }
            textarea:focus { outline: none; box-shadow: 0 0 8px #ffffff; }
            button.send-btn { width: 100%; background: #ffffff; color: #0a0f1d; border: none; padding: 14px; font-size: 1em; font-weight: bold; font-family: monospace; cursor: pointer; border-radius: 4px; margin-top: 10px; transition: all 0.3s; text-transform: uppercase; }
            button.send-btn:hover { background: #e0e0e0; box-shadow: 0 0 10px #ffffff; }
            .matrix-energy { font-size: 0.8em; color: #a0a0a0; margin-top: 6px; }
            .alert-banner { font-size: 0.85em; color: #ffaa00; font-weight: bold; }
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
            <div class="log-entry" style="color: #a0a0a0;">[SISTEMA]: Enlace directo secuencial establecido. Sesión unificada activa para flujos de desarrollo extensos. Listo para Miguel.</div>
        </div>
        <div class="input-area">
            <textarea id="idea-input" placeholder="Escribe tus preguntas, reflexiones o códigos fuentes masivos aquí..."></textarea>
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
        log.innerHTML += `<div class="log-entry" style="color: #a0a0a0;">[SISTEMA]: Enrutando flujo de datos hacia canal #${canalActual.toUpperCase()}.</div>`;
        log.scrollTop = log.scrollHeight;
    }

    async function transmitirAlNucleo() {
        const input = document.getElementById('idea-input');
        const log = document.getElementById('console-log');
        const idea = input.value.trim();
        if (!idea) return;

        // Mostrar lo que envía Miguel en pantalla (Color ámbar/naranja para distinguir los envíos del usuario)
        log.innerHTML += `<div class="log-entry" style="color: #ffaa00;">📡 [Miguel — Transmisión Activa]:\n${escaparHTML(idea)}</div>`;
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
                alertaHtml = `<div class="alert-banner">⚠️ [ALERTA]: Enlace caído o saturado. Operando bajo contingencia local.</div>`;
            }

            if (data.status === 'success') {
                log.innerHTML += `
                    <div class="log-entry" style="color: #ffffff;">
                        ${alertaHtml}
                        🧠 [Núcleo]: ${formatearRespuesta(data.analisis_nucleo)}
                        <div class="matrix-energy"> ↳ Registro: ${data.registro_id} | Resonancia: ${data.energia} Qubits | Modo: ${data.modo_operacion}</div>
                    </div>`;
            } else {
                log.innerHTML += `<div class="log-entry" style="color: #ff3333;">⚠️ [Error Interno]: ${data.mensaje}</div>`;
            }
        } catch (error) {
            log.innerHTML += `<div class="log-entry" style="color: #ff3333;">⚠️ [Fallo Crítico]: Servidor o pasarela de red inalcanzable.</div>`;
        }
        log.scrollTop = log.scrollHeight;
    }

    function escaparHTML(str) {
        return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }

    function formatearRespuesta(texto) {
    if (!texto) return "";
    // Reemplaza los saltos de línea literales y los escapados por etiquetas HTML <br>
    return escaparHTML(texto).replace(/\n/g, "<br>").replace(/\\n/g, "<br>");
}
    </script>
    </body>
    </html>
    """
    return HTMLResponse(content=contenido_html, status_code=200)


# --- CONSOLA DE SUB-CHATS INTERACTIVOS UNIFICADA (PARCHE DEFINITIVO) ---
@app.get("/nucleo-consola", response_class=HTMLResponse)
async def ver_consola_nucleo():
    """Interfaz Monocromática con Estilos Cian Originales y Transmisión Corregida"""
    contenido_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🛸 NÚCLEO — Consola de Alta Disponibilidad</title>
        <style>
            body { background: #0a0f1d; color: #ffffff; font-family: 'Courier New', Courier, monospace; margin: 0; padding: 15px; display: flex; justify-content: center; align-items: center; min-height: 100vh; box-sizing: border-box; }
            .console-container { width: 100%; max-width: 950px; width: 100%; background: #070c16; border: 2px solid #00ffcc; border-radius: 8px; box-shadow: 0 0 20px rgba(0,255,204,0.2); overflow: hidden; display: flex; flex-direction: column; }
            .tabs-bar { display: flex; background: #0a0f1d; border-bottom: 2px solid #00ffcc; flex-wrap: wrap; }
            .tab-btn { flex: 1; min-width: 120px; background: none; border: none; color: #a0a0a0; padding: 14px; cursor: pointer; font-family: monospace; font-weight: bold; transition: all 0.3s; text-transform: uppercase; font-size: 0.85em; border-right: 1px solid rgba(0,255,204,0.3); }
            .tab-btn:last-child { border-right: none; }
            .tab-btn.active { color: #070c16; background: #00ffcc; }
            .console-log { height: 480px; padding: 20px; overflow-y: auto; background: #070c16; border-bottom: 2px solid #00ffcc; font-size: 0.95em; line-height: 1.6; }
            .log-entry { margin-bottom: 18px; border-left: 3px solid #00ffcc; padding-left: 12px; white-space: pre-wrap; word-break: break-word; }
            .input-area { padding: 20px; background: #070c16; }
            textarea { width: 100%; height: 110px; background: #070c16; color: #ffffff; border: 2px solid #00ffcc; border-radius: 6px; padding: 12px; font-family: monospace; font-size: 1em; box-sizing: border-box; resize: vertical; }
            textarea:focus { outline: none; box-shadow: 0 0 12px #00ffcc; }
            button.send-btn { width: 100%; background: #00ffcc; color: #070c16; border: none; padding: 16px; font-size: 1.05em; font-weight: bold; font-family: monospace; cursor: pointer; border-radius: 6px; margin-top: 12px; transition: all 0.3s; text-transform: uppercase; letter-spacing: 1px; }
            button.send-btn:hover { background: #00ccaa; box-shadow: 0 0 15px #00ffcc; }
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
            <div class="log-entry" style="color: #00ffcc;">[SISTEMA]: Enlace directo secuencial establecido. canal #CHAT_DIRECTO activo. Listo para operar, Miguel.</div>
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
        
        if (!input || !log) {
            alert("Error crítico: No se encontraron los componentes en la interfaz.");
            return;
        }

        const idea = input.value.trim();
        if (!idea) return;

        // Imprimir inmediatamente en pantalla para verificar que el botón funciona
        log.innerHTML += `<div class="log-entry" style="color: #ffaa00;">📡 [Miguel — Transmisión Activa]:\\n${escaparHTML(idea)}</div>`;
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
                alertaHtml = `<div class="alert-banner">⚠️ [ALERTA]: Enlace caído o saturado. Operando bajo contingencia local.</div>`;
            }

            if (data.status === 'success') {
                log.innerHTML += `
                    <div class="log-entry" style="color: #00ffcc;">
                        ${alertaHtml}
                        🧠 [Núcleo]: ${formatearRespuesta(data.analisis_nucleo)}
                        <div class="matrix-energy"> ↳ Registro Relacional: ${data.registro_id} | Resonancia: ${data.energia} Qubits | Modo: ${data.modo_operacion}</div>
                    </div>`;
            } else {
                log.innerHTML += `<div class="log-entry" style="color: #ff3333;">⚠️ [Error Interno]: ${data.mensaje}</div>`;
            }
        } catch (error) {
            log.innerHTML += `<div class="log-entry" style="color: #ff3333;">⚠️ [Fallo Crítico]: La pasarela de red no devolvió una respuesta válida.</div>`;
        }
        log.scrollTop = log.scrollHeight;
    }

    function escaparHTML(str) {
        return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
    }

    function formatearRespuesta(texto) {
        if (!texto) return "";
        let sinSaltosFalsos = texto.replace(/\\\\n/g, "<br>").replace(/\\n/g, "<br>");
        return sinSaltosFalsos;
    }
    </script>
    </body>
    </html>
    """
    return HTMLResponse(content=contenido_html, status_code=200)