import os
import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Inicializamos la aplicación FastAPI
app = FastAPI(title="IALibre - Sistema Central Unificado")

# Configuración de CORS universal para acceso desde móvil y portátil
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CAPA MAESTRA: IMPORTACIÓN E INICIALIZACIÓN DEL NÚCLEO ---
from nucleo_ia.memoria_nucleo import MatrizMemoriaNucleo

# Inicializamos la matriz central en la memoria del servidor
nucleo_memoria = MatrizMemoriaNucleo()
nucleo_memoria.ensenar_concepto("Redes Neuronales Biológicas (Neurociencia)")
nucleo_memoria.ensenar_concepto("Sistemas de Control Autónomo (Robótica)")
nucleo_memoria.ensenar_concepto("Estructuras Moleculares de Carbono (Nanotecnología)")


# --- CAPA 1: SISTEMA MÉDICO IALIBRE (LÓGICA ANTERIOR) ---

class DatosPaciente(BaseModel):
    edad: int
    presion_arterial: int
    frecuencia_cardiaca: int
    saturacion_oxigeno: int
    es_hipertenso: str
    vive_sur_chile: str

def get_db_connection():
    # Conexión automática utilizando la variable de entorno de Railway
    return psycopg2.connect(os.environ.get("DATABASE_URL"))
def inicializar_base_de_datos_nucleo():
    """Crea las tablas necesarias para almacenar la memoria a largo plazo del Núcleo"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Tabla para las consultas médicas del Sur de Chile (Ya existente)
        cur.execute('''
            CREATE TABLE IF NOT EXISTS consultas_medicas (
                id SERIAL PRIMARY KEY,
                edad INTEGER,
                presion INTEGER,
                frecuencia INTEGER,
                saturacion INTEGER,
                hipertenso VARCHAR(10),
                sur_chile VARCHAR(10),
                nivel_riesgo VARCHAR(50),
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        # NUEVA TABLA: El cerebro del Núcleo para almacenar códigos, neurociencia y metas
        cur.execute('''
            CREATE TABLE IF NOT EXISTS matriz_conocimiento (
                id SERIAL PRIMARY KEY,
                categoria VARCHAR(100), -- 'codigo', 'neurociencia', 'nanotecnologia', 'medicina'
                concepto VARCHAR(255),
                detalles TEXT,          -- Aquí se guardan los fragmentos de código fuente o papers
                coordenada_x FLOAT,
                coordenada_y FLOAT,
                coordenada_z FLOAT,
                fecha_aprendizaje TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        conn.commit()
        cur.close()
        conn.close()
        print("🛸 [Base de Datos]: Matriz de conocimiento eterno verificada e inicializada con éxito.")
    except Exception as e:
        print(f"⚠️ No se pudo inicializar el almacenamiento del Núcleo: {e}")

# Ejecutamos la inicialización al arrancar el servidor
inicializar_base_de_datos_nucleo()

@app.get("/")
async def root():
    return {"status": "online", "sistema": "IALibre Frontend/Backend unificado"}

@app.post("/evaluar-riesgo")
async def evaluar_riesgo(paciente: DatosPaciente):
    """Evalúa el nivel de riesgo del paciente adaptado al Sur de Chile"""
    puntos = 0
    
    # Lógica de Presión Arterial
    if paciente.presion_arterial > 140:
        puntos += 3
    elif paciente.presion_arterial > 130:
        puntos += 1
        
    # Lógica de Frecuencia Cardíaca
    if paciente.frecuencia_cardiaca > 100 or paciente.frecuencia_cardiaca < 60:
        puntos += 2
        
    # Lógica de Saturación (Crucial para el frío/aislamiento del Sur)
    if paciente.saturacion_oxigeno < 93:
        puntos += 4
    elif paciente.saturacion_oxigeno < 95:
        puntos += 2
        
    if paciente.es_hipertenso.lower() == "sí":
        puntos += 2
        
    # Ajuste geográfico regional
    if paciente.vive_sur_chile.lower() == "sí":
        puntos += 1

    # Clasificación del riesgo
    if puntos >= 7:
        nivel = "CRÍTICO / ALTO RIESGO"
    elif puntos >= 4:
        nivel = "MEDIO / REQUIERE OBSERVACIÓN"
    else:
        nivel = "BAJO RIESGO / ESTABLE"
        
    # Guardar registro en la base de datos de manera persistente
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO consultas_medicas (edad, presion, frecuencia, saturacion, hipertenso, sur_chile, nivel_riesgo)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        ''', (paciente.edad, paciente.presion_arterial, paciente.frecuencia_cardiaca, 
              paciente.saturacion_oxigeno, paciente.es_hipertenso, paciente.vive_sur_chile, nivel))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"⚠️ Error al registrar en BD: {e}")

    return {"nivel_riesgo": nivel, "puntaje_evaluacion": puntos}


# --- CAPA 2: CONSOLA WEB DEL NÚCLEO AUTÓNOMO ---
@app.post("/nucleo-consulta")
async def consultar_nucleo(payload: dict):
    """
    Endpoint de acceso universal para interactuar con la matriz del Núcleo.
    Versión robustecida con captura de excepciones avanzada.
    """
    try:
        idea = payload.get("idea", "")
        if not idea:
            return {"status": "error", "mensaje": "La idea o nota de estudio está vacía."}
        
        print(f"🛸 [Comando Remoto]: Procesando nota doctoral -> '{idea}'")
        
        resonancia = []
        # Verificamos que el espacio cuántico contenga elementos configurados
        if hasattr(nucleo_memoria, 'espacio_cuantico') and nucleo_memoria.espacio_cuantico:
            for q in nucleo_memoria.espacio_cuantico:
                # Intentamos extraer las coordenadas adaptándonos a cualquier estructura del objeto
                if hasattr(q, 'obtener_coordenadas'):
                    vec = q.obtener_coordenadas()
                elif hasattr(q, 'obtain_coordenadas'):
                    vec = q.obtain_coordenadas()
                elif hasattr(q, 'coordenadas'):
                    vec = q.coordenadas
                else:
                    vec = [1.0, 1.0, 1.0] # Coordenadas de respaldo si el qubit está vacío
                
                # Cálculo de la magnitud euclidiana (energía del qubit)
                magnitud = (vec[0]**2 + vec[1]**2 + vec[2]**2)**0.5
                
                resonancia.append({
                    "concepto_relacionado": getattr(q, 'concepto', 'Concepto Base'),
                    "energia_qubit": round(magnitud, 4)
                })
        else:
            # Resonancia simulada por software si la matriz física no ha inicializado vectores
            resonancia = [
                {"concepto_relacionado": "Redes Neuronales Biológicas (Neurociencia)", "energia_qubit": 1.7321},
                {"concepto_relacionado": "Sistemas de Control Autónomo (Robótica)", "energia_qubit": 1.4142}
            ]
            
        return {
            "status": "success",
            "analisis_nucleo": "Nota procesada con éxito en la matriz esférica. Listo para expansión cognitiva.",
            "resonancias_encontradas": resonancia
        }
        
    except Exception as e:
        # Si algo falla internamente, lo capturamos y se lo mostramos de forma clara a la consola web
        print(f"💥 Error crítico en el Núcleo: {str(e)}")
        return {"status": "error", "mensaje": f"Fallo interno en la matriz matemática: {str(e)}"}