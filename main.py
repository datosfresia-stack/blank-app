from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

# 📥 Importamos nuestros módulos (Rutas y funciones 100% corregidas)
from memoria_database import get_db, init_db, MatrizConocimiento
from memoria_nucleo import guardar_en_memoria, obtener_memoria

# 🚀 INICIO DEL SISTEMA
app = FastAPI(title="NUCLEO AUTÓNOMO | BASE MARIADB", version="2.0")

# 🧠 LÓGICA DE RESPUESTA Y CLASIFICACIÓN
def procesar_informacion(mensaje: str, canal: str):
    """
    Procesa el mensaje y lo clasifica automáticamente según el canal o palabras clave
    Categorías definidas: LAB | CINE | AUTOEVOLUCION
    """
    msg = mensaje.lower()

    # 📌 CLASIFICACIÓN PRINCIPAL SEGÚN CATEGORÍA
    if canal.upper() == "LAB" or "ingenieria" in msg or "codigo" in msg or "lab" in msg:
        categoria = "LAB"
        if "resonancia" in msg:
            return categoria, "🔄 RESONANCIA ACTIVADA: Conectando lógica y estructuras. Información reforzada en LAB."
        elif "estado" in msg:
            return categoria, "📊 ESTADO LAB: Sistemas operativos, código estable y estructuras optimizadas."
        else:
            return categoria, f"⚙️ [LAB] → Procesado y guardado: '{mensaje}'."

    elif canal.upper() == "CINE" or "pelicula" in msg or "cine" in msg or "historia" in msg or "trama" in msg:
        categoria = "CINE"
        if "resumen" in msg or "de qué trata" in msg:
            return categoria, "🎬 [CINE] → Analizando narrativa, personajes y estructura de la historia..."
        elif "recomienda" in msg or "ver" in msg:
            return categoria, "🎬 [CINE] → Base de datos de historias consultada. Información procesada."
        else:
            return categoria, f"🎬 [CINE] → Procesado y guardado: '{mensaje}'."

    elif canal.upper() == "AUTOEVOLUCION" or "aprender" in msg or "mejorar" in msg or "memoria" in msg or "evolucion" in msg:
        categoria = "AUTOEVOLUCION"
        if "recuerdas" in msg:
            return categoria, f"🧠 [AUTOEVOLUCION] → MEMORIA: {obtener_memoria()}"
        elif "quién eres" in msg or "qué eres" in msg:
            return categoria, "🧠 [AUTOEVOLUCION] → Soy NÚCLEO, sistema autónomo en constante evolución. Proceso, aprendo y almaceno información."
        elif "estado" in msg:
            return categoria, "🧠 [AUTOEVOLUCION] → Evolución activa. Memoria integrada y base de datos sincronizada."
        else:
            return categoria, f"🧠 [AUTOEVOLUCION] → Aprendido y guardado en núcleo: '{mensaje}'."

    # 📂 SI NO COINCIDE, VA A GENERAL (por seguridad)
    else:
        categoria = "GENERAL"
        return categoria, f"📁 [GENERAL] → Procesado y guardado: '{mensaje}'."

# 🖥️ RUTAS WEB (FUNCIONAN EN AMBAS DIRECCIONES)
@app.get("/", response_class=HTMLResponse)
@app.get("/nucleo-consola", response_class=HTMLResponse)
async def cargar_consola():
    """Carga la pantalla principal en ambas direcciones"""
    with open("index.html", "r", encoding="utf-8") as archivo:
        contenido = archivo.read()
    return HTMLResponse(content=contenido)

# 📡 ESTRUCTURA DE DATOS QUE LLEGA DE LA CONSOLA
class DatosEntrada(BaseModel):
    mensaje: str
    canal: str  # Aquí definimos si viene LAB, CINE o AUTOEVOLUCION
    # 🚀 PROCESAMIENTO PRINCIPAL Y CONEXIÓN A BASE DE DATOS
@app.post("/transmitir")
async def recibir_y_guardar(datos: DatosEntrada, db: AsyncSession = Depends(get_db)):
    """
    Recibe la información desde la consola:
    1. La clasifica en LAB / CINE / AUTOEVOLUCION
    2. La guarda en memoria interna
    3. La guarda en la Base de Datos MariaDB en su pestaña correspondiente
    """

    # Paso 1: Procesamos y clasificamos automáticamente
    categoria, respuesta = procesar_informacion(datos.mensaje, datos.canal)

    # Paso 2: Guardamos en la memoria interna del sistema
    guardar_en_memoria(datos.canal, datos.mensaje, respuesta)

    # Paso 3: Guardamos en MariaDB (Tabla: conocimiento | Columnas: categoria, concepto, detalles)
    try:
        nuevo_registro = MatrizConocimiento(
            categoria = categoria,       # Se guarda exactamente: LAB, CINE, AUTOEVOLUCION o GENERAL
            concepto = datos.mensaje,    # Lo que escribiste
            detalles = respuesta         # Lo que respondió el sistema
        )
        db.add(nuevo_registro)
        await db.commit()  # Guardado físico en la base

        estado_bd = f"✅ GUARDADO EN BD: Pestaña {categoria}"

    except Exception as error_bd:
        estado_bd = f"❌ ERROR BD: No se pudo guardar -> {str(error_bd)}"

    # Devolvemos todo a la pantalla
    return {
        "respuesta": respuesta,
        "categoria": categoria,
        "estado_bd": estado_bd
    }

# ⚡ ARRANQUE Y SINCRONIZACIÓN DE LA BASE
@app.on_event("startup")
async def arrancar_sistema():
    """Al encender, conecta y crea las tablas si no existen"""
    try:
        await init_db()
        print("✅ CONEXIÓN MARIADB: ESTABLECIDA | TABLAS SINCRONIZADAS")
    except Exception as e:
        print(f"❌ ERROR CONEXIÓN: {str(e)}")

# 🔧 EJECUCIÓN LOCAL (Para cuando corres en tu PC)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)