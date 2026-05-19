import os
import pymysql
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel, Field
from datetime import datetime
import uvicorn

app = FastAPI(title="IA Nucleo Terminal")

DB_CONFIG = {
    'host': 'nozomi.proxy.rlwy.net',
    'port': 18384,
    'user': 'root',
    'password': 'E7hZ5nq8FrmUL4iSeRP1bvel5cDkQVil',
    'database': 'railway'
}

class EntradaFrase(BaseModel):
    frase: str = Field(..., min_length=1, max_length=255)
    respuesta: str = Field(None, max_length=1000)

def obtener_conexion():
    try:
        return pymysql.connect(
            host=DB_CONFIG['host'], port=DB_CONFIG['port'],
            user=DB_CONFIG['user'], password=DB_CONFIG['password'],
            database=DB_CONFIG['database'], autocommit=True, connect_timeout=5
        )
    except pymysql.MySQLError:
        return None

@app.get("/")
def raiz():
    return RedirectResponse(url='/terminal')

# RUTA NUEVA TOTALMENTE FORZADA
@app.get("/terminal", response_class=HTMLResponse)
def interfaz_grafica():
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>IA Núcleo - Terminal</title>
        <style>
            body { background-color: #0d1117; color: #c9d1d9; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .contenedor { background-color: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 30px; width: 450px; box-shadow: 0 8px 24px rgba(0,0,0,0.5); }
            h1 { color: #58a6ff; font-size: 24px; text-align: center; margin-top:0; padding-bottom: 15px; border-bottom: 1px solid #30363d; }
            .grupo { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; font-size: 14px; color: #8b949e; }
            input[type="text"], textarea { width: 100%; padding: 10px; background-color: #0d1117; border: 1px solid #30363d; border-radius: 6px; color: #c9d1d9; box-sizing: border-box; }
            button { width: 100%; padding: 12px; background-color: #238636; color: white; border: none; border-radius: 6px; font-size: 15px; font-weight: bold; cursor: pointer; }
            button:hover { background-color: #2ea043; }
            .consola-respuesta { margin-top: 20px; background-color: #0d1117; border-left: 4px solid #58a6ff; padding: 15px; border-radius: 4px; font-family: monospace; font-size: 13px; }
        </style>
    </head>
    <body>
        <div class="contenedor">
            <h1>🤖 Terminal NÚCLEO</h1>
            <div class="grupo">
                <label>Concepto o Frase:</label>
                <input type="text" id="frase" placeholder="Escribe aquí...">
            </div>
            <div class="grupo">
                <label>Respuesta (Opcional para Aprender):</label>
                <textarea id="respuesta" rows="3" placeholder="Si escribes aquí, se guardará en MariaDB..."></textarea>
            </div>
            <button onclick="enviar()">Transmitir a Núcleo</button>
            <div class="consola-respuesta" id="pantalla">Esperando transmisión...</div>
        </div>
        <script>
            async function enviar() {
                const f = document.getElementById('frase').value.trim();
                const r = document.getElementById('respuesta').value.trim();
                const p = document.getElementById('pantalla');
                if(!f) { p.innerHTML = "⚠️ Escribe una frase."; return; }
                p.innerHTML = "⚡ Conectando a MariaDB...";
                let payload = { frase: f };
                if(r) payload.respuesta = r;
                try {
                    const res = await fetch('/nucleo', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });
                    const data = await res.json();
                    p.innerHTML = data.respuesta || data.mensaje;
                    if(r && res.ok) { document.getElementById('frase').value=''; document.getElementById('respuesta').value=''; }
                } catch(e) { p.innerHTML = "❌ Error de red."; }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/nucleo")
def procesar_nucleo(datos: EntradaFrase):
    frase_limpia = datos.frase.strip()
    conexion = obtener_conexion()
    if not conexion:
        raise HTTPException(status_code=503, detail="MariaDB desconectado.")
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            if datos.respuesta:
                query = "INSERT INTO enciclopedia_nodos (nodo_nombre, tipo, descripcion, respuesta_asociada, fecha_creacion, estado) VALUES (%s, 'General', 'Grafica', %s, %s, 'Activo')"
                cursor.execute(query, (frase_limpia, datos.respuesta.strip(), datetime.now()))
                return {"respuesta": f"✨ Registro grabado en MariaDB. Aprendido: '{frase_limpia}'."}
            else:
                query = "SELECT respuesta_asociada FROM enciclopedia_nodos WHERE nodo_nombre LIKE %s AND estado = 'Activo' LIMIT 1"
                cursor.execute(query, (f"%{frase_limpia}%",))
                nodo = cursor.fetchone()
                if nodo: return {"respuesta": nodo['respuesta_asociada']}
                return {"respuesta": f"❌ No encontré respuestas para '{frase_limpia}'."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conexion.close()

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=puerto, reload=False)