import numpy as np

class RedNeuronal:
    def __init__(self):
        np.random.seed(1)
        self.pesos = 2 * np.random.random((3, 1)) - 1

    def sigmoide(self, x):
        return 1 / (1 + np.exp(-x))

    def derivada_sigmoide(self, x):
        return x * (1 - x)

    def entrenar(self, entradas, salidas, iteraciones):
        for _ in range(iteraciones):
            salida = self.pensar(entradas)
            error = salidas - salida
            ajustes = np.dot(entradas.T, error * self.derivada_sigmoide(salida))
            self.pesos += ajustes

    def pensar(self, entradas):
        entradas = entradas.astype(float)
        return self.sigmoide(np.dot(entradas, self.pesos))

# ------------------------------
# PROGRAMA PRINCIPAL
# ------------------------------
if __name__ == "__main__":
    # Crear la IA
    mi_ia = RedNeuronal()

    print("⚖️ Pesos iniciales (aleatorios):")
    print(mi_ia.pesos)

    # Datos para enseñar
    # Entradas
    entradas = np.array([
        [0, 0, 1],
        [1, 1, 1],
        [1, 0, 1],
        [0, 1, 1]
    ])
    
    # Salidas esperadas
    salidas = np.array([[0, 1, 1, 0]]).T

    # Entrenar
    mi_ia.entrenar(entradas, salidas, 10000)

    print("\n✅ Pesos después de aprender:")
    print(mi_ia.pesos)

    # Probar con datos nuevos
    print("\n🤔 Probando con [1, 0, 0]:")
    resultado = mi_ia.pensar(np.array([1, 0, 0]))
    print(resultado)
