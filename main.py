import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Inicializamos FastAPI
app = FastAPI(title="IA Núcleo")

# =====================================================================
# CONFIGURACIÓN DE LA BASE DE DATOS MARIADB (RAILWAY)
# =====================================================================
DB_CONFIG = {
    'host': 'nozomi.proxy.rlwy.net',
    'port': 18384,
    'user': 'root',
    'password': 'E7hZ5nq8FrmUL4iSeRP1bvel5cDkQVil',
    'database': 'railway'
}

AREAS_INTERES = {
    "1": "Informática", "2": "Robótica", "3": "Nanotecnología",
    "4": "Neurociencia", "5": "Medicina", "6": "Medicina Ancestral",
    "7": "Redes Cuánticas", "8": "Electrónica", "9": "Biotecnología",
    "10": "Sinergia Humano-IA"
}

def conectar_db():
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        if conexion.is_connected():
            return conexion
    except Error:
        return None

class ConsultaRequest(BaseModel):
    entrada: str

class AprendizajeRequest(BaseModel):
    entrada: str
    seleccion_area: str
    descripcion: str
    respuesta: str

# =====================================================================
# INTERFAZ DE USUARIO (SOLUCIÓN AL ERROR 404)
# =====================================================================

@app.get("/nucleo-consola", response_class=HTMLResponse)
def renderizar_consola():
    """Entrega la interfaz web de la Consola Núcleo para evitar el 404."""
    options_html = "".join([f"<option value='{k}'>{v}</option>" for k, v in AREAS_INTERES.items()])
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Consola Maestra - Núcleo</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #e2e8f0; margin: 0; padding: 20px; }}
            .container {{ max-width: 800px; margin: 0 auto; background: #1e293b; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.5); }}
            h1 {{ color: #38bdf8; border-bottom: 2px solid #334155; padding-bottom: 10px; margin-top: 0; }}
            .box {{ background: #0f172a; padding: 20px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #334155; }}
            label {{ display: block; margin-bottom: 8px; font-weight: bold; color: #94a3b8; }}
            input, textarea, select {{ width: 100%; padding: 10px; background: #1e293b; border: 1px solid #475569; border-radius: 6px; color: white; box-sizing: border-box; margin-bottom: 15px; }}
            button {{ background: #0284c7; color: white; border: none; padding: 12px 20px; border-radius: 6px; cursor: pointer; font-weight: bold; width: 100%; }}
            button:hover {{ background: #0369a1; }}
            #output {{ min-height: 50px; white-space: pre-wrap; font-family: monospace; color: #34d399; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Sistema Soberano Núcleo</h1>
            
            <div class="box">
                <h3>🔍 Consultar Enciclopedia</h3>
                <label>Concepto o Nodo:</label>
                <input type="text" id="queryInput" placeholder="Ej: Redes Cuánticas">
                <button onclick="ejecutarConsulta()">Consultar Cerebro Local</button>
            </div>

            <div class="box">
                <h3>🧠 Indexar Nuevo Conocimiento</h3>
                <label>Nombre del Nodo:</label>
                <input type="text" id="learnInput" placeholder="Ej: Medicina Ancestral">
                <label>Macroárea:</label>
                <select id="areaSelect">{options_html}</select>
                <label>Descripción Corta:</label>
                <input type="text" id="descInput" placeholder="Contexto general del concepto">
                <label>Respuesta o Instrucción Asociada:</label>
                <textarea id="respInput" rows="3" placeholder="Escribe aquí el conocimiento exacto..."></textarea>
                <button style="background: #10b981;" onclick="ejecutarAprendizaje()">Grabar en MariaDB</button>
            </div>

            <div class="box">
                <h3>📟 Terminal de Salida</h3>
                <div id="output">Consola lista y en espera de órdenes...</div>
            </div>
        </div>

        <script>
            async function ejecutarConsulta() {{
                const entrada = document.getElementById('queryInput').value;
                const out = document.getElementById('output');
                out.innerText = "Buscando en la enciclopedia local...";
                try {{
                    const response = await fetch('/consultar', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ entrada }})
                    }});
                    const data = await response.json();
                    out.innerText = data.respuesta;
                }} catch(e) {{
                    out.innerText = "Error de comunicación con el backend.";
                }}
            }}

            async function ejecutarAprendizaje() {{
                const payload = {{
                    entrada: document.getElementById('learnInput').value,
                    seleccion_area: document.getElementById('areaSelect').value,
                    descripcion: document.getElementById('descInput').value,
                    respuesta: document.getElementById('respInput').value
                }};
                const out = document.getElementById('output');
                out.innerText = "Escribiendo en MariaDB...";
                try {{
                    const response = await fetch('/aprender', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(payload)
                    }});
                    const data = await response.json();
                    out.innerText = data.mensaje || data.detail;
                }} catch(e) {{
                    out.innerText = "Error al intentar registrar en la base de datos.";
                }}
            }}
        </script>
    </body>
    </html>
    """
    return html_content

# =====================================================================
# ENDPOINTS DE CONTROL (CONSULTA Y APRENDIZAJE)
# =====================================================================

@app.get("/")
def estado_sistema():
    return {"status": "online", "sistema": "Núcleo", "modo": "Soberano Directo"}

@app.post("/consultar")
def procesar_consulta(datos: ConsultaRequest):
    entrada_limpia = datos.entrada.strip()
    if not entrada_limpia:
        raise HTTPException(status_code=400, detail="Consulta vacía.")

    conexion = conectar_db()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error: Cerebro MariaDB desconectado.")

    respuesta_guardada = None
    try:
        cursor = conexion.cursor()
        query = "SELECT respuesta_asociada FROM enciclopedia_nodos WHERE nodo_nombre = %s AND estado = 'Activo'"
        cursor.execute(query, (entrada_limpia,))
        resultado = cursor.fetchone()
        if resultado:
            respuesta_guardada = resultado[0]
    except Error:
        raise HTTPException(status_code=500, detail="Error al consultar los registros.")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

    if respuesta_guardada:
        return {"encontrado": True, "respuesta": f"🤖 Núcleo: {respuesta_guardada}"}
    return {"encontrado": False, "respuesta": "🤖 Núcleo: Nodo no registrado en el almacenamiento local."}

@app.post("/aprender")
def registrar_conocimiento(datos: AprendizajeRequest):
    conexion = conectar_db()
    if not conexion:
        raise HTTPException(status_code=500, detail="Sin conexión a MariaDB.")

    tipo_nodo = AREAS_INTERES.get(datos.seleccion_area.strip(), "General")
    
    try:
        cursor = conexion.cursor()
        query = """
            INSERT INTO enciclopedia_nodos 
            (nodo_nombre, tipo, descripcion, respuesta_asociada, fecha_creacion, estado) 
            VALUES (%s, %s, %s, %s, %s, 'Activo')
        """
        valores = (datos.entrada.strip(), tipo_nodo, datos.descripcion.strip(), datos.respuesta.strip(), datetime.now())
        cursor.execute(query, valores)
        conexion.commit()
        return {"status": "success", "mensaje": f"🤖 Núcleo: Conocimiento indexado en '{tipo_nodo}' con éxito."}
    except Error as e:
        conexion.rollback()
        raise HTTPException(status_code=500, detail=f"Fallo de escritura: {e}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()