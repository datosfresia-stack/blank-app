import numpy as np

class RedNeuronal:
    def __init__(self, num_entradas=3):
        # Usamos una semilla para que el resultado sea repetible
        np.random.seed(42)
        # Inicialización de pesos más eficiente (distribución normal)
        self.pesos = np.random.normal(0, 1, (num_entradas, 1))
        # Tasa de aprendizaje: controla qué tan rápido cambia lo que sabe
        self.tasa_aprendizaje = 0.1

    def sigmoide(self, x):
        """Función de activación: comprime el valor entre 0 y 1"""
        return 1 / (1 + np.exp(-x))

    def derivada_sigmoide(self, x):
        """Se usa para calcular la dirección del ajuste de los pesos"""
        return x * (1 - x)

    def entrenar(self, entradas, salidas, iteraciones):
        for epoca in range(iteraciones):
            # 1. Forward Pass: La IA intenta adivinar
            prediccion = self.pensar(entradas)
            
            # 2. Calcular el error
            error = salidas - prediccion
            
            # 3. Backpropagation: Calcular cuánto hay que ajustar los pesos
            # Multiplicamos el error por la pendiente de la sigmoide
            gradiente = error * self.derivada_sigmoide(prediccion)
            ajustes = np.dot(entradas.T, gradiente)
            
            # 4. Actualizar los pesos con la tasa de aprendizaje
            self.pesos += ajustes * self.tasa_aprendizaje
            
            # Mostrar progreso cada 2000 pasos
            if epoca % 2000 == 0:
                error_medio = np.mean(np.abs(error))
                print(f"Época {epoca}: Error medio = {error_medio:.5f}")

    def pensar(self, entradas):
        """Procesa las entradas a través de la red"""
        # Aseguramos que los datos sean flotantes
        entradas = np.array(entradas, dtype=float)
        return self.sigmoide(np.dot(entradas, self.pesos))

# ------------------------------
# PROGRAMA PRINCIPAL
# ------------------------------
if __name__ == "__main__":
    # 1. Inicializar la IA
    ia_fresia = RedNeuronal(num_entradas=3)

    # 2. Datos de entrenamiento (Patrón: El primer número manda la salida)
    entradas = np.array([
        [0, 0, 1],
        [1, 1, 1],
        [1, 0, 1],
        [0, 1, 1]
    ])
    salidas = np.array([[0, 1, 1, 0]]).T

    print("🚀 Iniciando entrenamiento...")
    ia_fresia.entrenar(entradas, salidas, 10000)

    print("\n🧠 IA Entrenada.")
    
    # 3. Pruebas con datos que NUNCA vio
    print("\n--- TEST DE INTELIGENCIA ---")
    
    # Caso A: El primer número es 1, debería dar cercano a 1
    test_1 = np.array([1, 0, 0])
    print(f"Entrada [1, 0, 0] -> Predicción: {ia_fresia.pensar(test_1)[0]:.4f}")

    # Caso B: El primer número es 0, debería dar cercano a 0
    test_2 = np.array([0, 1, 0])
    print(f"Entrada [0, 1, 0] -> Predicción: {ia_fresia.pensar(test_2)[0]:.4f}")
    
