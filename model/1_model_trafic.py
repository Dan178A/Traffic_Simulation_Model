import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Parámetros del modelo FVADM
k = 0.1 # Parámetro k
V1 = 10 # Parámetro V1
V2 = 20 # Parámetro V2
C1 = 10 # Parámetro C1
C2 = 20 # Parámetro C2
lambda_ = 0.5 # Parámetro lambda
gamma = 0.1 # Parámetro gamma

# Posiciones de los vehículos
x_l = 50 # Posición del vehículo líder
x = 40 # Posición del vehículo seguidor
l = 10 # Distancia entre vehículos
v_l = 30 # Velocidad del vehículo líder
v = 20 # Velocidad del vehículo seguidor
a = 5 # Aceleración del vehículo

# Función que define la ecuación diferencial FVADM
def modelo_FVADM(v, t):
    return k * (V1 + V2 * np.tanh((C1 * (x_l - x - l)) / C2) - v) + lambda_ * (v_l - v) + gamma * a

# Tiempo de simulación
t = np.linspace(0, 300, 1000)

# Resolviendo la ecuación diferencial
solucion = odeint(modelo_FVADM, v, t)

# Graficando la solución
plt.plot(t, solucion)
plt.xlabel('Tiempo')
plt.ylabel('Velocidad del vehículo seguidor')
plt.title('Modelo Full Velocity and Acceleration Difference Model')
plt.show()
