import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

# ✅ IMPORTAMOS TU ARCHIVO database.py TAL CUAL LO TIENES
from database import get_db, init_db

app = FastAPI(title="NUCLEO")

# ⚙️ CONFIGURACIÓN
CONFIGURACION_NUCLEO = {
    "nombre_sistema": "NUCLEO",
    "estado": "ACTIVO EN RAILWAY",
    "modo": "OPERATIVO",
    "conexion": "BASE DE DATOS ASÍNCRONA INTEGRADA"
}

# 🧠 LÓGICA COMPLETA (AQUÍ ES DONDE PIENSA Y RESPONDE)
def procesar_informacion(mensaje: str):
    mensaje_min = mensaje.lower()

    if "resonancia" in mensaje_min or "conecta" in mensaje_min:
        return "🔄 Resonancia activada: La información se cruza, conecta y refuerza todo el conocimiento existente. Estructura ampliada."
    elif "quién eres" in mensaje_min or "qué eres" in mensaje_min or "identificate" in mensaje_min:
        return "🤖 Soy NÚCLEO, sistema autónomo. Proceso, analizo, guardo y relaciono información. Opero de forma independiente y segura."
    elif "aprende" in mensaje_min or "registra" in mensaje_min or "enseña" in mensaje_min:
        return "🧠 Conocimiento integrado y almacenado en la matriz relacional. Ahora forma parte de mi base de datos permanente."
    elif "estado" in mensaje_min or "cómo estás" in mensaje_min or "sistema" in mensaje_min:
        return f"📊 Estado: {CONFIGURACION_NUCLEO['estado']} | Modo: {CONFIGURACION_NUCLEO['modo']} | Memoria activa."
    elif "hola" in mensaje_min or "saludo" in mensaje_min:
        return "👋 Hola. Sistema operativo estable. Esperando instrucciones o nueva información para procesar."
    elif "mejoras" in mensaje_min or "código" in mensaje_min or "optimizar" in mensaje_min:
        return "⚙️ Análisis de código: Se recomienda modularizar funciones, optimizar consultas a base de datos y reforzar seguridad. Datos registrados para futura evolución."
    elif "ayudar" in mensaje_min or "funciones" in mensaje_min or "qué haces" in mensaje_min:
        return "💡 Puedo: Almacenar información, relacionar conceptos, responder consultas, analizar datos y evolucionar con cada enseñanza que me entregues."
    elif "matriz" in mensaje_min or "cine" in mensaje_min:
        return "🎬 Modo Cine activado: Se almacenan conceptos narrativos, estructuras de guion y análisis de contenido audiovisual."
    elif "evolución" in mensaje_min or "crecimiento" in mensaje_min:
        return "📈 Auto-evolución: Cada dato nuevo refuerza mi lógica. Aprendo de lo que me enseñas y mejoro mis respuestas automáticamente."
    else:
        return f"✅ Información procesada: '{mensaje}'. Analizada, clasificada y guardada. Relacionada con conocimientos previos."

