import numpy as np
import matplotlib.pyplot as plt

# Definimos las constantes y variables iniciales

# Constante relacionada con el flujo de tráfico
C = 75000
# valor inicial para el flujo de tráfico
Q0 = 220
# Tolerancia para la convergencia
tolerancia = 1e-6
# Número máximo de iteraciones
maxIter = 100
iter = 0
Q = Q0


while True:
    # Calculamos el siguiente valor de Q usando la fórmula de Newton-Raphson
    Qnext = Q - (Q**2 - C) / (2*Q)
    # Si la diferencia entre Qnext y Q es menor que la tolerancia, terminamos el bucle
    if abs(Qnext - Q) < tolerancia:
        break
    # Actualizamos el valor de Q
    Q = Qnext
    # Incrementamos el contador de iteraciones
    iter = iter + 1
    # Si hemos excedido el número máximo de iteraciones, terminamos el bucle
    if iter > maxIter:
        print('Se excedio el numero maximo de iteraciones')
        break

# Imprimimos la raíz encontrada y el número de iteraciones
print('la raiz encontrada es:', Q)
print('numero de iteraciones:', iter)

# Definimos la función f(Q)
f = lambda Q: Q**2 - C

# Generamos un conjunto de valores de Q para graficar
Q_vals = np.linspace(0, 300, 400)
# Graficamos f(Q) en función de Q
plt.plot(Q_vals, f(Q_vals))
# Marcamos la raíz encontrada en el gráfico
plt.plot(Q, f(Q), 'ro')
# Etiquetamos los ejes y el título del gráfico
plt.xlabel('flujo de trafico (Q)')
plt.ylabel('f(Q)')
plt.title('Metodo de Newton-Raphson para el calculo del trafico vehicular')
# Activamos la cuadrícula del gráfico
plt.grid(True)
# Mostramos el gráfico
plt.show()