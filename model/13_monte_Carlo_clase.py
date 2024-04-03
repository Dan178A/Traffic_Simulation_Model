import numpy as np
import matplotlib.pyplot as plt

# Parámetros
lambda_ = 2  # media de tiempo entre llegadas, en minutos
mu = 1  # media de tiempo de servicio, en minutos
sigma = 0.5  # desviación estándar del tiempo de servicio en minutos
N = 1000  # número de simulaciones

tiempo_espera = np.zeros(N)

for i in range(N):
    llegadas = np.cumsum(np.random.exponential(lambda_, 100))  # 100 vehículos
    inicio_servicio = max(0, llegadas[0] - np.random.normal(mu, sigma))
    fin_servicio = inicio_servicio + np.random.normal(mu, sigma)
    espera = inicio_servicio - llegadas[0]

    for j in range(1, len(llegadas)):
        inicio_servicio = max(fin_servicio, llegadas[j])
        fin_servicio = inicio_servicio + np.random.normal(mu, sigma)
        espera += inicio_servicio - llegadas[j]

    tiempo_espera[i] = espera / len(llegadas)

media_espera = np.mean(tiempo_espera)
desviacion_espera = np.std(tiempo_espera)

# Gráfico de los tiempos de espera
plt.hist(tiempo_espera, bins=20)
plt.xlabel('Tiempo Medio de espera (Minutos)')
plt.ylabel('Frecuencia')
plt.title('Distribución del tiempo medio de espera en la interacción')
plt.show()