import numpy as np
import matplotlib.pyplot as plt

# Definir el tiempo de 0 a 300 segundos
t = np.arange(0, 300, 0.1)

# Definir la función de velocidad
v = 4*t - 2

# Desplazamiento
desplazamiento = np.trapz(v, t) / 1000 # km

# Velocidad absoluta
v_abs = np.abs(4*t - 2)

# Distancia total
distancia_total = np.trapz(v_abs, t) / 1000 # km

# Crear gráfico de barras
labels = ['Desplazamiento', 'Distancia Total Recorrida']
values = [desplazamiento, distancia_total]

plt.bar(labels, values)
plt.ylabel('Kilómetros')
plt.title('Desplazamiento y Distancia Total Recorrida')
plt.show()