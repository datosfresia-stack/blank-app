def analizar_lenguaje_oculto(nota, metadatos):
    # Detección de patrones de deterioro
    alertas = []
    
    # Si la complejidad es muy baja pero el texto es largo: posible fatiga cognitiva
    if metadatos['largoTexto'] > 50 and metadatos['complejidad'] < 2:
        alertas.append("Posible fatiga cognitiva o confusión leve detectada.")
    
    # Detección de lenguaje circular (repetición)
    if "no sé" in nota.lower() and "ayuda" in nota.lower():
        alertas.append("Estado de estrés agudo - Requiere derivación prioritaria.")
        
    return alertas

# En tu función principal:
def procesar_evaluacion(data):
    nota = data.get('nota_usuario', '')
    metadatos = data.get('metadatos_escritura', {})
    
    alertas = analizar_lenguaje_oculto(nota, metadatos)
    
    return {
        "analisis": "Tu orientación basada en tus parámetros...",
        "alerta_oculta": alertas if alertas else None,
        "acciones": [...]
    }
