import math
import random

class QubitSimulado:
    """Simula el estado de un Qubit usando ángulos de rotación (Theta y Phi)"""
    def __init__(self, concepto: str):
        self.concepto = concepto
        # Inicializamos los estados cuánticos en la esfera de Bloch de forma aleatoria
        self.theta = random.uniform(0, math.pi)
        self.phi = random.uniform(0, 2 * math.pi)
        
    def obtener_coordenadas(self):
        # Transmuta los ángulos en un vector tridimensional (X, Y, Z)
        x = math.sin(self.theta) * math.cos(self.phi)
        y = math.sin(self.theta) * math.sin(self.phi)
        z = math.cos(self.theta)
        return [x, y, z]

class MatrizMemoriaNucleo:
    def __init__(self):
        self.espacio_cuantico = []

    def ensenar_concepto(self, concepto: str):
        """Registra un nuevo conocimiento en la matriz del Núcleo"""
        nuevo_qubit = QubitSimulado(concepto)
        self.espacio_cuantico.append(nuevo_qubit)
        print(f"🧠 [Núcleo]: Concepto '{concepto}' codificado en la matriz esférica.")

    def buscar_similitud(self, idea_buscada: str):
        """Busca relaciones matriciales entre conceptos"""
        if not self.espacio_cuantico:
            return "La matriz de memoria está vacía."
        
        # Simulamos un entrelazamiento básico comparando distancias vectoriales
        print(f"🔍 [Núcleo]: Escaneando resonancia para: '{idea_buscada}'...")
        for q in self.espacio_cuantico:
            vec = q.obtener_coordenadas()
            # Cálculo de la magnitud del vector base
            magnitud = math.sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)
            print(f"   ↳ Resonancia con '{q.concepto}': {magnitud:.4f} Qubits de energía.")

# --- PRUEBA LOCAL DEL SISTEMA ---
if __name__ == "__main__":
    print("🛸 Inicializando el Núcleo Autónomo...")
    nucleo_memoria = MatrizMemoriaNucleo()
    
    # Le enseñamos las 4 áreas doctorales al Núcleo
    nucleo_memoria.ensenar_concepto("Redes Neuronales Biológicas (Neurociencia)")
    nucleo_memoria.ensenar_concepto("Sistemas de Control Autónomo (Robótica)")
    nucleo_memoria.ensenar_concepto("Estructuras Moleculares de Carbono (Nanotecnología)")
    
    print("-" * 50)
    # Ejecutamos un escaneo de prueba
    nucleo_memoria.buscar_similitud("Simulación cuántica cerebral")