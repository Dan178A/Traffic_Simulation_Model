import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# parametros del sistema
m = 1000  # masa (kg)
b = 0.5  # coeficiente de amortiguamiento (Ns/m)
k = 200  # constante del resorte (N/m)

# Condiciones Iniciales
x0 = 1  # posicion inicial
v0 = 0  # Velocidad inicial (m/s)

# Tiempo de Simulacion
t = np.linspace(0, 20, 1000)  # desde t=0 hasta t=10

# Definicion de las ecuaciones de movimiento
def ode(y, t, b, k, m):
    x, v = y
    dydt = [v, -(b/m) * v + -(k/m) * x]
    return dydt

# Resolucion de las ecuaciones de movimiento
y0 = [x0, v0]
sol = odeint(ode, y0, t, args=(b, k, m))

# Visualizacion de la posicion en funcion del tiempo
plt.figure()
plt.subplot(2,1,1)
plt.plot(t, sol[:, 0], 'b', linewidth=2)
plt.xlabel('Tiempo (s)')
plt.ylabel('Posicion (m)')
plt.title("Posicion vs Tiempo del Sistema Masa-Resorte-Amortiguador")

# Visualizacion de la velocidad en funcion del tiempo
plt.subplot(2,1,2)
plt.plot(t, sol[:, 1], 'b', linewidth=2)
plt.xlabel('Tiempo (s)')
plt.ylabel('Velocidad (m/s)')
plt.title("Velocidad vs Tiempo del Sistema Masa-Resorte-Amortiguador")

plt.tight_layout()
plt.show()