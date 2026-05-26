import os
import csv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse # Importante para la descarga
from datetime import datetime
import uvicorn

app = FastAPI()

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ARCHIVO_PACIENTES = "pacientes_ialibre.csv"

# Asegurar que el archivo tenga cabeceras al iniciar
if not os.path.exists(ARCHIVO_PACIENTES):
    with open(ARCHIVO_PACIENTES, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Fecha", "Nombre", "Domicilio", "Telefono", "Edad", "Peso", "Presion", "Diagnostico", "Necesidad", "Detalle", "Prioridad"])

@app.get("/")
def root():
    return {"status": "Núcleo operativo"}

# --- AQUÍ VA LO QUE ME PEDISTE ---

@app.post("/guardar-paciente")
async def guardar_paciente(request: Request):
    data = await request.json()
    
    # Lógica simple de prioridad
    diag = data.get('diagnostico', '').lower()
    prioridad = "ALTA" if any(x in diag for x in ['cancer', 'urgente', 'dolor']) else "NORMAL"
    
    fila = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data.get('nombre'), data.get('domicilio'), data.get('telefono'),
        data.get('edad'), data.get('peso'), data.get('presion'),
        data.get('diagnostico'), data.get('necesidad'), data.get('detalle_peticion'),
        prioridad
    ]
    
    with open(ARCHIVO_PACIENTES, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(fila)
        
    return {"status": "success"}

@app.get("/descargar-datos")
def descargar_datos():
    # Esto te permite bajar el archivo desde el navegador
    return FileResponse(ARCHIVO_PACIENTES, media_type='text/csv', filename="pacientes_ialibre.csv")

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
