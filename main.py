import os
import smtplib
from email.message import EmailMessage
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Configuración CORS para permitir tu WordPress
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Núcleo operativo"}

# Ponemos la lógica directamente aquí para evitar errores de importación
@app.post("/guardar-paciente")
async def guardar_paciente(request: Request):
    data = await request.json()
    
    # Lógica de prioridad
    diag = data.get('diagnostico', '').lower()
    prioridad = "ALTA" if any(x in diag for x in ['cancer', 'urgente', 'dolor']) else "NORMAL"
    
    msg = EmailMessage()
    msg['Subject'] = f"[{prioridad}] Nueva Solicitud IALIBRE - {data.get('nombre')}"
    msg['From'] = os.getenv('EMAIL_USER')
    msg['To'] = 'ialibre@outlook.com'
    
    msg.set_content(f"""
    Nombre: {data.get('nombre')}
    Edad: {data.get('edad')}
    Diagnóstico: {data.get('diagnostico')}
    Necesidad: {data.get('peticion_contacto')}
    Prioridad: {prioridad}
    """)
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))
            smtp.send_message(msg)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "detalle": str(e)}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
