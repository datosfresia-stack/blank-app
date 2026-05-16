import os
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
import google.generativeai as genai

app = FastAPI(title="Núcleo de Inferencia Doctoral - Resiliencia Híbrida")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "nucleo_conocimiento")
DB_PORT = int(os.getenv("DB_PORT", 3306))

class ConsultaRequest(BaseModel):
    consulta: str

def obtener_contexto_mariadb(query_usuario: str) -> str:
    contexto = ""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, port=DB_PORT
        )
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT titulo, contenido FROM nodos WHERE MATCH(titulo, contenido) AGAINST(%s IN NATURAL LANGUAGE MODE)"
        cursor.execute(sql, (query_usuario,))
        resultados = cursor.fetchall()
        
        if not resultados:
            cursor.execute("SELECT titulo, contenido FROM nodos ORDER BY id DESC LIMIT 5")
            resultados = cursor.fetchall()
            
        for row in resultados:
            contexto += f"\nNODO: {row['titulo']}\nContenido: {row['contenido']}\n"
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[⚠️ DB]: Falló extracción de contexto ({e})")
    return contexto

@app.post("/nucleo-consulta")
async def consultar_nucleo(request: ConsultaRequest):
    contexto_local = obtener_contexto_mariadb(request.consulta)
    
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

    api_key = os.getenv("GEMINI_API_KEY")
    
    # --- NIVEL 1: NUBE (STANDARD) ---
    if api_key:
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
        except Exception as nube_error:
            print(f"[⚠️ Nube]: Error en Gemini: {nube_error}. Conmutando a local...")

    # --- NIVEL 2: MODO AVIÓN (OLLAMA + QWEN LOCAL) ---
    try:
        url_ollama = "http://localhost:11434/api/generate"
        payload = {
            "model": "qwen2.5:1.5b",
            "prompt": prompt_final,
            "stream": False
        }
        async with httpx.AsyncClient(timeout=15.0) as client:
            res_ollama = await client.post(url_ollama, json=payload)
            if res_ollama.status_code == 200:
                data = res_ollama.json()
                return {
                    "respuesta": data.get("response", ""),
                    "registro_relacional": "1",
                    "resonancia": "1.618 Qubits",
                    "modo": "OFFLINE_LOCAL"
                }
    except Exception as local_error:
        print(f"[🚨 Local]: Ollama offline o no responde ({local_error})")

    raise HTTPException(
        status_code=503, 
        detail="Fallo multicanal: Nube inaccesible y motor local apagado."
    )

@app.get("/")
def estado_nucleo():
    return {"status": "ONLINE", "arquitectura": "Hibrida (Cloud/Offline)"}