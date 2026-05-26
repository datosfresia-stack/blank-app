import os
import csv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime

app = FastAPI()

# Configuración CORS para permitir tu WordPress
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Nombre del archivo donde se guardarán los pacientes
ARCHIVO_PACIENTES = "base_datos_pacientes.csv"

# Inicializar el archivo con cabeceras si no existe
if not os.path.exists(ARCHIVO_PACIENTES):
    with open(ARCHIVO_PACIENTES, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Fecha", "Nombre", "Edad", "Diagnóstico", "Necesidad", "Prioridad"])

@app.get("/")
def root():
    return {"status": "Núcleo operativo - Base de datos activa"}

@app.post("/guardar-paciente")
async def guardar_paciente(request: Request):
    try:
        data = await request.json()
        
        # Lógica de prioridad
        diag = data.get('diagnostico', '').lower()
        prioridad = "ALTA" if any(x in diag for x in ['cancer', 'urgente', 'dolor']) else "NORMAL"
        
        # Registrar en el archivo CSV local
        nueva_fila = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data.get('nombre'),
            data.get('edad'),
            data.get('diagnostico'),
            data.get('peticion_contacto'),
            prioridad
        ]
        
        with open(ARCHIVO_PACIENTES, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(nueva_fila)
            
        return {"status": "success", "mensaje": "Paciente guardado en base de datos local"}
        
    except Exception as e:
        return {"status": "error", "detalle": str(e)}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
