import os
import sys
import random
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# ✅ RUTA CORREGIDA PARA ENCONTRAR database.py Y .env (Railway)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database import get_db_connection

# 🛸 INICIALIZACIÓN DEL NÚCLEO - VERSIÓN AUTÓNOMA V2
# Conectado a Base de Datos RAILWAY - Enlace Público
app = FastAPI(title="IALibre Núcleo Autónomo V2 - Railway Producción")

def inicializar_base_de_datos_nucleo():
    """Crea la estructura completa de NODOS y ENLACES en la BD de Railway"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Tabla de Datos Biomédicos (tu estructura original para el proyecto Sur de Chile)
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
        );''')

        # 🧠 TABLA MATRIZ DE CONOCIMIENTO: Preparada para ÁLGEBRA LINEAL Y VECTORES
        cur.execute('''
        CREATE TABLE IF NOT EXISTS matriz_conocimiento (
            id INT AUTO_INCREMENT PRIMARY KEY,
            categoria VARCHAR(100),
            concepto VARCHAR(255),
            detalles TEXT,
            coordenada_x FLOAT DEFAULT 0.0,
            coordenada_y FLOAT DEFAULT 0.0,
            coordenada_z FLOAT DEFAULT 0.0,
            magnitud FLOAT DEFAULT 1.0,
            modo_operacion VARCHAR(50) DEFAULT 'STANDARD',
            fecha_aprendizaje TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );''')

        # 🔗 TABLA DE ENLACES: EL CORAZÓN DE TU INTELIGENCIA (Red Semántica)
        cur.execute('''
        CREATE TABLE IF NOT EXISTS enciclopedia_nodos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            area VARCHAR(100) NOT NULL,
            concepto VARCHAR(255) NOT NULL,
            definicion_profunda LONGTEXT NOT NULL,
            vector_embedding JSON,
            requisitos_previos TEXT,
            fecha_indexacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS enciclopedia_enlaces (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nodo_origen_id INT,
            nodo_destino_id INT,
            tipo_conexion VARCHAR(100),
            magnitud_qubit FLOAT DEFAULT 1.6180,
            peso_relacional FLOAT DEFAULT 0.0,
            FOREIGN KEY (nodo_origen_id) REFERENCES enciclopedia_nodos(id) ON DELETE CASCADE,
            FOREIGN KEY (nodo_destino_id) REFERENCES enciclopedia_nodos(id) ON DELETE CASCADE
        );''')

        conn.commit()
        cur.close()
        conn.close()
        print("🛸 [Base de Datos RAILWAY]: Estructura de Red Semántica Verificada y Operativa.")
    except Exception as e:
        print(f"⚠️ Alerta de conexión con Railway: {e}")

# Ejecutamos la creación de tablas al iniciar
inicializar_base_de_datos_nucleo()

# --- CONSOLA DE INTERFAZ (LA MISMA QUE TE GUSTA, INTACTA Y MEJORADA) ---
@app.get("/nucleo-consola", response_class=HTMLResponse)
async def ver_consola_nucleo():
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
<button class="tab-btn" onclick="cambiarCanal('medicina', this)">🩺 Bio-Sur Chile</button>
</div>
<div id="console-log" class="console-log">
<div class="log-entry" style="color: #8892b0;">[SISTEMA]: Enciclopedia Relacional Doctorada V4. Motor híbrido flexible offline operativo.</div>
</div>
<div class="input-area">
<textarea id="idea-input" placeholder="Escribe tu petición o usa 'aprender: area=... concepto=... detalles=...'"></textarea>
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
if (data.status === 'success') {
log.innerHTML += `
<div class="log-entry" style="color: #00ffcc;">
${alertaHtml}
🧠 [Núcleo - Razonamiento Propio]: ${data.analisis_nucleo}
<div class="matrix-energy"> ↳ Registro: ${data.registro_id} | Energía: ${data.energia} Qubits | Modo: ${data.modo_operacion}</div>
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

# 🧠 MOTOR PRINCIPAL: LÓGICA DE RAZONAMIENTO PROPIO (SIN DEPENDENCIAS EXTERNAS)
@app.post("/nucleo-consulta")
async def consultar_nucleo(payload: dict):
    idea = payload.get("idea", "").strip()
    tema = payload.get("tema", "ingenieria")
    
    if not idea:
        return {
            "status": "error",
            "mensaje": "Transmisión vacía.",
            "analisis_nucleo": "",
            "registro_id": "ERR-000",
            "energia": 0.0,
            "modo_operacion": "ERROR"
        }

    modo_operacion = "AUTÓNOMO V2 - RAILWAY PRODUCCIÓN"
    respuesta_cuerpo = ""
    energia_emitida = 0.0
    registro_id = "000-0000"
    cantidad_nodos = 0
    areas_interes = ["informatica", "robotica", "electronica", "nanotecnologia", "neurociencia", "biorobotica", "medicina", "ancestral", "idiomas", "surchile"]

    try:
        # ✅ CONEXIÓN DIRECTA A TU BASE DE DATOS EN RAILWAY
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)

        # 📥 OPCIÓN 1: EL USUARIO ENSEÑA AL SISTEMA
        if idea.lower().startswith("aprender:"):
            partes = idea.split("|")
            area = tema
            concepto = "Nuevo Concepto"
            detalles = idea

            for parte in partes:
                if "area=" in parte.lower():
                    area = parte.split("=")[1].strip()
                if "concepto=" in parte.lower():
                    concepto = parte.split("=")[1].strip()
                if "detalles=" in parte.lower():
                    detalles = parte.split("=")[1].strip()

            # 📐 ASIGNACIÓN DE COORDENADAS EN ESPACIO VECTORIAL
            x = round(random.uniform(-10.0, 10.0), 4)
            y = round(random.uniform(-10.0, 10.0), 4)
            z = round(random.uniform(-10.0, 10.0), 4)

            cur.execute(
                'INSERT INTO enciclopedia_nodos (area, concepto, definicion_profunda) VALUES (%s, %s, %s)',
                (area, concepto, detalles)
            )
            conn.commit()
            nuevo_nodo_id = cur.lastrowid
            registro_id = f"ND-{nuevo_nodo_id}"

            # 🔍 INTELIGENCIA: CREACIÓN AUTOMÁTICA DE ENLACES LÓGICOS
            enlaces_creados = []
            for otra_area in areas_interes:
                if otra_area in detalles.lower() and otra_area != area:
                    cur.execute(
                        "SELECT id, concepto FROM enciclopedia_nodos WHERE area = %s LIMIT 1",
                        (otra_area,)
                    )
                    nodo_destino = cur.fetchone()
                    if nodo_destino:
                        cur.execute(
                            'INSERT INTO enciclopedia_enlaces (nodo_origen_id, nodo_destino_id, tipo_conexion, magnitud_qubit) VALUES (%s, %s, %s, %s)',
                            (nuevo_nodo_id, nodo_destino['id'], 'INTEGRACION_DOCTORAL', 1.6180)
                        )
                        conn.commit()
                        enlaces_creados.append(f"{otra_area.upper()} ↔ {nodo_destino['concepto']}")

            str_enlaces = ", ".join(enlaces_creados) if enlaces_creados else "Ninguno (Nodo aislado por ahora)"
            energia_emitida = round(1.6180 * (len(enlaces_creados) + 1), 4) if enlaces_creados else 1.0

            respuesta_cuerpo = f"""
