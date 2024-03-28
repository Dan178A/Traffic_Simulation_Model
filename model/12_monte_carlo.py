import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Definir parámetros del modelo
num_simulaciones = 1000
num_vehiculos = 220
velocidad_media = 80 # km/h
desviacion_velocidad = 10 # km/h
num_vehiculos_hora_pico = 330  # Aumento de vehículos durante la hora pico
probabilidad_hora_pico = 0.25  # Probabilidad de que sea hora pico

# Inicializar lista para almacenar resultados
resultados_simulacion: list = []

# Ejecutar la simulación
for _ in range(num_simulaciones):
    # Determinar si es hora pico
    es_hora_pico: bool = np.random.rand() < probabilidad_hora_pico

    # Ajustar el número de vehículos en función de si es hora pico
    num_vehiculos_simulacion: int  = num_vehiculos_hora_pico if es_hora_pico else num_vehiculos

    # Generar velocidades aleatorias para los vehículos
    velocidades = np.random.normal(velocidad_media, desviacion_velocidad, num_vehiculos_simulacion)

    # Test de la simulación
    tiempo_viaje_promedio = np.mean(velocidades) / 60 # Convertir a horas

    # push de los resultados a la lista
    resultados_simulacion.append(tiempo_viaje_promedio)

# Convertir la lista de resultados en un DataFrame para análisis
df_resultados: pd.DataFrame = pd.DataFrame(resultados_simulacion, columns=['Tiempo Viaje Promedio'])

# Analizar los resultados
media_tiempo_viaje: float = df_resultados['Tiempo Viaje Promedio'].mean()
desviacion_tiempo_viaje: float = df_resultados['Tiempo Viaje Promedio'].std()

print(f"Tiempo de viaje promedio: {media_tiempo_viaje:.2f} horas")
print(f"Desviación estándar del tiempo de viaje: {desviacion_tiempo_viaje:.2f} horas")

# Plot de histograma de los resultados
plt.hist(resultados_simulacion, bins=30, edgecolor='black')

# labels
plt.title('Distribución de los Resultados de la Simulación Monte Carlo')
plt.xlabel('Valor del Resultado') # x-axis: Representa el tiempo de viaje promedio en horas
plt.ylabel('Frecuencia') # y-axis: Representa la frecuencia de cada valor

# Mostrar el gráfico
plt.show()
