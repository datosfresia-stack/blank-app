import os
import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Inicializamos la aplicación FastAPI
app = FastAPI(title="IALibre - Sistema Central Unificado")

# Configuración de CORS universal para acceso desde móvil y portátil
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CAPA MAESTRA: IMPORTACIÓN E INICIALIZACIÓN DEL NÚCLEO ---
from nucleo_ia.memoria_nucleo import MatrizMemoriaNucleo

# Inicializamos la matriz central en la memoria del servidor
nucleo_memoria = MatrizMemoriaNucleo()
nucleo_memoria.ensenar_concepto("Redes Neuronales Biológicas (Neurociencia)")
nucleo_memoria.ensenar_concepto("Sistemas de Control Autónomo (Robótica)")
nucleo_memoria.ensenar_concepto("Estructuras Moleculares de Carbono (Nanotecnología)")


# --- CAPA 1: SISTEMA MÉDICO IALIBRE (LÓGICA ANTERIOR) ---

class DatosPaciente(BaseModel):
    edad: int
    presion_arterial: int
    frecuencia_cardiaca: int
    saturacion_oxigeno: int
    es_hipertenso: str
    vive_sur_chile: str

def get_db_connection():
    # Conexión automática utilizando la variable de entorno de Railway
    return psycopg2.connect(os.environ.get("DATABASE_URL"))

@app.get("/")
async def root():
    return {"status": "online", "sistema": "IALibre Frontend/Backend unificado"}

