import os
import csv
from fastapi import APIRouter, Request
from datetime import datetime

router = APIRouter()
ARCHIVO_CHAT = "historial_chat.csv"

# Inicializar archivo de historial si no existe
if not os.path.exists(ARCHIVO_CHAT):
    with open(ARCHIVO_CHAT, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Fecha", "Nombre_Usuario", "Nota", "Alertas", "Acciones"])

def analizar_lenguaje_oculto(nota, metadatos):
    alertas = []
    largo = metadatos.get('largoTexto', 0)
    complejidad = metadatos.get('complejidad', 5)
    
    if largo > 50 and complejidad < 2:
        alertas.append("Posible fatiga cognitiva o confusión leve detectada.")
    
    nota_lower = nota.lower()
    if "no sé" in nota_lower and "ayuda" in nota_lower:
        alertas.append("Estado de estrés agudo - Requiere derivación prioritaria.")
        
    return alertas

@router.post("/evaluar-riesgo")
async def evaluar_riesgo(request: Request):
    data = await request.json()
    usuario = data.get('nombre_usuario', 'Anónimo')
    nota = data.get('nota_usuario', '')
    metadatos = data.get('metadatos_escritura', {})
    
    alertas = analizar_lenguaje_oculto(nota, metadatos)
    acciones = ["Recomendación médica", "Soporte emocional"]
    
    # GUARDAR REGISTRO EN CSV
    registro = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        usuario,
        nota,
        " | ".join(alertas) if alertas else "Ninguna",
        " | ".join(acciones)
    ]
    
    with open(ARCHIVO_CHAT, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(registro)
    
    return {
        "analisis": "Tu orientación basada en tus parámetros...",
        "alerta_oculta": alertas if alertas else None,
        "acciones": acciones
    }
