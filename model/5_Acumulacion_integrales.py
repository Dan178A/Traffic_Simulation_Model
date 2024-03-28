import numpy as np
from scipy.integrate import cumtrapz
import matplotlib.pyplot as plt

# Rango de tiempo
t = np.arange(0, 300.1, 0.1)

# Velocidad de los vehículos A y B
v_A = 3*t
v_B = 3*t + 4

# Desplazamiento utilizando integración numérica
s_A = cumtrapz(v_A, t, initial=0)
s_B = cumtrapz(v_B, t, initial=0)

# Graficar Velocidad vs. Tiempo
plt.figure()
plt.subplot(2,1,1)
plt.plot(t, v_A, 'b-', t, v_B, 'r--')
plt.legend(['Velocidad A', 'Velocidad B'])
plt.title('Velocidad vs. Tiempo')
plt.xlabel('Tiempo (s)')
plt.ylabel('Velocidad (m/s)')

# Graficar Desplazamiento vs. Tiempo
plt.subplot(2,1,2)
plt.plot(t, s_A, 'b-', t, s_B, 'r--')
plt.legend(['Desplazamiento A', 'Desplazamiento B'])
plt.title('Desplazamiento vs. Tiempo')
plt.xlabel('Tiempo (s)')
plt.ylabel('Desplazamiento (m)')

plt.tight_layout()
plt.show()