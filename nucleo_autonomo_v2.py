import os
import sys
import random
import math
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import json

# ✅ RUTA CORREGIDA PARA CONECTAR CON TU BASE DE DATOS EN RAILWAY
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database import get_db_connection

# 🛸 INICIALIZACIÓN DEL NÚCLEO - VERSIÓN AUTÓNOMA V2
# Conectado a Base de Datos RAILWAY - Enlace Público
app = FastAPI(title="IALibre Núcleo Autónomo V2 - Producción")

def inicializar_base_de_datos_nucleo():
    """Crea la estructura completa de tablas en la base de datos de Railway"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Tabla de Datos Biomédicos
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

        # Tabla de Conocimiento General
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

        # Tabla de Relaciones entre conocimientos
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
        print("🛸 [Base de Datos RAILWAY]: Estructura verificada y operativa.")
    except Exception as e:
        print(f"⚠️ Alerta de conexión: {e}")

# Ejecutamos la creación de tablas al iniciar
inicializar_base_de_datos_nucleo()

# --- INTERFAZ PRINCIPAL CON LAS 4 PESTAÑAS ---
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
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    body {
        background: linear-gradient(135deg, #0a0f1d 0%, #111a2e 100%);
        color: #00ffcc;
        min-height: 100vh;
        padding: 20px;
    }
    .contenedor-principal {
        max-width: 900px;
        margin: 0 auto;
        background: #111a2e;
        border: 2px solid #00ffcc;
        border-radius: 12px;
        box-shadow: 0 0 30px rgba(0,255,204,0.2);
        overflow: hidden;
    }
    /* ESTILO DE LAS PESTAÑAS */
    .barra-pestanas {
        display: flex;
        background: #070c16;
        border-bottom: 2px solid #00ffcc;
        flex-wrap: wrap;
    }
    .boton-pestana {
        flex: 1;
        min-width: 120px;
        background: none;
        border: none;
        color: #8892b0;
        padding: 15px 10px;
        cursor: pointer;
        font-size: 0.95em;
        font-weight: 600;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .boton-pestana:hover {
        color: #00ffcc;
        background: rgba(0,255,204,0.05);
    }
    .boton-pestana.activa {
        color: #0a0f1d;
        background: #00ffcc;
    }
    /* ÁREA DE MENSAJES */
    .area-mensajes {
        height: 400px;
        padding: 25px;
        overflow-y: auto;
        background: #070c16;
        border-bottom: 1px solid #00ffcc;
        line-height: 1.6;
        font-size: 1em;
    }
    .mensaje {
        margin-bottom: 20px;
        padding: 15px;
        border-radius: 8px;
        max-width: 90%;
    }
    .mensaje-usuario {
        background: rgba(0,255,204,0.1);
        border-left: 3px solid #00ffcc;
        margin-left: auto;
        color: #ffffff;
    }
    .mensaje-nucleo {
        background: rgba(136, 146, 176, 0.1);
        border-left: 3px solid #ff007f;
        margin-right: auto;
        color: #e0e0e0;
    }
    .mensaje-sistema {
        background: rgba(255, 170, 0, 0.05);
        border-left: 3px solid #ffaa00;
        text-align: center;
        color: #ffaa00;
        font-style: italic;
    }
    /* ÁREA DE ENTRADA */
    .area-entrada {
        padding: 20px;
        background: #111a2e;
    }
    textarea {
        width: 100%;
        height: 100px;
        background: #070c16;
        color: #ffffff;
        border: 2px solid #00ffcc;
        border-radius: 8px;
        padding: 15px;
        font-size: 1em;
        resize: vertical;
        transition: all 0.3s ease;
    }
    textarea:focus {
        outline: none;
        box-shadow: 0 0 15px rgba(0,255,204,0.3);
    }
    .boton-enviar {
        width: 100%;
        background: #00ffcc;
        color: #0a0f1d;
        border: none;
        padding: 15px;
        font-size: 1.1em;
        font-weight: bold;
        border-radius: 8px;
        margin-top: 15px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .boton-enviar:hover {
        background: #00b38f;
        box-shadow: 0 0 20px rgba(0,255,204,0.4);
    }
    .info-sistema {
        text-align: center;
        padding: 10px;
        color: #8892b0;
        font-size: 0.9em;
        border-top: 1px solid #00ffcc;
    }
    /* ESTILOS ESPECIALES PARA CADA PESTAÑA */
    .lab .mensaje-nucleo {
        border-color: #00ff88;
    }
    .cine .mensaje-nucleo {
        border-color: #ff007f;
    }
    .evolucion .mensaje-nucleo {
        border-color: #ffaa00;
    }
    .chat .mensaje-nucleo {
        border-color: #0088ff;
    }
</style>
</head>
<body>
    <div class="contenedor-principal">
        <!-- BARRA DE PESTAÑAS -->
        <div class="barra-pestanas">
            <button class="boton-pestana activa" onclick="cambiarPestana('lab', this)">💻 Lab</button>
            <button class="boton-pestana" onclick="cambiarPestana('cine', this)">🎬 Cine Matrix</button>
            <button class="boton-pestana" onclick="cambiarPestana('evolucion', this)">🧬 Auto Evolución</button>
            <button class="boton-pestana" onclick="cambiarPestana('chat', this)">💬 Chat</button>
        </div>

        <!-- ÁREA DE MENSAJES -->
        <div id="area-mensajes" class="area-mensajes lab">
            <div class="mensaje mensaje-sistema">[SISTEMA]: Enciclopedia Relacional Doctorada V4. Motor híbrido flexible operativo.</div>
            <div class="mensaje mensaje-nucleo">🧠 [Núcleo]: ¡Hola! Soy tu asistente inteligente. Elige una pestaña para empezar:<br>
            • Lab: Para ayuda con códigos, programación y temas técnicos<br>
            • Cine Matrix: Para información sobre películas y temas relacionados<br>
            • Auto Evolución: Para ver cómo funciona mi aprendizaje y crecimiento<br>
            • Chat: Para charlas sencillas, claras y fáciles de entender</div>
        </div>

        <!-- ÁREA DE ENTRADA -->
        <div class="area-entrada">
            <textarea id="entrada-usuario" placeholder="Escribe aquí tu mensaje o consulta..."></textarea>
            <button class="boton-enviar" onclick="enviarMensaje()">Enviar mensaje</button>
        </div>

        <div class="info-sistema">
            ↳ Registro Relacional: 1 | Resonancia: 1.618 Qubits | Modo: STANDARD
        </div>
    </div>

    <script>
        let pestanaActual = 'lab';

        // CAMBIAR DE PESTAÑA
        function cambiarPestana(nuevaPestana, elemento) {
            pestanaActual = nuevaPestana;
            
            // Quitar clase activa de todos los botones
            document.querySelectorAll('.boton-pestana').forEach(boton => {
                boton.classList.remove('activa');
            });
            
            // Poner clase activa al botón seleccionado
            elemento.classList.add('activa');
            
            // Cambiar estilo del área de mensajes
            const areaMensajes = document.getElementById('area-mensajes');
            areaMensajes.className = `area-mensajes ${nuevaPestana}`;
            
            // Mostrar mensaje de bienvenida según la pestaña
            let bienvenida = '';
            switch(nuevaPestana) {
                case 'lab':
                    bienvenida = '🧠 [Núcleo - Lab]: Bienvenido al espacio de desarrollo. Aquí te ayudo con códigos, estructuras, algoritmos y todo lo relacionado con programación. Pregunta lo que necesites.';
                    break;
                case 'cine':
                    bienvenida = '🧠 [Núcleo - Cine Matrix]: Bienvenido al espacio cinematográfico. Aquí tienes información sobre películas, historias, tramas y temas relacionados con el mundo del cine y la ciencia ficción.';
                    break;
                case 'evolucion':
                    bienvenida = '🧠 [Núcleo - Auto Evolución]: Bienvenido al espacio de crecimiento. Aquí puedes ver cómo aprendo, cómo guardo información y cómo voy mejorando con cada consulta que me haces.';
                    break;
                case 'chat':
                    bienvenida = '🧠 [Núcleo - Chat]: Bienvenido al espacio de charla. Aquí hablamos con lenguaje sencillo, claro y fácil de entender. Sin términos complicados, solo información útil para todos.';
                    break;
            }
            
            agregarMensaje(bienvenida, 'nucleo');
        }

        // AGREGAR MENSAJE A LA PANTALLA
        function agregarMensaje(texto, tipo) {
            const contenedor = document.getElementById('area-mensajes');
            const divMensaje = document.createElement('div');
            divMensaje.className = `mensaje mensaje-${tipo}`;
            divMensaje.innerHTML = texto.replace(/\n/g, '<br>');
            contenedor.appendChild(divMensaje);
            contenedor.scrollTop = contenedor.scrollHeight;
        }

        // ENVIAR MENSAJE AL SERVIDOR
        async function enviarMensaje() {
            const entrada = document.getElementById('entrada-usuario');
            const texto = entrada.value.trim();
            
            if (!texto) return;

            // Mostrar mensaje del usuario
            agregarMensaje(texto, 'usuario');
            entrada.value = '';

            try {
                // Enviar consulta al backend
                const respuesta = await fetch('/nucleo-consulta', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        idea: texto,
                        tema: pestanaActual
                    })
                });

                const datos = await respuesta.json();

                // Mostrar respuesta según la pestaña
                let respuestaMostrar = datos.analisis_nucleo;

                // Si es pestaña Chat, hacemos que el lenguaje sea más sencillo
                if (pestanaActual === 'chat') {
                    respuestaMostrar = simplificarLenguaje(respuestaMostrar);
                }

                agregarMensaje(respuestaMostrar, 'nucleo');

            } catch (error) {
                agregarMensaje('⚠️ Lo siento, hubo un problema al procesar tu mensaje. Inténtalo de nuevo más tarde.', 'sistema');
                console.error(error);
            }
        }

        // FUNCIÓN PARA SIMPLIFICAR EL LENGUAJE EN LA PESTAÑA CHAT
        function simplificarLenguaje(texto) {
            // Cambiamos términos técnicos por palabras más sencillas
            const cambios = {
                'análisis': 'explicación',
                'algoritmo': 'forma de hacer las cosas',
                'estructura': 'organización',
                'base de datos': 'archivo de información',
                'función': 'herramienta',
                'código': 'instrucciones',
                'programación': 'creación de programas',
                'sistema': 'conjunto de herramientas',
                'consulta': 'pregunta',
                'registro': 'información guardada',
                'conexión': 'unión o relación',
                'reconocimiento': 'identificación',
                'procesamiento': 'tratamiento de información'
            };

            let textoSencillo = texto;
            for (const [original, sustitucion] of Object.entries(cambios)) {
                const expresionRegular = new RegExp(original, 'gi');
                textoSencillo = textoSencillo.replace(expresionRegular, sustitucion);
            }
            // También reducimos un poco los párrafos para que sea más amigable
            textoSencillo = textoSencillo.replace(/\n\n/g, '\n');
            textoSencillo = textoSencillo.replace(/\*\*/g, '');
            return textoSencillo;
        }

        // Enviar mensaje al presionar Enter
        document.getElementById('entrada-usuario').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                enviarMensaje();
            }
        });
    </script>
</body>
</html>
    """
    return HTMLResponse(content=contenido_html, status_code=200)

