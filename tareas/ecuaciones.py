import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Parámetros del modelo
densidad_inicial = 220 # Densidad inicial de vehículos
tiempo = np.linspace(0, 300, 1000) # Tiempo de simulación
velocidad = 2 # Velocidad de los vehículos
capacidad_carretera = 500 # Capacidad de la carretera, asumida para este ejemplo
tasa_crecimiento = 0.1 # Tasa de crecimiento, asumida para este ejemplo

# Función que define la ecuación diferencial
def modelo_tráfico(N, t):
    return tasa_crecimiento * N * (1 - N / capacidad_carretera)

# Resolviendo la ecuación diferencial
solucion = odeint(modelo_tráfico, densidad_inicial, tiempo)

# Graficando la solución
plt.plot(tiempo, solucion)
plt.xlabel('Tiempo (segundos)')
plt.ylabel('Densidad de vehículos')
plt.title('Modelo de tráfico vehicular')
plt.show()