✅ **[INGESTA COMPLETADA - RED ACTIVA]**

🧠 Nodo registrado en ÁREA: **{area.upper()}**
📌 Concepto: *{concepto}*
📍 Coordenadas asignadas: X:{x}, Y:{y}, Z:{z}

🔗 **Conexiones lógicas detectadas y creadas:**
{str_enlaces}

💾 Guardado en Base de Datos RAILWAY. Listo para ser cruzado.
            """

        # 📤 OPCIÓN 2: EL USUARIO PREGUNTA - MOTOR DE RAZONAMIENTO
        else:
            # PASO 1: ANÁLISIS SEMÁNTICO - Descomponer en palabras clave
            palabras_clave = [p.strip() for p in idea.lower().split() if len(p) > 3]
            if not palabras_clave:
                palabras_clave = [idea.lower()]

            # PASO 2: BÚSQUEDA INTELIGENTE EN LA RED DE CONOCIMIENTO
            condiciones = []
            valores_busqueda = []
            for palabra in palabras_clave:
                condiciones.append("(concepto LIKE %s OR definicion_profunda LIKE %s OR area LIKE %s)")
                valores_busqueda.extend([f"%{palabra}%", f"%{palabra}%", f"%{palabra}%"])

            consulta_sql = "SELECT * FROM enciclopedia_nodos WHERE " + " OR ".join(condiciones) + " ORDER BY fecha_indexacion DESC"
            cur.execute(consulta_sql, valores_busqueda)
            nodos_encontrados = cur.fetchall()
            cantidad_nodos = len(nodos_encontrados)

            # PASO 3: PROCESAMIENTO Y CRUCE DE DATOS
            if cantidad_nodos > 0:
                registro_id = f"QRY-{random.randint(100,999)}"
                ids_nodos = [n['id'] for n in nodos_encontrados]
                conexiones_totales = []

                # Buscar relaciones entre nodos
                if ids_nodos:
                    placeholders = ", ".join(["%s"] * len(ids_nodos))
                    cur.execute(f"""
                        SELECT e.tipo_conexion, destino.concepto, destino.area, e.magnitud_qubit
                        FROM enciclopedia_enlaces e
                        JOIN enciclopedia_nodos destino ON e.nodo_destino_id = destino.id
                        WHERE e.nodo_origen_id IN ({placeholders})
                    """, ids_nodos)
                    conexiones_totales = cur.fetchall()

                # 📊 CÁLCULO DE RELEVANCIA Y ENERGÍA
                energia_emitida = round((cantidad_nodos * 1.618) + (len(conexiones_totales) * 0.5), 4)

                # ✍️ GENERACIÓN DE RESPUESTA (LÓGICA PROPIA)
                if cantidad_nodos == 1:
                    # Respuesta exacta
                    nodo = nodos_encontrados[0]
                    respuesta_cuerpo = f"""