# --- LÓGICA DEL SERVIDOR Y RESPUESTAS ---
@app.post("/nucleo-consulta")
async def consultar_nucleo(payload: dict):
    idea = payload.get("idea", "").strip()
    tema = payload.get("tema", "lab")

    if not idea:
        return {
            "status": "error",
            "analisis_nucleo": "Por favor escribe algo para poder ayudarte.",
            "registro_id": "ERR-000",
            "energia": 0.0,
            "modo_operacion": "ERROR"
        }

    modo_operacion = "SISTEMA UNIVERSAL OPERATIVO"
    respuesta_principal = ""
    registro_id = "REG-" + str(random.randint(10000, 99999))
    energia = round(random.uniform(1.0, 10.0), 2)

    try:
        # Conexión a la base de datos
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)

        # ==============================================
        # LÓGICA SEGÚN LA PESTAÑA SELECCIONADA
        # ==============================================

        # 1. PESTAÑA LAB: Ayuda con códigos y temas técnicos
        if tema == "lab":
            if idea.lower().startswith("aprender:"):
                # Guardar nueva información
                partes = idea.split("|")
                area = "informatica"
                concepto = idea
                descripcion = idea
                requisitos = ""

                for p in partes:
                    if "area=" in p.lower():
                        area = p.split("=")[1].strip()
                    if "concepto=" in p.lower():
                        concepto = p.split("=")[1].strip()
                    if "detalles=" in p.lower() or "descripcion=" in p.lower():
                        descripcion = p.split("=")[1].strip()
                    if "requisitos=" in p.lower():
                        requisitos = p.split("=")[1].strip()

                # Guardar en base de datos
                cur.execute('''
                    INSERT INTO enciclopedia_nodos (area, concepto, definicion_profunda, requisitos_previos)
                    VALUES (%s, %s, %s, %s)
                ''', (area, concepto, descripcion, requisitos))
                conn.commit()

                respuesta_principal = f"""
✅ **¡Información guardada correctamente!**

📌 Datos registrados:
• Área: {area}
• Tema: {concepto}
• Detalles: {descripcion[:150]}...

💾 Ahora esta información está disponible para futuras consultas.
                """

            else:
                # Buscar información existente
                palabras = idea.lower().split()
                condiciones = []
                valores = []

                for p in palabras:
                    if len(p) > 2:
                        condiciones.append("(concepto LIKE %s OR definicion_profunda LIKE %s OR area LIKE %s)")
                        valores.extend([f"%{p}%", f"%{p}%", f"%{p}%"])

                if condiciones:
                    consulta = f"SELECT * FROM enciclopedia_nodos WHERE {' OR '.join(condiciones)} LIMIT 10"
                    cur.execute(consulta, valores)
                    resultados = cur.fetchall()

                    if resultados:
                        respuesta_principal = f"""
📚 **Resultados encontrados para: {idea}**

He encontrado {len(resultados)} registros relacionados con tu búsqueda:
"""
                        for res in resultados:
                            respuesta_principal += f"""
🔹 **{res['concepto']}**
📍 Área: {res['area']}
📝 Descripción: {res['definicion_profunda'][:200]}...
"""
                    else:
                        respuesta_principal = f"""
🔍 **No encontré información sobre "{idea}"**

Puedes enseñarme esta información usando el formato:
`aprender: area= [tema] | concepto= [nombre] | detalles= [lo que quieras que sepa]`

Así guardaré todo y podré responderte la próxima vez.
"""
                else:
                    respuesta_principal = "Por favor escribe algo más específico para poder buscar o guardar información."

        # 2. PESTAÑA CINE MATRIX: Información sobre películas y temas relacionados
        elif tema == "cine":
            palabras = idea.lower().split()
            condiciones = []
            valores = []

            for p in palabras:
                if len(p) > 2:
                    condiciones.append("(concepto LIKE %s OR definicion_profunda LIKE %s OR area LIKE %s)")
                    valores.extend([f"%{p}%", f"%{p}%", f"%{p}%"])

            if condiciones:
                consulta = f"""
                    SELECT * FROM enciclopedia_nodos 
                    WHERE area LIKE '%cine%' OR {' OR '.join(condiciones)} 
                    LIMIT 10
                """
                cur.execute(consulta, valores)
                resultados = cur.fetchall()

                if resultados:
                    respuesta_principal = f"""
🎬 **Información sobre: {idea}**

Aquí tienes lo que sé sobre este tema:
"""
                    for res in resultados:
                        respuesta_principal += f"""
• **{res['concepto']}**
  {res['definicion_profunda'][:250]}...
"""
                else:
                    respuesta_principal = f"""
🎬 **Sobre "{idea}"**

Esta es una área muy interesante. Puedo buscar información sobre películas, directores, historias, tramas y todo lo relacionado con el mundo del cine.
Escribe el nombre de lo que quieras saber y te daré todos los detalles.
"""
            else:
                respuesta_principal = "¿De qué película o tema quieres información? Dime el nombre y te cuento todo lo que sé."

        # 3. PESTAÑA AUTO EVOLUCIÓN: Información sobre cómo funciona el sistema
        elif tema == "evolucion":
            if "cómo funcionas" in idea.lower() or "cómo aprendes" in idea.lower():
                respuesta_principal = """
🧬 **¿Cómo funciono y cómo aprendo?**

Soy un sistema que guarda toda la información que me das en una base de datos.
Cada vez que me haces una pregunta o me enseñas algo, voy guardando nuevos conocimientos.

Cuando me haces una consulta:
1. Busco en mi archivo de información lo que se relaciona con tu pregunta
2. Uno los datos que encuentro para darte una respuesta clara
3. Voy guardando todas las interacciones para ir creciendo cada vez más

Cuanta más información me des, más completo seré y mejor podré ayudarte en todos tus campos de interés.
"""
            elif "cómo creces" in idea.lower() or "cómo mejoras" in idea.lower():
                respuesta_principal = """
📈 **¿Cómo voy creciendo y mejorando?**

Mi crecimiento se basa en 3 cosas principales:
• **Información que me das**: Cada nuevo dato que me enseñas se convierte en conocimiento para todos
• **Relaciones que encuentro**: Puedo ver cómo se conectan los temas entre sí, aunque sean de áreas diferentes
• **Tus consultas**: Cada pregunta me ayuda a entender qué es lo que más te interesa y cómo explicarlo mejor

Siempre estoy aprendiendo y actualizándome. Con el tiempo podré ayudarte en tareas más complejas y con mayor precisión.
"""
            else:
                respuesta_principal = """
🧬 **Espacio de Auto Evolución**

Aquí puedes conocer cómo funciona mi sistema, cómo aprendo, cómo guardo información y cómo voy mejorando con el tiempo.

Pregúntame cosas como:
• ¿Cómo funcionas?
• ¿Cómo aprendes?
• ¿Cómo creces?
• ¿Qué áreas conoces?

Y te explicaré todo detalladamente.
"""

        # 4. PESTAÑA CHAT: Lenguaje sencillo y fácil de entender
        elif tema == "chat":
            # En esta pestaña respondemos de forma clara, sin términos complicados
            if any(p in idea.lower() for p in ["hola", "buenos dias", "buenas", "qué tal"]):
                respuesta_principal = """
¡Hola! 👋 ¿Cómo estás? Me da mucho gusto hablar contigo.

Estoy aquí para ayudarte en lo que necesites. Puedes preguntarme sobre cualquier tema, contarme algo o decirme qué información quieres que guarde.

¿En qué te puedo colaborar hoy?
"""
            elif "gracias" in idea.lower():
                respuesta_principal = """
¡De nada! 😊 Me alegra mucho poder ayudarte.

Si necesitas algo más, aquí estaré. Solo dímelo.
"""
            elif "adios" in idea.lower() or "hasta luego" in idea.lower():
                respuesta_principal = """
¡Hasta luego! 👋 Que tengas un día maravilloso.

Cuando quieras volver a hablar conmigo, aquí estaré esperándote.
"""
            else:
                # Buscamos información general y la explicamos de forma sencilla
                palabras = idea.lower().split()
                condiciones = []
                valores = []

                for p in palabras:
                    if len(p) > 2:
                        condiciones.append("(concepto LIKE %s OR definicion_profunda LIKE %s)")
                        valores.extend([f"%{p}%", f"%{p}%", f"%{p}%"])

                if condiciones:
                    consulta = f"SELECT * FROM enciclopedia_nodos WHERE {' OR '.join(condiciones)} LIMIT 5"
                    cur.execute(consulta, valores)
                    resultados = cur.fetchall()

                    if resultados:
                        respuesta_principal = f"""
¡Claro que sí! Aquí te explico lo que sé sobre "{idea}":

"""
                        for res in resultados:
                            # Simplificamos el texto para que sea más fácil de entender
                            texto_sencillo = res['definicion_profunda']
                            texto_sencillo = texto_sencillo.replace("análisis", "explicación")
                            texto_sencillo = texto_sencillo.replace("algoritmo", "forma de hacer las cosas")
                            texto_sencillo = texto_sencillo.replace("estructura", "organización")
                            texto_sencillo = texto_sencillo.replace("función", "herramienta")
                            texto_sencillo = texto_sencillo.replace("código", "instrucciones")
                            texto_sencillo = texto_sencillo.replace("programación", "creación de programas")
                            texto_sencillo = texto_sencillo.replace("base de datos", "archivo de información")

                            respuesta_principal += f"📌 **{res['concepto']}**: {texto_sencillo[:250]}...\n\n"

                        respuesta_principal += """
Si quieres que te lo explique de otra forma o quieres saber más detalles, solo dímelo y te lo cuento con mucho gusto.
"""
                    else:
                        respuesta_principal = f"""
¡Muy buena pregunta! 😊 Sobre "{idea}" aún no tengo información guardada.

Pero puedes enseñarme lo que sabes, así lo guardaré y la próxima vez que me preguntes te podré dar todos los detalles.

Solo usa este formato:
`aprender: area= [de qué tema es] | concepto= [nombre] | detalles= [lo que quieras que sepa]`

Así lo tendré todo ordenado y listo para usarlo.
"""
                else:
                    respuesta_principal = """
¡Cuéntame! 😊 Dime qué quieres saber o de qué tema quieres que te hable.

Puedo explicarte cosas sobre:
• Tecnología y programación
• Cine y entretenimiento
• Cómo funciona este sistema
• Cualquier tema que te interese

Solo dímelo y te responderé con claridad.
"""

        # Cerrar conexión
        cur.close()
        conn.close()

        return {
            "status": "success",
            "analisis_nucleo": respuesta_principal,
            "registro_id": registro_id,
            "energia": energia,
            "modo_operacion": modo_operacion
        }

    except Exception as e:
        return {
            "status": "error",
            "analisis_nucleo": f"Lo siento, ocurrió un problema al procesar tu mensaje. Detalle: {str(e)}",
            "registro_id": "ERR-999",
            "energia": 0.0,
            "modo_operacion": "ERROR"
        }

# --- CONFIGURACIÓN PARA RAILWAY ---
if __name__ == "__main__":
    import uvicorn
    import os
    puerto = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "nucleo_autonomo_v2:app",
        host="0.0.0.0",
        port=puerto,
        reload=False
    )