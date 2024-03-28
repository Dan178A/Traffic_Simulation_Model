import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Parámetros del sistema
m = 1350 # masa (kg)
c = 600 # coeficiente de amortiguamiento (Ns/m)
k = 1500 # constante del resorte (N/m)

# Condiciones iniciales
x0 = 0 # posición inicial
v0 = 20 # velocidad inicial (m/s)

# Definición de las ecuaciones de movimiento
def vehicle_dynamics(x, t, m, c, k):
    dxdt = np.zeros(2)
    dxdt[0] = x[1]
    
    leader_speed = 20 + 5*np.sin(0.5*t)
    dxdt[1] = (-c*x[1] - k*(x[0] - leader_speed)) / m
    
    return dxdt

# Resolución de las ecuaciones de movimiento
y0 = [x0, v0]
t = np.linspace(0, 60, 1000)
sol = odeint(vehicle_dynamics, y0, t, args=(m, c, k), atol=1e-9, rtol=1e-6)

# Visualización de la posición en función del tiempo
plt.figure()
plt.subplot(2,1,1)
plt.plot(t, sol[:, 0])
plt.title('Posicion del vehiculo Seguidor')
plt.xlabel('Tiempo (s)')
plt.ylabel('Posicion (m)')

# Visualización de la velocidad en función del tiempo
plt.subplot(2,1,2)
plt.plot(t, sol[:, 1])
plt.title('Velocidad del vehiculo Seguidor')
plt.xlabel('Tiempo (s)')
plt.ylabel('Velocidad (m/s)')

plt.tight_layout()
plt.show()