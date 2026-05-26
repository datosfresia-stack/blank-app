from fastapi import APIRouter, Request

# 1. Definimos el router
router = APIRouter()

def analizar_lenguaje_oculto(nota, metadatos):
    alertas = []
    # Usamos .get para que no falle si falta información
    largo = metadatos.get('largoTexto', 0)
    complejidad = metadatos.get('complejidad', 5)
    
    if largo > 50 and complejidad < 2:
        alertas.append("Posible fatiga cognitiva o confusión leve detectada.")
    
    nota_lower = nota.lower()
    if "no sé" in nota_lower and "ayuda" in nota_lower:
        alertas.append("Estado de estrés agudo - Requiere derivación prioritaria.")
        
    return alertas

# 2. Convertimos tu lógica en un endpoint (ruta)
@router.post("/evaluar-riesgo")
async def evaluar_riesgo(request: Request):
    data = await request.json()
    nota = data.get('nota_usuario', '')
    metadatos = data.get('metadatos_escritura', {})
    
    alertas = analizar_lenguaje_oculto(nota, metadatos)
    
    return {
        "analisis": "Tu orientación basada en tus parámetros...",
        "alerta_oculta": alertas if alertas else None,
        "acciones": ["Recomendación médica", "Soporte emocional"]
    }