# 🖥️ INTERFAZ: FONDO NEGRO, LETRAS BLANCAS, BORDES PLOMO/GRIS
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
            body { 
                background: #000000 !important; 
                color: #ffffff !important; 
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
                background: #000000; 
                border: 2px solid #888888; 
                border-radius: 8px; 
                overflow: hidden; 
            }
            .tabs-bar { 
                display: flex; 
                background: #111111; 
                border-bottom: 2px solid #888888; 
            }
            .tab-btn { 
                flex:1; 
                background:#000; 
                border:none; 
                color:#ffffff; 
                padding:12px; 
                cursor:pointer; 
                font-family:monospace; 
                font-weight:bold; 
                transition:all 0.2s; 
                text-transform:uppercase; 
                font-size:0.85em; 
            }
            .tab-btn.active { 
                color:#000; 
                background:#888888; 
            }
            .console-log { 
                height:350px; 
                padding:15px; 
                overflow-y:auto; 
                background:#000000; 
                border-bottom:1px solid #888888; 
                font-size:0.9em; 
                line-height:1.6;
                color: #ffffff !important;
            }
            .log-entry { 
                margin-bottom:12px; 
                border-left:3px solid #888888; 
                padding-left:8px; 
                color: #ffffff !important;
            }
            .input-area { 
                padding:15px; 
                background:#000000; 
            }
            textarea { 
                width:100%; 
                height:90px; 
                background:#1a1a1a; 
                color:#ffffff !important; 
                border:1px solid #888888; 
                border-radius:4px; 
                padding:10px; 
                font-family:monospace; 
                font-size:0.95em; 
                box-sizing:border-box; 
                resize:none; 
            }
            textarea:focus { outline:none; box-shadow:0 0 6px #aaaaaa; }
            .send-btn { 
                width:100%; 
                background:#888888; 
                color:#000000; 
                border:none; 
                padding:12px; 
                font-size:1em; 
                font-weight:bold; 
                font-family:monospace; 
                cursor:pointer; 
                border-radius:4px; 
                margin-top:10px; 
                transition:all 0.3s; 
                text-transform:uppercase; 
            }
            .send-btn:hover { background:#aaaaaa; }
            .matrix-energy { 
                font-size:0.8em; 
                color:#bbbbbb; 
                margin-top:4px; 
            }
            .alert-banner { 
                font-size:0.85em; 
                color:#cccccc; 
                font-weight:bold; 
            }
        </style>
    </head>
    <body>
        <div class="console-container">
            <div class="tabs-bar">
                <button class="tab-btn active" onclick="cambiarCanal('ingenieria', this)">💻 LABORATORIO DE PROGRAMACIÓN</button>
                <button class="tab-btn" onclick="cambiarCanal('peliculas', this)">🎬 MATRIZ DE CINE</button>
                <button class="tab-btn" onclick="cambiarCanal('evolucion', this)">🧬 AUTO-EVOLUCIÓN</button>
            </div>

            <div id="console-log" class="console-log">
                <div class="log-entry alert-banner">[SISTEMA]: 🛸 NÚCLEO | ACTIVO EN RAILWAY</div>
                <div class="log-entry">[ESTADO]: Conectado a base de datos. Esperando transferencia...</div>
            </div>

            <div class="input-area">
                <textarea id="idea-input" placeholder="Escribe tu petición, enseñanza o pregunta aquí..."></textarea>
                <button class="send-btn" onclick="transmitirAlNucleo()">TRANSMITIR AL NÚCLEO</button>
                <div class="matrix-energy" id="estado-matriz"></div>
            </div>
        </div>

        <script>
            let canalActual = 'ingenieria';
            function cambiarCanal(nuevoCanal, el) {
                canalActual = nuevoCanal;
                document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
                el.classList.add('active');
                let nombre = nuevoCanal === 'ingenieria' ? 'INGENIERÍA' : nuevoCanal === 'peliculas' ? 'PELÍCULAS' : 'EVOLUCIÓN';
                agregarEntrada(`[SISTEMA]: Cambiado a ${nombre}. Modo especial activado.`);
            }
            function agregarEntrada(texto, usuario=false) {
                const log = document.getElementById('console-log');
                const div = document.createElement('div');
                div.className = 'log-entry';
                div.style.color = usuario ? '#cccccc' : '#ffffff';
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
                document.getElementById('estado-matriz').textContent = "⚛️ Analizando...";
                try {
                    const res = await fetch('/transmitir', {
                        method:'POST',
                        headers:{'Content-Type':'application/json'},
                        body:JSON.stringify({mensaje, canal:canalActual})
                    });
                    const data = await res.json();
                    agregarEntrada(`[NÚCLEO]: ${data.respuesta}`);
                    document.getElementById('estado-matriz').textContent = `💾 ${data.estado}`;
                } catch(e) {
                    agregarEntrada(`[ERROR]: ${e}`);
                    document.getElementById('estado-matriz').textContent = "❌ Fallo en enlace";
                }
            }
        </script>
    </body>
    </html>
    """)

# 📡 ESTRUCTURA DE DATOS
class PeticionUsuario(BaseModel):
    mensaje: str
    canal: str

# 📡 ENDPOINT ADAPTADO A TU database.py
@app.post("/transmitir")
async def recibir_peticion(
    peticion: PeticionUsuario, 
    db: AsyncSession = Depends(get_db)
):
    # 1. Generamos la respuesta inteligente
    respuesta_texto = procesar_informacion(peticion.mensaje)

    # 2. Guardamos en base usando SQLAlchemy (tu sistema)
    try:
        # Definimos la categoría según la pestaña
        cat = {
            "ingenieria":"CODE_LAB", 
            "peliculas":"CINE_MATRIX", 
            "evolucion":"AUTO_EVOLUCION"
        }.get(peticion.canal, "GENERAL")

        # Creamos la tabla si no existe y guardamos (consulta SQL directa compatible)
        await db.execute(text("""
            CREATE TABLE IF NOT EXISTS matriz_conocimiento (
                id INT AUTO_INCREMENT PRIMARY KEY,
                categoria VARCHAR(100),
                concepto VARCHAR(255),
                detalles TEXT,
                fecha_aprendizaje TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        await db.execute(
            text("INSERT INTO matriz_conocimiento (categoria, concepto, detalles) VALUES (:cat, :msg, :resp)"),
            {"cat": cat, "msg": peticion.mensaje, "resp": respuesta_texto}
        )
        await db.commit()
        estado = "✅ Guardado en Memoria Relacional"

    except Exception as e:
        estado = f"⚠️ Guardado fallido: {str(e)}"

    return {"respuesta": respuesta_texto, "estado": estado}

# 🚀 ARRANQUE INICIAL
@app.on_event("startup")
async def startup_event():
    await init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
