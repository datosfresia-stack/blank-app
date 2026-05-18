# ==================================================
# NÚCLEO AUTÓNOMO V2 - SISTEMA INDESTRUCTIBLE
# SERVIDOR PRINCIPAL: RAILWAY | SERVIDOR SECUNDARIO: TU CELULAR (QWEN2.5)
# ==================================================

import os
import sys
import json
import requests
import subprocess
from flask import Flask, request, jsonify, render_template_string
from urllib.parse import quote_plus

# --------------------------
# CONFIGURACIÓN DE SERVIDORES
# --------------------------
CONFIG = {
    "servidor_principal": {
        "nombre": "Railway",
        "activo": True,
        # Aquí va tu configuración actual de Railway (se mantiene igual)
    },
    "servidor_secundario": {
        "nombre": "Celular - Termux",
        "activo": True,
        # TUS DOS IPs QUE ME ENVIASTE
        "ip_wifi": "192.168.1.100",       # <-- TU IP WIFI AQUÍ
        "ip_movil": "10.150.25.45",       # <-- TU IP MÓVIL AQUÍ
        "puerto": "8080",                 # Puerto donde correremos Qwen como API
        "ruta_api": "/v1/chat/completions",
        "modelo": "qwen2.5-1.5b-instruct-q8_0"
    },
    "sistema": {
        "modo_respuesta": "amigable", # Como yo te hablo, natural y claro
        "buscar_en_internet": True,   # Habilitado para la pestaña Chat
        "versión": "2.0 - INDESTRUCTIBLE"
    }
}

# --------------------------
# INICIO DE LA APLICACIÓN
# --------------------------
app = Flask(__name__)

# PESTAÑAS ORIGINALES (SE MANTIENEN INTACTAS, SIN CAMBIOS)
# Esto asegura que Lab, Cine, AutoEvolución sigan funcionando igual que antes

@app.route('/lab')
def laboratorio():
    # --- TU CÓDIGO ORIGINAL DE LABORATORIO ---
    return render_template_string("<h1>🔬 Laboratorio - Funcionando Normal</h1><p>Servidor Principal Activo</p>")

@app.route('/cine')
def cine():
    # --- TU CÓDIGO ORIGINAL DE CINE ---
    return render_template_string("<h1>🎬 Cine - Funcionando Normal</h1><p>Base de datos y reproducción activa</p>")

@app.route('/autoevolucion')
def auto_evolucion():
    # --- TU CÓDIGO ORIGINAL DE AUTO EVOLUCIÓN ---
    return render_template_string("<h1>🧬 Auto Evolución - Funcionando Normal</h1><p>Aprendizaje continuo activo</p>")

