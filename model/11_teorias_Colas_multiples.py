import numpy as np
import matplotlib.pyplot as plt

# Parámetros del sistema
_lambda = 6  # Tasa de llegada de vehículos
mu = 5  # Tasa de servicio
c = 4  # Número de servidores
K = 10  # Número máximo de vehículos en el sistema

# Probabilidad de que el sistema esté en estado i
pi = np.zeros(K+1)
pi[0] = 1
for i in range(1, c+1):
    pi[i] = (_lambda/mu)**i * pi[0]
for i in range(c+1, K+1):
    pi[i] = (_lambda/(c*mu))**i * pi[0]
pi[0] = 1 / np.sum(pi)

# Número promedio de vehículos en el sistema
L = np.sum(pi * np.arange(0, K+1))

# Probabilidad de que un vehículo que llega tenga que esperar
P_wait = 1 - np.sum(pi[:c+1])

# Gráfico de la distribución de probabilidad
plt.figure()
plt.bar(np.arange(0, K+1), pi)
plt.xlabel('Número de vehículos en el sistema')
plt.ylabel('Probabilidad')
plt.title('Distribución de probabilidad del número de vehículos en el sistema')
plt.show()

# Imprimir estadísticas
print(f'Número promedio de vehículos en el sistema: {L:.2f}')
print(f'Probabilidad de que un vehículo que llega tenga que esperar: {P_wait:.2f}')