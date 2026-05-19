# ==================================================
# 🧠 NÚCLEO IA - ARCHIVO PRINCIPAL
# Versión: 2.0 | Modo: Público / Multiusuario
# Ruta: /terminal
# ==================================================

import os
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# ✅ Importamos la configuración y tablas que hicimos en la Parte 1
from memoria_database import get_db, iniciar_base_datos, EnciclopediaNodos, AREAS_CONOCIMIENTO
from memoria_nucleo import guardar_en_memoria, obtener_historial_nativo, obtener_ultimo_registro_diagnostico

# ==================================================
# ⚙️ CONFIGURACIÓN DEL SERVIDOR
# ==================================================
app = FastAPI(title="Núcleo IA", version="2.0")

# Permitimos acceso desde cualquier lugar (para que funcione en Railway y desde celulares)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================================================
# 🚀 ARRANQUE DEL SISTEMA
# ==================================================
@app.on_event("startup")
async def encender_sistema():
    """Se ejecuta al prender el servidor: conecta a la base de datos"""
    print("🛸 Iniciando secuencia de arranque NÚCLEO...")
    await iniciar_base_datos()
    print("✅ Sistema operativo. Esperando consultas.")
    print(f"📚 Áreas disponibles (para uso futuro): {', '.join(AREAS_CONOCIMIENTO)}")

# ==================================================
# 🗺️ RUTAS DE ACCESO (URL)
# ==================================================

# Redirige la dirección raíz hacia tu terminal
@app.get("/")
def ir_a_terminal():
    return RedirectResponse(url="/terminal")

# Muestra la interfaz gráfica
@app.get("/terminal", response_class=HTMLResponse)
def mostrar_consola():
    ruta_archivo = os.path.join(os.path.dirname(__file__), "index.html")
    return FileResponse(ruta_archivo)

# ==================================================
# 📥 ESTRUCTURA DE DATOS RECIBIDOS
# ==================================================
class EntradaUsuario(BaseModel):
    mensaje: str # Lo que escribe cualquier persona

# ==================================================
# 🧠 LÓGICA PRINCIPAL: GUARDAR - BUSCAR - RESPONDER
# ==================================================
@app.post("/nucleo-procesar")
async def procesar_entrada(datos: EntradaUsuario, db: AsyncSession = Depends(get_db)):
    texto_recibido = datos.mensaje.strip()

    # --------------------------------------------------
    # MODO 1: ENSEÑAR / GUARDAR INFORMACIÓN
    # Si el usuario escribe "Algo --- Explicación", se guarda en la base
    # --------------------------------------------------
    if "---" in texto_recibido:
        try:
            # Separamos lo que se va a guardar
            partes = texto_recibido.split("---", 1)
            tema_a_guardar = partes[0].strip()
            contenido_a_guardar = partes[1].strip()

            # 📝 Guardamos en la tabla principal
            nuevo_conocimiento = EnciclopediaNodos(
                area="general", # Por ahora general, luego activamos clasificación automática
                tema=tema_a_guardar,
                contenido=contenido_a_guardar,
                requisitos="" # Aquí irán los requisitos cuando avancemos
            )
            db.add(nuevo_conocimiento)
            await db.commit()
            await db.refresh(nuevo_conocimiento)

            # Guardamos también en memoria temporal para recordar el hilo de la conversación
            guardar_en_memoria("publico", texto_recibido, f"Información guardada: {tema_a_guardar}")

            return {
                "respuesta": f"✅ **GUARDADO CORRECTAMENTE**\n\n"
                             f"📌 Tema: {tema_a_guardar}\n"
                             f"💾 ID Registro: {nuevo_conocimiento.id}\n"
                             f"ℹ️ Esta información está disponible para todos los usuarios.",
                "estado": "exitoso"
            }

        except Exception as error_guardado:
            return {"respuesta": f"❌ Error al guardar: {str(error_guardado)}", "estado": "error"}

    # --------------------------------------------------
    # MODO 2: CONSULTAR / BUSCAR RESPUESTA
    # Si el usuario escribe cualquier cosa, buscamos en la base
    # --------------------------------------------------
    else:
        try:
            # 🔎 Buscamos coincidencias en lo que ya hemos aprendido
            # Busca en todo el contenido y temas, sin importar quién lo guardó
            busqueda = select(EnciclopediaNodos).where(
                EnciclopediaNodos.tema.ilike(f"%{texto_recibido}%")
            ).order_by(EnciclopediaNodos.fecha_guardado.desc()).limit(1)

            resultado = await db.execute(busqueda)
            dato_encontrado = resultado.scalar_one_or_none()

            if dato_encontrado:
                # Guardamos esta consulta en memoria
                guardar_en_memoria("publico", texto_recibido, dato_encontrado.contenido)

                return {
                    "respuesta": f"🧠 **NÚCLEO:**\n\n{dato_encontrado.contenido}",
                    "estado": "encontrado"
                }
            else:
                # Si no sabe, explica cómo enseñarle
                guardar_en_memoria("publico", texto_recibido, "Sin información")

                return {
                    "respuesta": f"❌ **No tengo información sobre:** '{texto_recibido}'\n\n"
                                 f"💡 **Para enseñarme**, escribe así:\n"
                                 f"`{texto_recibido} --- Escribe aquí toda la explicación, código o conocimiento...`",
                    "estado": "sin_datos"
                }

        except Exception as error_consulta:
            return {"respuesta": f"⚠️ Error en la consulta: {str(error_consulta)}", "estado": "error"}

# ==================================================
# 🚀 LEVANTAR SERVIDOR (COMPATIBLE RAILWAY)
# ==================================================
if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=puerto, reload=False)