@app.post("/evaluar-riesgo")
async def evaluar_riesgo(paciente: DatosPaciente):
    """Evalúa el nivel de riesgo del paciente adaptado al Sur de Chile"""
    puntos = 0
    
    # Lógica de Presión Arterial
    if paciente.presion_arterial > 140:
        puntos += 3
    elif paciente.presion_arterial > 130:
        puntos += 1
        
    # Lógica de Frecuencia Cardíaca
    if paciente.frecuencia_cardiaca > 100 or paciente.frecuencia_cardiaca < 60:
        puntos += 2
        
    # Lógica de Saturación (Crucial para el frío/aislamiento del Sur)
    if paciente.saturacion_oxigeno < 93:
        puntos += 4
    elif paciente.saturacion_oxigeno < 95:
        puntos += 2
        
    if paciente.es_hipertenso.lower() == "sí":
        puntos += 2
        
    # Ajuste geográfico regional
    if paciente.vive_sur_chile.lower() == "sí":
        puntos += 1

    # Clasificación del riesgo
    if puntos >= 7:
        nivel = "CRÍTICO / ALTO RIESGO"
    elif puntos >= 4:
        nivel = "MEDIO / REQUIERE OBSERVACIÓN"
    else:
        nivel = "BAJO RIESGO / ESTABLE"
        
    # Guardar registro en la base de datos de manera persistente
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO consultas_medicas (edad, presion, frecuencia, saturacion, hipertenso, sur_chile, nivel_riesgo)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        ''', (paciente.edad, paciente.presion_arterial, paciente.frecuencia_cardiaca, 
              paciente.saturacion_oxigeno, paciente.es_hipertenso, paciente.vive_sur_chile, nivel))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"⚠️ Error al registrar en BD: {e}")

    return {"nivel_riesgo": nivel, "puntaje_evaluacion": puntos}


# --- CAPA 2: CONSOLA WEB DEL NÚCLEO AUTÓNOMO ---
@app.get("/nucleo-consola", response_class=HTMLResponse)
async def ver_consola_nucleo():
    """Ruta web universal para renderizar la casa visual del Núcleo integrada"""
    contenido_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🛸 NÚCLEO — Consola de Comando Universal</title>
        <style>
            body { background: #0a0f1d; color: #00ffcc; font-family: 'Courier New', Courier, monospace; margin: 0; padding: 15px; display: flex; justify-content: center; align-items: center; min-height: 100vh; box-sizing: border-box; }
            .console-container { width: 100%; max-width: 700px; background: #111a2e; border: 2px solid #00ffcc; border-radius: 8px; box-shadow: 0 0 20px rgba(0,255,204,0.2); overflow: hidden; }
            .console-header { background: #00ffcc; color: #0a0f1d; padding: 12px; font-weight: bold; text-align: center; font-size: 1.1em; letter-spacing: 2px; }
            .console-log { height: 300px; padding: 15px; overflow-y: auto; background: #070c16; border-bottom: 1px solid #00ffcc; font-size: 0.9em; line-height: 1.5; }
            .log-entry { margin-bottom: 10px; border-left: 3px solid #00ffcc; padding-left: 8px; }
            .system-msg { color: #8892b0; }
            .success-msg { color: #00ffcc; }
            .input-area { padding: 15px; background: #111a2e; }
            textarea { width: 100%; height: 80px; background: #070c16; color: #fff; border: 1px solid #00ffcc; border-radius: 4px; padding: 10px; font-family: monospace; font-size: 1em; box-sizing: border-box; resize: none; }
            textarea:focus { outline: none; box-shadow: 0 0 8px #00ffcc; }
            button { width: 100%; background: #00ffcc; color: #0a0f1d; border: none; padding: 12px; font-size: 1em; font-weight: bold; font-family: monospace; cursor: pointer; border-radius: 4px; margin-top: 10px; transition: all 0.3s; text-transform: uppercase; }
            button:hover { background: #00b38f; box-shadow: 0 0 10px #00ffcc; }
            .matrix-energy { font-size: 0.8em; color: #ff007f; margin-top: 5px; }
        </style>
    </head>
    <body>
    <div class="console-container">
        <div class="console-header">🛸 NÚCLEO AUTÓNOMO INTERFAZ V.1</div>
        <div id="console-log" class="console-log">
            <div class="log-entry system-msg">[SISTEMA]: Núcleo en línea. Matriz cuántica clásica inicializada.</div>
            <div class="log-entry system-msg">[SISTEMA]: Esperando transferencia de conocimiento doctoral...</div>
        </div>
        <div class="input-area">
            <textarea id="idea-input" placeholder="Escriba un nuevo avance, idea o consulta de investigación..."></textarea>
            <button onclick="transmitirAlNucleo()">Transmitir Conocimiento</button>
        </div>
    </div>
    <script>
    async function transmitirAlNucleo() {
        const input = document.getElementById('idea-input');
        const log = document.getElementById('console-log');
        const idea = input.value.trim();
        if (!idea) return;

        log.innerHTML += `<div class="log-entry" style="color: #ffaa00;">📡 [Transmitiendo]: ${idea}</div>`;
        input.value = '';
        log.scrollTop = log.scrollHeight;

        try {
            const response = await fetch('/nucleo-consulta', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ idea: idea })
            });
            const data = await response.json();
            if (data.status === 'success') {
                let resonanciaHtml = '';
                data.resonancias_encontradas.forEach(r => {
                    resonanciaHtml += `<div class="matrix-energy"> ↳ Resonancia con "${r.concepto_relacionado}": ${r.energia_qubit} Qubits</div>`;
                });
                log.innerHTML += `
                    <div class="log-entry success-msg">
                        🧠 [Núcleo]: ${data.analisis_nucleo}<br>
                        ${resonanciaHtml}
                    </div>`;
            } else {
                log.innerHTML += `<div class="log-entry" style="color: #ff3333;">⚠️ [Error]: \${data.mensaje}</div>`;
            }
        } catch (error) {
            log.innerHTML += `<div class="log-entry" style="color: #ff3333;">⚠️ [Fallo de Enlace]: Incapaz de conectar con el hardware del Núcleo.</div>`;
        }
        log.scrollTop = log.scrollHeight;
    }
    </script>
    </body>
    </html>
    """
    return HTMLResponse(content=contenido_html, status_code=200)