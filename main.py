import os
import smtplib
from email.message import EmailMessage
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import chat_medico 

app = FastAPI()

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir tus rutas existentes
app.include_router(chat_medico.router)

@app.get("/")
def root():
    return {"status": "Núcleo y ChatMédico operativos"}

# --- NUEVA RUTA CORREGIDA PARA FASTAPI ---
@app.post("/guardar-paciente")
async def guardar_paciente(request: Request):
    data = await request.json()
    
    # Lógica de prioridad
    diagnostico = data.get('diagnostico', '').lower()
    peticion = data.get('peticion_contacto', '').lower()
    prioridad = "ALTA" if any(p in diagnostico or p in peticion for p in ['cancer', 'urgente', 'dolor']) else "NORMAL"
    
    msg = EmailMessage()
    msg['Subject'] = f"[{prioridad}] Nueva Solicitud IALIBRE - {data.get('nombre')}"
    msg['From'] = os.getenv('EMAIL_USER')
    msg['To'] = 'ialibre@outlook.com'
    
    cuerpo = f"""
    Nueva solicitud recibida desde IALIBRE:
    
    - Nombre: {data.get('nombre')}
    - Edad: {data.get('edad')}
    - Domicilio: {data.get('domicilio')}
    - Teléfono: {data.get('telefono')}
    - Diagnóstico: {data.get('diagnostico')}
    - Necesidad: {data.get('necesidad')}
    - Detalles: {data.get('peticion_contacto')}
    
    Prioridad detectada: {prioridad}
    """
    msg.set_content(cuerpo)
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))
            smtp.send_message(msg)
        return {"status": "success", "mensaje": "Tu mensaje ha sido enviado. Pronto te contactaremos."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "mensaje": str(e)})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
