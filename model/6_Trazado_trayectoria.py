import numpy as np
import matplotlib.pyplot as plt

tiempo_final = 30  # segundos
dt = 0.1

# condiciones iniciales para el vehiculo1
posicion1 = 0
velocidad1 = 0
aceleracion1 = 3

# condiciones iniciales para el vehiculo2
posicion2 = 0
velocidad2 = 0
aceleracion2 = 1.5

# Preparacion de la figura para la simulacion
plt.figure()
plt.grid(True)
plt.xlabel('tiempo (s)')
plt.ylabel('Posicion (m)')

# Listas para almacenar las posiciones y tiempos
tiempos = []
posiciones1 = []
posiciones2 = []

# for simulacion
for t in np.arange(0, tiempo_final+dt, dt):
    # Actualizar Posiciones y Velocidades
    posicion1 = posicion1 + velocidad1 * dt
    velocidad1 = velocidad1 + aceleracion1 * dt

    posicion2 = posicion2 + velocidad2 * dt
    velocidad2 = velocidad2 + aceleracion2 * dt

    # Almacenar los tiempos y posiciones
    tiempos.append(t)
    posiciones1.append(posicion1)
    posiciones2.append(posicion2)

# Graficar
plt.plot(tiempos, posiciones1, 'r-')
plt.plot(tiempos, posiciones2, 'b-')

plt.title('Trayectoria de dos vehiculos')
plt.legend(['Vehiculo 1', 'Vehiculo 2'])
plt.show()