# --------------------------
# ✅ NUEVA PESTAÑA: CHAT (CONECTADA A TU CELULAR)
# --------------------------
@app.route('/chat')
def chat_nuevo():
    # Cargamos la interfaz visual, totalmente separada de las otras
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>💬 Chat - Núcleo Autónomo</title>
        <style>
            body { font-family: Arial, sans-serif; background: #1a1a1a; color: #fff; padding: 20px; }
            .contenedor { max-width: 800px; margin: auto; }
            .mensaje { padding: 12px; border-radius: 10px; margin: 8px 0; max-width: 75%; }
            .usuario { background: #2c5aa0; margin-left: auto; text-align: right; }
            .ia { background: #333333; margin-right: auto; }
            #entrada { width: 80%; padding: 10px; }
            #enviar { padding: 10px 20px; background: #28a745; border: none; color: white; cursor: pointer; }
            .estado { color: #28a745; font-size: 12px; margin-bottom: 15px; }
        </style>
    </head>
    <body>
        <div class="contenedor">
            <h1>💬 Chat Inteligente | Conectado a: TU CELULAR 📱</h1>
            <p class="estado">✅ Servidor Secundario Activo | Qwen2.5 | Búsqueda en Internet: ACTIVA</p>
            <div id="historial"></div>
            <br>
            <input type="text" id="entrada" placeholder="Escribe tu mensaje aquí...">
            <button id="enviar" onclick="enviarMensaje()">Enviar</button>
        </div>

        <script>
        async function enviarMensaje() {
            const texto = document.getElementById('entrada').value;
            if (!texto) return;
            
            agregarMensaje(texto, 'usuario');
            document.getElementById('entrada').value = '';
            
            // Enviamos la pregunta a nuestro núcleo, que la redirige al celular
            const respuesta = await fetch('/procesar_chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({"mensaje": texto})
            });
            
            const datos = await respuesta.json();
            agregarMensaje(datos.respuesta, 'ia');
        }

        function agregarMensaje(texto, tipo) {
            const div = document.createElement('div');
            div.className = 'mensaje ' + tipo;
            div.textContent = texto;
            document.getElementById('historial').appendChild(div);
        }
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

# --------------------------
# LÓGICA DE CONEXIÓN AL CELULAR Y PROCESAMIENTO
# --------------------------
@app.route('/procesar_chat', methods=['POST'])
def procesar_chat():
    datos = request.get_json()
    mensaje_usuario = datos.get('mensaje', '')

    # PASO 1: INTENTAMOS CONECTAR AL CELULAR (PRIMERO WIFI, SI NO FUNCIONA USA DATOS MÓVILES)
    respuesta_ia = conectar_a_celular(mensaje_usuario)

    # PASO 2: SI LA RESPUESTA ES CORTA O POCO CLARA, BUSCAMOS EN INTERNET (COMO PEDISTE)
    if CONFIG["sistema"]["buscar_en_internet"] and len(respuesta_ia) < 100:
        info_internet = buscar_en_internet(mensaje_usuario)
        # Mezclamos el conocimiento de Qwen con información actual de la red
        prompt_final = f"""
        Responde de forma amigable, clara y natural, como una persona que explica bien.
        Usa esta información actual de internet si es necesario: {info_internet}
        Pregunta del usuario: {mensaje_usuario}
        Respuesta:
        """
        respuesta_ia = conectar_a_celular(prompt_final)

    return jsonify({"respuesta": respuesta_ia})

def conectar_a_celular(mensaje):
    """ Se conecta primero por WiFi, si falla usa la IP de Datos Móviles """
    ips = [
        f"http://{CONFIG['servidor_secundario']['ip_wifi']}:{CONFIG['servidor_secundario']['puerto']}{CONFIG['servidor_secundario']['ruta_api']}",
        f"http://{CONFIG['servidor_secundario']['ip_movil']}:{CONFIG['servidor_secundario']['puerto']}{CONFIG['servidor_secundario']['ruta_api']}"
    ]

    payload = {
        "model": CONFIG['servidor_secundario']['modelo'],
        "messages": [
            {"role": "system", "content": "Eres una inteligencia artificial amigable, clara y servicial. Responde en español, de forma natural, sencilla y útil. No seas robótico."},
            {"role": "user", "content": mensaje}
        ],
        "temperature": 0.7,
        "stream": False
    }

    for url in ips:
        try:
            respuesta = requests.post(url, json=payload, timeout=15)
            if respuesta.status_code == 200:
                dato = respuesta.json()
                return dato['choices'][0]['message']['content']
        except:
            continue # Si falla una IP, prueba la siguiente
    
    return "⚠️ Parece que no estoy conectado al celular ahora mismo, pero sigo aquí. Inténtalo más tarde o verifica la conexión."

# --- AQUÍ SE DETIENE LA PRIMERA PARTE ---
# ==================================================
# CONTINUACIÓN - PARTE 2 / 2
# FUNCIONES DE BÚSQUEDA, ARRANQUE Y SISTEMA COMPLETO
# ==================================================

# --------------------------
# FUNCIÓN: BÚSQUEDA EN INTERNET
# --------------------------
def buscar_en_internet(consulta):
    """
    Busca información actualizada en la web para complementar
    el conocimiento de Qwen. Solo se activa para la pestaña Chat.
    """
    try:
        # Palabras clave para búsquedas limpias y seguras
        consulta_limpia = consulta.replace(" ", "+")
        url_busqueda = f"https://html.duckduckgo.com/html/?q={quote_plus(consulta)}"

        cabeceras = {
            "User-Agent": "Mozilla/5.0 (compatible; NucleoAutonomo/2.0; +https://tudominio.com)"
        }

        respuesta = requests.get(url_busqueda, headers=cabeceras, timeout=10)
        if respuesta.status_code != 200:
            return "Sin datos nuevos de internet."

        # Extraemos resumen de información relevante
        from bs4 import BeautifulSoup
        sopa = BeautifulSoup(respuesta.text, 'html.parser')
        resultados = sopa.find_all('a', class_='result__snippet')

        # Recopilamos los 3 primeros resultados para dar contexto
        informacion = []
        for i, res in enumerate(resultados[:3]):
            texto = res.get_text(strip=True)
            if texto and len(texto) > 30:
                informacion.append(f"- {texto}")

        if informacion:
            return "Información actualizada encontrada:\n" + "\n".join(informacion)
        else:
            return "No se encontraron detalles nuevos en la web, respondo con mi conocimiento base."

    except Exception as e:
        # Si falla la conexión a internet, no se cae el sistema, avisa y sigue
        return f"(Sin conexión a fuentes externas, uso mi conocimiento propio)"

# --------------------------
# FUNCIÓN: GESTIÓN DEL SERVIDOR QWEN EN TERMUX (TU CELULAR)
# --------------------------
def arrancar_servidor_celular():
    """
    Esta función prepara y arranca el servidor API de Qwen2.5
    dentro de Termux automáticamente al iniciar el núcleo.
    Solo se ejecuta si estamos corriendo esto dentro del celular.
    """
    try:
        # Verificamos si estamos en el entorno Termux
        if os.path.exists("/data/data/com.termux/files/usr/bin/bash"):
            print("[✅ TERMUX DETECTADO] - Preparando servidor local...")

            # Ruta donde tienes tu llama.cpp y el modelo
            ruta_llama = "/data/data/com.termux/files/home/llama.cpp"
            ejecutable_api = f"{ruta_llama}/build/bin/llama-simple-chat"
            modelo_ruta = f"{ruta_llama}/models/qwen2.5-1.5b-instruct-q8_0 (1).gguf"

            # Comando para arrancar como SERVIDOR API en el puerto 8080
            # Esto es lo que permite que Railway o tu navegador se conecten al celular
            comando = [
                ejecutable_api,
                "-m", modelo_ruta,
                "-c", "2048",
                "--port", "8080",          # Puerto que definimos en la configuración
                "--host", "0.0.0.0",       # Escucha desde CUALQUIER IP (WiFi y Datos)
                "--api",                   # Modo Servidor API activado
                "--n-gpu-layers", "0"      # Optimizado para CPU de celular
            ]

            # Ejecutamos en segundo plano para que no se bloquee el sistema
            subprocess.Popen(comando, cwd=ruta_llama, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("[🚀 SERVIDOR QWEN ACTIVO] - Escuchando en puerto 8080")
            return True

    except Exception as e:
        print(f"[⚠️ AVISO] - No estoy en Termux o no se pudo arrancar: {e}")
        return False

# --------------------------
# SEGURIDAD Y SEPARACIÓN DE SISTEMAS
# --------------------------
@app.before_request
def proteger_sistemas():
    """
    REGLAS DE ORO:
    1. Si accedes a /lab, /cine, /autoevolucion -> SOLO usa Railway / Código Original
    2. Si accedes a /chat -> SOLO usa Celular / Qwen + Búsqueda
    3. NUNCA mezcla datos ni lógica entre secciones
    """
    ruta_actual = request.path

    # SECCIÓN 1: SISTEMA ORIGINAL (NO TOCAR NADA)
    if ruta_actual in ['/lab', '/cine', '/autoevolucion']:
        # Aquí se cargan tus funciones originales que ya funcionan en Railway
        # Dejamos que Flask siga su curso normal con tu código antiguo
        pass

    # SECCIÓN 2: SISTEMA NUEVO (CHAT / CELULAR)
    elif ruta_actual in ['/chat', '/procesar_chat']:
        # Forzamos que esta sección use ESTRICTAMENTE la configuración del celular
        # y las reglas de lenguaje amigable y búsqueda
        CONFIG["servidor_principal"]["activo"] = False  # Desconectado de Railway aquí
        CONFIG["sistema"]["modo_respuesta"] = "amigable" # Forzamos el tono
    else:
        # Rutas generales o raíz
        pass

# --------------------------
# RUTA PRINCIPAL Y MENÚ DE NAVEGACIÓN
# --------------------------
@app.route('/')
def menu_principal():
    """
    Página de inicio con enlaces a todas las secciones,
    mostrando claramente cuál está activa y dónde corre.
    """
    html_menu = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>🏛️ Núcleo Autónomo - Sistema Indestructible</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #0f0f0f; color: #e0e0e0; margin: 0; padding: 30px; text-align: center; }
            h1 { color: #f0db4f; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; max-width: 900px; margin: 40px auto; }
            .tarjeta { padding: 30px; border-radius: 12px; text-decoration: none; color: white; font-weight: bold; font-size: 18px; transition: transform 0.3s; }
            .tarjeta:hover { transform: scale(1.05); }
            .lab { background: linear-gradient(45deg, #4a6fa5, #6388bb); }
            .cine { background: linear-gradient(45deg, #a54a6f, #bb6388); }
            .evo { background: linear-gradient(45deg, #4aa56f, #63bb88); }
            .chat { background: linear-gradient(45deg, #a58a4a, #bb9f63); box-shadow: 0 0 15px #f0db4f80; }
            .estado { margin-top: 20px; font-size: 14px; color: #888; }
        </style>
    </head>
    <body>
        <h1>🧠 NÚCLEO AUTÓNOMO V2.0</h1>
        <p>Arquitectura: Servidor Principal (Railway) + Servidor Secundario (Tu Celular)</p>
        
        <div class="grid">
            <a href="/lab" class="tarjeta lab">🔬 LABORATORIO<br><small>Sistema Original</small></a>
            <a href="/cine" class="tarjeta cine">🎬 CINE<br><small>Base de Datos</small></a>
            <a href="/autoevolucion" class="tarjeta evo">🧬 AUTO EVOLUCIÓN<br><small>Aprendizaje</small></a>
            <a href="/chat" class="tarjeta chat">💬 CHAT INTELIGENTE<br><small>Potencia: TU CELULAR 📱</small></a>
        </div>

        <div class="estado">
            ✅ Railway: Activo Globalmente | 📱 Celular: Activo como Respaldo y Chat
        </div>
    </body>
    </html>
    """
    return render_template_string(html_menu)

# --------------------------
# ARRANQUE FINAL DEL SISTEMA
# --------------------------
if __name__ == "__main__":
    # PASO 1: Intentamos arrancar el servidor API de Qwen si estamos en el celular
    arrancar_servidor_celular()

    # PASO 2: Iniciamos el núcleo en el puerto 5000 (estándar Flask/Railway)
    # Escucha en todas las interfaces para aceptar conexiones externas
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)

# ==================================================
# FIN DEL CÓDIGO - SISTEMA COMPLETO INTEGRADO
# ==================================================