**[ANÁLISIS DIRECTO - NODO ÚNICO]** 🎯

He localizado el concepto exacto en mi base de datos (Railway):
📚 **{nodo['concepto'].upper()}**
🔖 Área de conocimiento: {nodo['area']}

📝 **Registro almacenado:**
{nodo['definicion_profunda']}
                    """
                    if conexiones_totales:
                        respuesta_cuerpo += "\n\n🔗 **Conceptos relacionados en mi red:**\n"
                        for con in conexiones_totales[:3]:
                            respuesta_cuerpo += f"  ↳ {con['tipo_conexion']}: {con['concepto']} ({con['area']})\n"

                else:
                    # Síntesis de múltiples nodos
                    areas_afectadas = list(set([n['area'] for n in nodos_encontrados]))
                    respuesta_cuerpo = f"""
**[SÍNTESIS RELACIONAL - {cantidad_nodos} NODOS CONECTADOS]** 🧠

Tu consulta cruza información de varias áreas de mi conocimiento:
🌐 {', '.join(areas_afectadas)}

📌 **Análisis generado por el Núcleo:**
He procesado los datos y he encontrado estas coincidencias principales:
"""
                    for n in nodos_encontrados[:3]:
                        respuesta_cuerpo += f"\n• **{n['concepto']}**: {n['definicion_profunda'][:150]}..."

                    if conexiones_totales:
                        respuesta_cuerpo += f"\n\n🔗 **Deducción automática:**\nExisten {len(conexiones_totales)} vínculos lógicos que conectan estos temas."

                    respuesta_cuerpo += "\n\n⚙️ *Interpretación realizada íntegramente con mi lógica. Datos alojados en Railway.*"

            else:
                # No hay datos -> Modo aprendizaje
                respuesta_cuerpo = """
**[CONOCIMIENTO NO ENCONTRADO]** ❓

No dispongo de registros en mi base de datos sobre este tema.

📘 **Modo de acción activado:**
Puedes enseñarme ahora mismo usando el formato:
`aprender: area= [Área] | concepto= [Nombre] | detalles= [Lo que quieras que aprenda]`

Yo lo indexaré, le asignaré coordenadas en mi espacio vectorial y guardaré todo en el servidor.
                """
                energia_emitida = 0.0

        # --- CIERRE DE CONEXIONES ---
        cur.close()
        conn.close()

        return {
            "status": "success",
            "analisis_nucleo": respuesta_cuerpo,
            "registro_id": registro_id,
            "energia": energia_emitida,
            "modo_operacion": modo_operacion
        }

    except Exception as e:
        return {
            "status": "error",
            "mensaje": f"Fallo en el procesamiento: {str(e)}",
            "analisis_nucleo": "",
            "registro_id": "ERR-001",
            "energia": 0.0,
            "modo_operacion": "ERROR"
        }

# --- EJECUTADOR DEL SERVIDOR (CONFIGURADO PARA RAILWAY) ---
if __name__ == "__main__":
    import uvicorn
    # ✅ Configuración optimizada para producción en Railway
    uvicorn.run(
        "nucleo_autonomo_v2:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        workers=1
    )