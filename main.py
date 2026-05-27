import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importamos las dos ramas
import chat_medico
import chat_laboral

app = FastAPI()

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registramos las rutas de ambas ramas
app.include_router(chat_medico.router)
app.include_router(chat_laboral.router)

@app.get("/")
def root():
    return {"status": "Núcleo IALibre en funcionamiento - Rama Salud y Laboral activas"}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    uvicorn.run(app, host='0.0.0.0', port=port)
    @app.get("/descargar-postulantes")
def descargar_postulantes():
    return FileResponse("postulantes_laboral.csv", media_type='text/csv', filename="postulantes_laboral.csv")

@app.get("/descargar-ofertas")
def descargar_ofertas():
    return FileResponse("ofertas_laboral.csv", media_type='text/csv', filename="ofertas_laboral.csv")
