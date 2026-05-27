from fastapi import APIRouter, Request
import csv
import os
from datetime import datetime

router = APIRouter()

@router.post("/guardar-laboral")
async def guardar_laboral(request: Request):
    data = await request.json()
    tipo = data.get("tipo")  # 'postulante' o 'empleador'
    archivo = "postulantes_laboral.csv" if tipo == "postulante" else "ofertas_laboral.csv"
    
    # Crear archivo con cabeceras si no existe
    if not os.path.exists(archivo):
        with open(archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if tipo == "postulante":
                writer.writerow(["Fecha", "Nombre", "Oficio", "Experiencia", "Contacto"])
            else:
                writer.writerow(["Fecha", "Empresa", "Rubro", "Cargo", "Requisitos", "Contacto"])

    # Guardar datos
    with open(archivo, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if tipo == "postulante":
            writer.writerow([datetime.now().strftime("%Y-%m-%d"), data['nombre'], data['oficio'], data['exp'], data['contacto']])
        else:
            writer.writerow([datetime.now().strftime("%Y-%m-%d"), data['nombre'], data['rubro'], data['cargo'], data['req'], data['contacto']])
            
    return {"status": "success"}
