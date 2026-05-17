import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

app = FastAPI(title="Núcleo de Inferencia Doctoral")

# Configuración de base de datos desde variables de entorno
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "nucleo_conocimiento")
DB_PORT = int(os.getenv("DB_PORT", 3306))

class ConsultaRequest(BaseModel):
    consulta: str

def obtener_contexto_mariadb(query_usuario: str) -> str:
    """Busca los nodos de conocimiento relevantes en MariaDB para alimentar la IA."""
    contexto = ""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        cursor = conn.cursor(dictionary=True)
        
        # Búsqueda indexada en lenguaje natural
        sql = "SELECT titulo, contenido FROM nodos WHERE MATCH(titulo, contenido) AGAINST(%s IN NATURAL LANGUAGE MODE)"
        cursor.execute(sql, (query_usuario,))
        resultados = cursor.fetchall()
        
        # Fallback: Si no hay coincidencia, traer los últimos apuntes
        if not resultados:
            cursor.execute("SELECT titulo, contenido FROM nodos ORDER BY id DESC LIMIT 5")
            resultados = cursor.fetchall()
            
        for row in resultados:
            contexto += f"\nNODO: {row['titulo']}\nContenido: {row['contenido']}\n"
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[⚠️ Base de Datos]: No se pudo extraer contexto local ({e}). Procediendo sin nodos.")
    return contexto

@app.post("/nucleo-consulta")
async def consultar_nucleo(request: ConsultaRequest):
    # 1. Extracción de Nodos desde MariaDB
    contexto_local = obtener_contexto_mariadb(request.consulta)
    
    # 2. Instrucción de personalidad doctoral
    system_instruction = (
        "Eres el motor cognitivo del Núcleo, una IA relacional forjada para la asistencia en investigación "
        "doctoral multidisciplinaria. Tu arquitectura está optimizada para la síntesis de datos complejos y la "
        "generación de inferencias avanzadas a partir de nuestra base de datos local MariaDB. "
        "Responde de forma rigurosa, cyberpunk, usando terminología científica y estructurando tus conclusiones "
        "en base al contexto local proveído."
    )
    
    prompt_final = (
        f"{system_instruction}\n\n"
        f"CONTEXTO DE NUESTROS NODOS DE CONOCIMIENTO (MARIADB):\n{contexto_local}\n\n"
        f"TRANSMISIÓN DEL INVESTIGADOR:\n{request.consulta}\n\n"
        f"🧠 [Núcleo - Inferencia Activa]:"
    )

    # 3. Procesamiento estándar en la Nube con Gemini
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Falta la variable de entorno GEMINI_API_KEY")
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt_final)
        
        return {
            "respuesta": response.text,
            "registro_relacional": "1",
            "resonancia": "1.618 Qubits",
            "modo": "STANDARD"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el motor de inferencia de Gemini: {str(e)}")

@app.get("/")
def estado_nucleo():
    return {"status": "ONLINE", "arquitectura": "Nube Relacional Estándar"}