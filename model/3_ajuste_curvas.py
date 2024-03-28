import numpy as np
import matplotlib.pyplot as plt

# Datos: hora del dia y trafico vehicular
horas_dia = np.array([6, 7, 8, 9, 10, 11, 12])
trafico = np.array([100, 150, 200, 250, 300, 350, 400])

# modelo de regresion lineal
coeficientes = np.polyfit(horas_dia, trafico, 1)

# predicciones
horas_prediccion = np.linspace(6, 12, 100)
trafico_predicho = np.polyval(coeficientes, horas_prediccion)

# Graficar
plt.figure()
plt.plot(horas_dia, trafico, 'o', markersize=10)
plt.plot(horas_prediccion, trafico_predicho, '-r', linewidth=2)  # Graficar la linea de regresión
plt.xlabel('hora del dia')
plt.ylabel('Tráfico vehicular')
plt.title('Regresión lineal de tráfico vehicular')
plt.legend(['Datos', 'Linea de regresion'], loc='upper right')  # Corrección aquí
plt.grid(True)

# Interpretación de resultados
print('Coeficientes del modelo de regresión lineal: ')
print(f'Pendiente (coeficiente 1): {coeficientes[0]}')
print(f'Término independiente (coeficiente 2): {coeficientes[1]}')

plt.show()