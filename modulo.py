import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.integrate import odeint, cumtrapz
from scipy.interpolate import interp1d


class Modulo:
    def __init__(self, n):
        self.n = n

    def model_trafic(self):
        # Parámetros del modelo FVADM
        k = 0.1  # Parámetro k
        V1 = 10  # Parámetro V1
        V2 = 20  # Parámetro V2
        C1 = 10  # Parámetro C1
        C2 = 20  # Parámetro C2
        lambda_ = 0.5  # Parámetro lambda
        gamma = 0.1  # Parámetro gamma

        # Posiciones de los vehículos
        x_l = 50  # Posición del vehículo líder
        x = 40  # Posición del vehículo seguidor
        l = 10  # Distancia entre vehículos
        v_l = 30  # Velocidad del vehículo líder
        v = 20  # Velocidad del vehículo seguidor
        a = 5  # Aceleración del vehículo

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

    def calculo_raices(self):
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
        def f(Q): return Q**2 - C

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

    def ajuste_curvas(self):
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
        plt.plot(horas_prediccion, trafico_predicho, '-r',
                 linewidth=2)  # Graficar la linea de regresión
        plt.xlabel('hora del dia')
        plt.ylabel('Tráfico vehicular')
        plt.title('Regresión lineal de tráfico vehicular')
        plt.legend(['Datos', 'Linea de regresion'],
                   loc='upper right')  # Corrección aquí
        plt.grid(True)

        # Interpretación de resultados
        print('Coeficientes del modelo de regresión lineal: ')
        print(f'Pendiente (coeficiente 1): {coeficientes[0]}')
        print(f'Término independiente (coeficiente 2): {coeficientes[1]}')

        plt.show()

    def derivada_velocidad_aceleracion(self):
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
        plt.plot(tiempo, velocidad, 'o', tiempo_interp,
                 velocidad_interp, '-', tiempo_extrap, velocidad_extrap, '--')
        plt.title('Velocidad vs. Tiempo')
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Velocidad (m/s)')
        plt.legend(['Datos', 'Interpolación', 'Extrapolación'])

        plt.subplot(2, 1, 2)
        plt.plot(tiempo_interp[:-1], aceleracion_interp,
                 '-', tiempo_extrap[:-1], aceleracion_extrap, '--')
        plt.title('Aceleración vs. Tiempo')
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Aceleración (m/s^2)')
        plt.legend(['Interpolación', 'Extrapolación'])

        plt.tight_layout()
        plt.show()

    def Acumulacion_integrales(self):
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
        plt.subplot(2, 1, 1)
        plt.plot(t, v_A, 'b-', t, v_B, 'r--')
        plt.legend(['Velocidad A', 'Velocidad B'])
        plt.title('Velocidad vs. Tiempo')
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Velocidad (m/s)')

        # Graficar Desplazamiento vs. Tiempo
        plt.subplot(2, 1, 2)
        plt.plot(t, s_A, 'b-', t, s_B, 'r--')
        plt.legend(['Desplazamiento A', 'Desplazamiento B'])
        plt.title('Desplazamiento vs. Tiempo')
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Desplazamiento (m)')

        plt.tight_layout()
        plt.show()

    def Trazado_trayectorias(self):
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

    def Trapecio(self):
        ...

    def Masa_amortiguador(self):
        ...

    def analogia_masa_amortiguador(self):
        ...

    def Teorias_colas_simples(self):
        ...

    def Teorias_colas_multiples(self):
        ...

    def Monte_Carlo(self):
        ...
