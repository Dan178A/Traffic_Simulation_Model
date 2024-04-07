import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pygame
import os
from scipy.integrate import odeint, cumtrapz
from scipy.interpolate import interp1d


class Presentation_Result(object):
    def __init__(self, tiempo_simulacion: int):
        self.time = tiempo_simulacion
        self.figures = []  # Lista para almacenar las figuras y ejes
        self.vehiculos: dict[str, dict[str, float]] = {
            "car": {
                "masa": 1.814,
                "amortiguamiento": 50,
                "resorte": 10.0,
                "posicion": 1,
                "velocidad": 2.25,
            },
            "bus": {
                "masa": 9.071,
                "amortiguamiento": 100,
                "resorte": 20.0,
                "posicion": 1,
                "velocidad": 1.8,
            },
            "truck": {
                "masa": 3.629,
                "amortiguamiento": 150,
                "resorte": 30.0,
                "posicion": 1,
                "velocidad": 1.8,
            },
            "bike": {
                "masa": 250,
                "amortiguamiento": 30,
                "resorte": 5000,
                "posicion": 1,
                "velocidad": 2.5,
            },
        }

    def show_all_plots(self):
        # Calcular el número de filas y columnas necesarias
        num_plots = len(self.figures)
        # Puedes ajustar esto según sea necesario
        num_cols = int(len(self.figures)/4)
        num_rows = num_plots // num_cols
        if num_plots % num_cols:
            num_rows += 1

        # Crear una cuadrícula de subgráficos
        # Ajusta el tamaño de la figura según sea necesario
        fig, axs = plt.subplots(num_rows, num_cols, figsize=(13, 8))

        # Añadir cada figura a la cuadrícula
        for i, ax in enumerate(self.figures):
            # Calcular la posición en la cuadrícula
            row = i // num_cols
            col = i % num_cols

            # Añadir la figura a la cuadrícula
            for line in ax.lines:
                # Crear una copia de la línea
                line_copy = line.__class__(line.get_xdata(), line.get_ydata(), color=line.get_color(
                ), linestyle=line.get_linestyle(), linewidth=line.get_linewidth())
                axs[row, col].add_line(line_copy)
            for patch in ax.patches:
                # Crear una copia del parche
                patch_copy = matplotlib.patches.Rectangle((patch.get_x(), patch.get_y(
                )), patch.get_width(), patch.get_height(), fill=True, color=patch.get_facecolor())
                axs[row, col].add_patch(patch_copy)
            axs[row, col].set_xlabel(ax.get_xlabel(), fontsize=8)
            axs[row, col].set_ylabel(ax.get_ylabel(), fontsize=8)
            axs[row, col].set_title(ax.get_title(), fontsize=10)
            axs[row, col].relim()
            axs[row, col].autoscale_view()

            # # Reducir el tamaño de la fuente de los ejes
            # axs[row, col].tick_params(axis='both', which='major', labelsize=4)

        # Ajustar el layout para que los gráficos no se solapen
        plt.tight_layout()
        # Añadir espacio adicional entre los gráficos
        # plt.subplots_adjust(wspace=0.5, hspace=0.5)
        # Maximizar la ventana de la figura
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        plt.savefig('graphs/all_plots.png')
        # Mostrar la figura con todos los gráficos
        plt.close(fig)
        # Iniciar Pygame
        pygame.init()

        # Cargar la imagen guardada
        image = pygame.image.load('graphs/all_plots.png')

        # Crear una ventana del tamaño de la imagen
        screen = pygame.display.set_mode(
            (image.get_width(), image.get_height()))

        # Mostrar la imagen
        screen.blit(image, (0, 0))
        pygame.display.flip()

        # Mantener la ventana abierta hasta que se cierre
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()

    def model_trafic(self, position_lider: float = 50, position_seguidor: float = 40, distance: float = 10, velocity_lider: float = 30, velocity_seguidor: float = 20, acceleration: float = 5):
        # Parámetros del modelo FVADM
        k = 0.1  # Parámetro k
        V1 = 10  # Parámetro V1
        V2 = 20  # Parámetro V2
        C1 = 10  # Parámetro C1
        C2 = 20  # Parámetro C2
        lambda_ = 0.5  # Parámetro lambda
        gamma = 0.1  # Parámetro gamma

        # Posiciones de los vehículos
        x_l = position_lider  # Posición del vehículo líder
        x = position_seguidor  # Posición del vehículo seguidor
        l = distance  # Distancia entre vehículos
        v_l = velocity_lider  # Velocidad del vehículo líder
        v = velocity_seguidor  # Velocidad del vehículo seguidor
        a = acceleration  # Aceleración del vehículo

        # Función que define la ecuación diferencial FVADM
        def modelo_FVADM(v, _):
            return k * (V1 + V2 * np.tanh((C1 * (x_l - x - l)) / C2) - v) + lambda_ * (v_l - v) + gamma * a

        # Tiempo de simulación
        t = np.linspace(0, self.time, 1000)

        # Resolviendo la ecuación diferencial
        solucion = odeint(modelo_FVADM, v, t)
        # Crear la figura y los ejes
        #         ax = plt.Axes(fig=plt.figure(), rect=[0,0,1,1])

        ax = plt.Axes(fig=plt.figure(), rect=[0, 0, 1, 1])
        # Graficando la solución
        ax.plot(t, solucion)
        ax.set_xlabel('Tiempo')
        ax.set_ylabel('Velocidad del vehículo seguidor')
        ax.set_title(
            'Modelo Full Velocity \n and Acceleration Difference Model')
        self.figures.append(ax)

    def calculo_raices(self, N_vehiculos: int = 220):
        # Constante relacionada con el flujo de tráfico
        C = 75000
        # valor inicial para el flujo de tráfico
        Q0 = N_vehiculos
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
        Q_vals = np.linspace(0, self.time, 400)
        # Crear la figura y los ejes
        # fig, ax = plt.subplots()
        # Crear los ejes
        ax = plt.Axes(fig=plt.figure(), rect=[0, 0, 1, 1])
        # Graficamos f(Q) en función de Q
        ax.plot(Q_vals, f(Q_vals))
        # Marcamos la raíz encontrada en el gráfico
        ax.plot(Q, f(Q), 'ro')
        # Etiquetamos los ejes y el título del gráfico
        ax.set_xlabel('flujo de trafico (Q)')
        ax.set_ylabel('f(Q)')
        ax.set_title(
            'Metodo de Newton-Raphson \n para el calculo del trafico vehicular')
        # Activamos la cuadrícula del gráfico
        ax.grid(True)
        # Mostramos el gráfico
        self.figures.append(ax)

    def ajuste_curvas(self):
        # Datos: hora del dia y trafico vehicular
        horas_dia = np.array([6, 7, 8, 9, 10, 11, 12])
        trafico = np.array([100, 150, 200, 250, 300, 350, 400])

        # modelo de regresion lineal
        coeficientes = np.polyfit(horas_dia, trafico, 1)

        # predicciones
        horas_prediccion = np.linspace(6, 12, 100)
        trafico_predicho = np.polyval(coeficientes, horas_prediccion)
        # Crear la figura y los ejes
        # fig, ax = plt.subplots()
        # Crear los ejes
        ax = plt.Axes(fig=plt.figure(), rect=[0, 0, 1, 1])
        # Graficar
        ax.plot(horas_dia, trafico, 'o', markersize=10)
        ax.plot(horas_prediccion, trafico_predicho, '-r',
                linewidth=2)  # Graficar la linea de regresión
        ax.set_xlabel('hora del dia')
        ax.set_ylabel('Tráfico vehicular')
        ax.set_title('Regresión lineal de tráfico vehicular')
        ax.legend(['Datos', 'Linea de regresion'],
                  loc='upper right')
        ax.grid(True)

        self.figures.append(ax)

    def derivada_velocidad_aceleracion(self, speeds: list = [2.25, 1.8, 1.8, 2.5]):

        # Datos de tiempo y velocidad
        tiempo = np.linspace(0, self.time, 4)
        # de m/s a km/s
        velocidad = np.array([speed * 50 for speed in speeds])

        # Interpolación de la velocidad
        tiempo_interp = np.arange(0, tiempo[-1], 0.1)
        f = interp1d(tiempo, velocidad, kind='cubic')
        velocidad_interp = f(tiempo_interp)

        # Extrapolación de la velocidad
        tiempo_extrap = np.arange(0, velocidad[0], 0.1)
        f = interp1d(tiempo, velocidad, kind='cubic', fill_value="extrapolate")
        velocidad_extrap = f(tiempo_extrap)

        # Cálculo de la aceleración como la derivada de la velocidad
        aceleracion_interp = np.diff(velocidad_interp) / np.diff(tiempo_interp)
        aceleracion_extrap = np.diff(velocidad_extrap) / np.diff(tiempo_extrap)

        # Crear la figura y los ejes
        fig, axs = plt.subplots(2, 1)

        # Gráficos
        axs[0].plot(tiempo, velocidad, 'o', tiempo_interp,
                    velocidad_interp, '-', tiempo_extrap, velocidad_extrap, '--')
        axs[0].set_title('Velocidad vs. Tiempo')
        axs[0].set_xlabel('Tiempo (s)')
        axs[0].set_ylabel('Velocidad (m/s)')
        axs[0].legend(['Datos', 'Interpolación', 'Extrapolación'])

        axs[1].plot(tiempo_interp[:-1], aceleracion_interp,
                    '-', tiempo_extrap[:-1], aceleracion_extrap, '--')
        axs[1].set_title('Aceleración vs. Tiempo')
        axs[1].set_xlabel('Tiempo (s)')
        axs[1].set_ylabel('Aceleración (m/s^2)')
        axs[1].legend(['Interpolación', 'Extrapolación'])

        fig.tight_layout()
        # Aplanar axs y agregar cada objeto AxesSubplot a self.figures
        for ax in np.ravel(axs):
            self.figures.append(ax)

    def Acumulacion_integrales(self, vehicleClass: str = "car"):
        # Rango de tiempo
        t = np.arange(0, self.time, 0.1)

        velocidad_vehiculo = self.vehiculos[vehicleClass]["velocidad"]
        # Velocidad de los vehículos A y B
        v_A = velocidad_vehiculo*t
        v_B = velocidad_vehiculo*t + 4

        # Desplazamiento utilizando integración numérica
        s_A = cumtrapz(v_A, t, initial=0)
        s_B = cumtrapz(v_B, t, initial=0)
        # Crear la figura y los ejes
        fig, axs = plt.subplots(2, 1)

        # Graficar Velocidad vs. Tiempo
        axs[0].plot(t, v_A, 'b-', t, v_B, 'r--')
        axs[0].legend(['Velocidad A', 'Velocidad B'])
        axs[0].set_title('Velocidad vs. Tiempo')
        axs[0].set_xlabel('Tiempo (s)')
        axs[0].set_ylabel('Velocidad (m/s)')

        # Graficar Desplazamiento vs. Tiempo
        axs[1].plot(t, s_A, 'b-', t, s_B, 'r--')

        axs[1].legend(['Desplazamiento A', 'Desplazamiento B'])
        axs[1].set_title('Desplazamiento vs. Tiempo')
        axs[1].set_xlabel('Tiempo (s)')
        axs[1].set_ylabel('Desplazamiento (m)')

        fig.tight_layout()
        # Aplanar axs y agregar cada objeto AxesSubplot a self.figures
        for ax in np.ravel(axs):
            self.figures.append(ax)

    def Trazado_trayectorias(self, vehiculo1: tuple[float, float, float] = (0, 0, 3), vehiculo2: tuple[float, float, float] = (0, 0, 1.5)):

        tiempo_final = self.time  # segundos
        dt = 0.1
        # condiciones iniciales para el vehiculo1

        posicion1, velocidad1, aceleracion1 = vehiculo1

        # condiciones iniciales para el vehiculo2
        posicion2, velocidad2, aceleracion2 = vehiculo2
        # Crear la figura y los ejes
        ax = plt.Axes(fig=plt.figure(), rect=[0, 0, 1, 1])

        # Preparacion de la figura para la simulacion

        ax.grid(True)
        ax.set_xlabel('tiempo (s)')
        ax.set_ylabel('Posicion (m)')

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
        ax.plot(tiempos, posiciones1, 'r-')
        ax.plot(tiempos, posiciones2, 'b-')

        ax.set_title('Trayectoria de dos vehiculos')
        ax.legend(['Vehiculo 1', 'Vehiculo 2'])
        self.figures.append(ax)

    def Trapecio(self, vehiculeClass: str = "car"):
        # Definir el tiempo de 0 a 300 segundos
        t = np.arange(0, self.time, 0.1)

        # Velocidad del vehículo
        velocidad_vehiculo = self.vehiculos[vehiculeClass]["velocidad"]

        # Definir la función de velocidad en m/s
        v = velocidad_vehiculo*t - 2

        # Desplazamiento
        desplazamiento = np.trapz(v, t) / 1000  # km

        # Velocidad absoluta
        v_abs = np.abs(v)

        # Distancia total
        distancia_total = np.trapz(v_abs, t) / 1000  # km

        # Crear gráfico de barras
        labels = ['Desplazamiento', 'Distancia Total Recorrida']
        values = [desplazamiento, distancia_total]
        # Crear la figura y los ejes
        ax = plt.Axes(fig=plt.figure(), rect=[0, 0, 1, 1])

        ax.bar(labels, values)
        ax.set_ylabel('Kilómetros')
        ax.set_title('Desplazamiento y Distancia Total Recorrida')
        self.figures.append(ax)

    def Masa_amortiguador(self, vehicleClass: str = "car"):

        masa = self.vehiculos[vehicleClass]["masa"]
        amortiguamiento = self.vehiculos[vehicleClass]["amortiguamiento"]
        resorte = self.vehiculos[vehicleClass]["resorte"]
        posicion = self.vehiculos[vehicleClass]["posicion"]
        velocidad = self.vehiculos[vehicleClass]["velocidad"]
        # parametros del sistema
        m = masa  # masa (kg)
        b = amortiguamiento  # coeficiente de amortiguamiento (Ns/m)
        k = resorte  # constante del resorte (N/m)

        # Condiciones Iniciales
        x0 = posicion  # posicion inicial
        v0 = velocidad  # Velocidad inicial (m/s)

        # Tiempo de Simulacion
        t = np.linspace(0, self.time, 1000)  # desde t=0 hasta t=10

        # Definicion de las ecuaciones de movimiento
        def ode(y, t, b, k, m):
            x, v = y
            dydt = [v, -(b/m) * v + -(k/m) * x]
            return dydt

        # Resolucion de las ecuaciones de movimiento
        y0 = [x0, v0]
        sol = odeint(ode, y0, t, args=(b, k, m))
        # Crear la figura y los ejes
        fig, axs = plt.subplots(2, 1)

        # Visualizacion de la posicion en funcion del tiempo
        axs[0].plot(t, sol[:, 0], 'b', linewidth=2)
        axs[0].set_xlabel('Tiempo (s)')
        axs[0].set_ylabel('Posicion (m)')
        axs[0].set_title(
            "Posicion vs Tiempo del Sistema \n Masa-Resorte-Amortiguador")

        # Visualizacion de la velocidad en funcion del tiempo
        axs[1].plot(t, sol[:, 1], 'b', linewidth=2)
        axs[1].set_xlabel('Tiempo (s)')
        axs[1].set_ylabel('Velocidad (m/s)')
        axs[1].set_title(
            "Velocidad vs Tiempo del Sistema \n Masa-Resorte-Amortiguador")

        fig.tight_layout()
        # Aplanar axs y agregar cada objeto AxesSubplot a self.figures
        for ax in np.ravel(axs):
            self.figures.append(ax)

    def analogia_masa_amortiguador(self, vehicleClass: str = "car"):

        masa = self.vehiculos[vehicleClass]["masa"]
        amortiguamiento = self.vehiculos[vehicleClass]["amortiguamiento"]
        resorte = self.vehiculos[vehicleClass]["resorte"]
        posicion = self.vehiculos[vehicleClass]["posicion"]
        velocidad = self.vehiculos[vehicleClass]["velocidad"]
        # Parámetros del sistema
        m = masa  # masa (kg)
        c = amortiguamiento  # coeficiente de amortiguamiento (Ns/m)
        k = resorte  # constante del resorte (N/m)

        # Condiciones iniciales
        x0 = posicion  # posición inicial
        v0 = velocidad  # velocidad inicial (m/s)

        # Definición de las ecuaciones de movimiento
        def vehicle_dynamics(x, t, m, c, k):
            dxdt = np.zeros(2)
            dxdt[0] = x[1]

            leader_speed = 20 + 5*np.sin(0.5*t)
            dxdt[1] = (-c*x[1] - k*(x[0] - leader_speed)) / m

            return dxdt

        # Resolución de las ecuaciones de movimiento
        y0 = [x0, v0]
        t = np.linspace(0, self.time, 1000)
        sol = odeint(vehicle_dynamics, y0, t, args=(
            m, c, k), atol=1e-9, rtol=1e-6)
        # Crear la figura y los ejes
        fig, axs = plt.subplots(2, 1)

        # Visualización de la posición en función del tiempo
        axs[0].plot(t, sol[:, 0])
        axs[0].set_title('Posicion del vehiculo Seguidor')
        axs[0].set_xlabel('Tiempo (s)')
        axs[0].set_ylabel('Posicion (m)')

        # Visualización de la velocidad en función del tiempo
        axs[1].plot(t, sol[:, 1])
        axs[1].set_title('Velocidad del vehiculo Seguidor')
        axs[1].set_xlabel('Tiempo (s)')
        axs[1].set_ylabel('Velocidad (m/s)')

        fig.tight_layout()
        # Aplanar axs y agregar cada objeto AxesSubplot a self.figures
        for ax in np.ravel(axs):
            self.figures.append(ax)

    def Teorias_colas_simples(self, Numero_vehiculos: int = 10):
        # Parámetros del sistema
        _lambda = 4  # Tasa de llegada de vehículos
        mu = 5  # Tasa de servicio
        k = Numero_vehiculos  # Número máximo de vehículos en el sistema

        # Probabilidad de que el sistema esté en estado i
        pi = np.zeros(k+1)
        pi[0] = 1
        for i in range(1, k+1):
            pi[i] = (_lambda/mu)**i * pi[0]
        pi[0] = 1 / np.sum(pi)

        # Número promedio de vehículos en el sistema
        L = np.sum(pi * np.arange(0, k+1))

        # Probabilidad de que un vehículo que llega tenga que esperar
        P_wait = 1 - pi[0]
        # Crear la figura y los ejes
        ax = plt.Axes(fig=plt.figure(), rect=[0, 0, 1, 1])

        # Gráfico de la distribución de probabilidad

        ax.bar(np.arange(0, k+1), pi)
        ax.set_xlabel('Número de vehículos en el sistema')
        ax.set_ylabel('Probabilidad')
        ax.set_title(
            'Distribución de probabilidad \n del número de vehículos en el sistema')
        self.figures.append(ax)

        # Imprimir estadísticas
        print(f'Número promedio de vehículos en el sistema: {L:.2f}')
        print(
            f'Probabilidad de que un vehículo que llega tenga que esperar: {P_wait:.2f}')

    def Teorias_colas_multiples(self, Numero_vehiculos: int = 10):
        # Parámetros del sistema
        _lambda = 6  # Tasa de llegada de vehículos
        mu = 5  # Tasa de servicio
        c = 4  # Número de servidores
        K = Numero_vehiculos  # Número máximo de vehículos en el sistema

        # Probabilidad de que el sistema esté en estado i
        pi = np.zeros(K+1)
        pi[0] = 1
        for i in range(1, c+1):
            pi[i] = (_lambda/mu)**i * pi[0]
        for i in range(c+1, K+1):
            pi[i] = (_lambda/(c*mu))**i * pi[0]
        pi[0] = 1 / np.sum(pi)

        # Número promedio de vehículos en el sistema
        L = np.sum(pi * np.arange(0, K+1))

        # Probabilidad de que un vehículo que llega tenga que esperar
        P_wait = 1 - np.sum(pi[:c+1])
        # Crear la figura y los ejes
        ax = plt.Axes(fig=plt.figure(), rect=[0, 0, 1, 1])

        # Gráfico de la distribución de probabilidad

        ax.bar(np.arange(0, K+1), pi)
        ax.set_xlabel('Número de vehículos en el sistema')
        ax.set_ylabel('Probabilidad')
        ax.set_title(
            'Distribución de probabilidad  \ndel número de vehículos en el sistema')
        self.figures.append(ax)

        # Imprimir estadísticas
        print(f'Número promedio de vehículos en el sistema: {L:.2f}')
        print(
            f'Probabilidad de que un vehículo que llega tenga que esperar: {P_wait:.2f}')

    def Monte_Carlo(self, simulaciones: int = 1000):
        # Parámetros
        lambda_ = 2  # media de tiempo entre llegadas, en minutos
        mu = 1  # media de tiempo de servicio, en minutos
        sigma = 0.5  # desviación estándar del tiempo de servicio en minutos
        N = simulaciones  # número de simulaciones

        tiempo_espera = np.zeros(N)

        for i in range(N):
            llegadas = np.cumsum(np.random.exponential(
                lambda_, 100))  # 100 vehículos
            inicio_servicio = max(0, llegadas[0] - np.random.normal(mu, sigma))
            fin_servicio = inicio_servicio + np.random.normal(mu, sigma)
            espera = inicio_servicio - llegadas[0]

            for j in range(1, len(llegadas)):
                inicio_servicio = max(fin_servicio, llegadas[j])
                fin_servicio = inicio_servicio + np.random.normal(mu, sigma)
                espera += inicio_servicio - llegadas[j]

            tiempo_espera[i] = espera / len(llegadas)

        media_espera = np.mean(tiempo_espera)
        desviacion_espera = np.std(tiempo_espera)
        # Crear la figura y los ejes
        ax = plt.Axes(fig=plt.figure(), rect=[0, 0, 1, 1])

        # Gráfico de los tiempos de espera
        ax.hist(tiempo_espera, bins=20)
        ax.set_xlabel('Tiempo Medio de espera (Minutos)')
        ax.set_ylabel('Frecuencia')
        ax.set_title(
            'Distribución del tiempo \n medio de espera en la interacción')
        self.figures.append(ax)


if __name__ == '__main__':
    modulo = Presentation_Result(300)
    modulo.model_trafic()
    modulo.calculo_raices()
    modulo.ajuste_curvas()
    modulo.derivada_velocidad_aceleracion()
    modulo.Acumulacion_integrales()
    modulo.Trazado_trayectorias()
    modulo.Trapecio()
    modulo.Masa_amortiguador()
    modulo.analogia_masa_amortiguador()
    modulo.Teorias_colas_simples()
    modulo.Teorias_colas_multiples()
    modulo.Monte_Carlo()
    modulo.show_all_plots()
