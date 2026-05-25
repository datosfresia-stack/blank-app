from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import chat_medico # Importamos tu nuevo módulo médico

app = FastAPI()

# CORS configurado desde el inicio
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas de tus módulos
app.include_router(chat_medico.router)

@app.get("/")
def root():
    return {"status": "Núcleo y ChatMédico operativos"}
