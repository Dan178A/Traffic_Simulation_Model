import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

# Datos de tiempo y velocidad
tiempo = np.array([0, 2, 4, 6, 8, 10])
velocidad = np.array([0, 10, 20, 30, 40, 50])

# Interpolación de la velocidad
tiempo_interp = np.arange(0, 10.1, 0.1)
f = interp1d(tiempo, velocidad, kind='cubic')
velocidad_interp = f(tiempo_interp)

# Extrapolación de la velocidad
tiempo_extrap = np.arange(0, 12.1, 0.1)
f = interp1d(tiempo, velocidad, kind='cubic', fill_value="extrapolate")
velocidad_extrap = f(tiempo_extrap)

# Cálculo de la aceleración como la derivada de la velocidad
aceleracion_interp = np.diff(velocidad_interp) / np.diff(tiempo_interp)
aceleracion_extrap = np.diff(velocidad_extrap) / np.diff(tiempo_extrap)

# Gráficos
plt.figure()
plt.subplot(2, 1, 1)
plt.plot(tiempo, velocidad, 'o', tiempo_interp, velocidad_interp, '-', tiempo_extrap, velocidad_extrap, '--')
plt.title('Velocidad vs. Tiempo')
plt.xlabel('Tiempo (s)')
plt.ylabel('Velocidad (m/s)')
plt.legend(['Datos', 'Interpolación', 'Extrapolación'])

plt.subplot(2, 1, 2)
plt.plot(tiempo_interp[:-1], aceleracion_interp, '-', tiempo_extrap[:-1], aceleracion_extrap, '--')
plt.title('Aceleración vs. Tiempo')
plt.xlabel('Tiempo (s)')
plt.ylabel('Aceleración (m/s^2)')
plt.legend(['Interpolación', 'Extrapolación'])

plt.tight_layout()
plt.show()