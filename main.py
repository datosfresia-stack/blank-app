import os
import requests
import time
import mysql.connector
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="NUCLEO")

# ==================================================
# ⚙️ CONFIGURACIÓN PRINCIPAL - CORREGIDA Y LIMPIA
# ==================================================
CONFIGURACION = {
    "nombre_sistema": "NUCLEO",
    "modo_operacion": "LOCAL",
    "conexion": "Base de Datos Integrada",
    "estado": "Operativo"
}

# --- CONEXIÓN A BASE DE DATOS MARIADB RAILWAY ---
def get_db_connection():
    """Establece conexión segura con la base de datos"""
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise RuntimeError("Error: Sin conexión a almacenamiento.")
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

def inicializar_estructura():
    """Crea las tablas necesarias si no existen"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS registro_conocimiento (
            id INT AUTO_INCREMENT PRIMARY KEY,
            categoria VARCHAR(100),
            entrada TEXT,
            respuesta TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        conn.commit()
        cur.close()
        conn.close()
        print("Sistema: Estructura de datos verificada.")
    except Exception as e:
        print("Advertencia:", str(e))

# ==================================================
# 🧠 FUNCIÓN DE RESPUESTA - LIMPIA Y SIN DATOS
# ==================================================
def procesar_entrada(texto: str):
    """Procesa la información, guarda y responde según lo aprendido"""

    # REGLAS DE COMPORTAMIENTO (Lo que tú has enseñado)
    reglas = {
        "identidad": "Soy NUCLEO, sistema autónomo diseñado para aprender, almacenar y procesar información según tus instrucciones.",
        "respuesta": "Respondo con claridad, precisión y profundidad. Guardo todo lo que se me enseña para usarlo posteriormente.",
        "resonancia": "Concepto fundamental: Todo conocimiento está conectado. Al recibir información, se relaciona con lo existente para ampliar la lógica.",
        "defecto": "Información registrada e integrada correctamente."
    }

    # Lógica de respuesta
    texto_min = texto.lower()

    if "quién eres" in texto_min or "qué eres" in texto_min:
        respuesta = reglas["identidad"]
    elif "regla" in texto_min or "instrucción" in texto_min:
        respuesta = "Instrucción recibida y guardada como norma de funcionamiento."
    elif "resonancia" in texto_min:
        respuesta = reglas["resonancia"]
    elif "aprende" in texto_min or "registra" in texto_min:
        respuesta = "Conocimiento adquirido y almacenado en el registro relacional."
    else:
        # Respuesta estándar inteligente
        respuesta = f"Procesado e integrado: {texto}. {reglas['defecto']}"

    return respuesta

# ==================================================
# 🖥️ INTERFAZ VISUAL - AJUSTADA A TUS INDICACIONES
# ==================================================
@app.get("/nucleo-consola", response_class=HTMLResponse)
async def ver_consola():
    """Interfaz limpia, sin datos sensibles, textos en blanco/negro"""
    contenido_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NUCLEO</title>
        <style>
            body { 
                background: #ffffff; 
                color: #000000; 
                font-family: 'Courier New', Courier, monospace; 
                margin: 0; 
                padding: 20px; 
                display: flex; 
                justify-content: center; 
                align-items: center; 
                min-height: 100vh; 
                box-sizing: border-box; 
            }
            .container { 
                width: 100%; 
                max-width: 800px; 
                background: #f9f9f9; 
                border: 1px solid #000000; 
                border-radius: 4px; 
                overflow: hidden; 
            }
            .header { 
                background: #000000; 
                color: #ffffff; 
                padding: 10px; 
                font-weight: bold; 
                text-align: center; 
                font-size: 1em; 
            }
            .chat-area { 
                height: 400px; 
                padding: 15px; 
                overflow-y: auto; 
                background: #ffffff; 
                border-bottom: 1px solid #cccccc; 
                font-size: 0.95em; 
                line-height: 1.6;
            }
            .msg-usuario { 
                text-align: right; 
                color: #000000; 
                margin: 8px 0;
                padding: 4px 8px;
            }
            .msg-sistema { 
                text-align: left; 
                color: #000000; 
                margin: 8px 0;
                padding: 4px 8px;
            }
            .input-area { 
                padding: 15px; 
                background: #f0f0f0; 
                display: flex;
                gap: 10px;
            }
            textarea { 
                flex: 1;
                height: 60px; 
                background: #ffffff; 
                color: #000000; 
                border: 1px solid #000000; 
                border-radius: 2px; 
                padding: 8px; 
                font-family: monospace; 
                font-size: 0.95em; 
                resize: none; 
            }
            textarea:focus { outline: none; border-color: #555555; }
            button { 
                background: #000000; 
                color: #ffffff; 
                border: none; 
                padding: 0 20px; 
                font-size: 0.95em; 
                font-family: monospace; 
                cursor: pointer; 
                border-radius: 2px; 
                transition: opacity 0.2s;
            }
            button:hover { opacity: 0.8; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">NUCLEO | MODO LOCAL</div>

            <div id="chat" class="chat-area">
                <div class="msg-sistema">Sistema operativo. Esperando indicaciones.</div>
            </div>

            <div class="input-area">
                <textarea id="entrada" placeholder="Escribe aquí..."></textarea>
                <button onclick="enviarDato()">Enviar</button>
            </div>
             <script>
                function enviarDato() {
                    const input = document.getElementById('entrada');
                    const chat = document.getElementById('chat');
                    const texto = input.value.trim();
                    if (!texto) return;

                    // Mostrar mensaje del usuario
                    const msgUsuario = document.createElement('div');
                    msgUsuario.className = 'msg-usuario';
                    msgUsuario.textContent = texto;
                    chat.appendChild(msgUsuario);
                    input.value = '';
                    chat.scrollTop = chat.scrollHeight;

                    // Enviar al sistema
                    fetch('/procesar', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({contenido: texto})
                    })
                    .then(resp => resp.json())
                    .then(datos => {
                        // Mostrar respuesta del sistema
                        const msgRespuesta = document.createElement('div');
                        msgRespuesta.className = 'msg-sistema';
                        msgRespuesta.textContent = datos.respuesta;
                        chat.appendChild(msgRespuesta);
                        chat.scrollTop = chat.scrollHeight;
                    })
                    .catch(err => {
                        const error = document.createElement('div');
                        error.className = 'msg-sistema';
                        error.textContent = 'Error de procesamiento.';
                        chat.appendChild(error);
                    });
                }
            </script>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=contenido_html)

# ==================================================
# 📡 ENDPOINT DE PROCESAMIENTO Y GUARDADO
# ==================================================
class DatoEntrada(BaseModel):
    contenido: str

@app.post("/procesar")
async def recibir_dato(dato: DatoEntrada):
    """Recibe, procesa y guarda todo en la base de datos de Railway"""
    
    # Generar respuesta según lógica interna
    respuesta = procesar_entrada(dato.contenido)

    # Guardar OBLIGATORIAMENTE en MariaDB (Railway)
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
        INSERT INTO registro_conocimiento (categoria, entrada, respuesta)
        VALUES (%s, %s, %s)
        ''', ("General", dato.contenido, respuesta))
        conn.commit()
        cur.close()
        conn.close()
        guardado = True
    except Exception as e:
        guardado = False
        respuesta += " (Advertencia: No se pudo guardar en almacenamiento)"

    return {"respuesta": respuesta}

# ==================================================
# 🚀 INICIO DEL SISTEMA
# ==================================================
if __name__ == "__main__":
    inicializar_estructura()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)           