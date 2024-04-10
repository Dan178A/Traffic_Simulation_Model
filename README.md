# Traffic_simulation_Model


<img src="/images/output.gif" width="100%" height="100%">

## Description

Modelo de simulación de tráfico vehicular que se asemeja a un modelo macroscópico de simulación de tráfico vehicular. Este modelo se centra en la simulación de la interacción entre vehículos y señales de tráfico en una intersección, utilizando un enfoque macroscópico para representar el comportamiento del tráfico a nivel de la intersección.

El modelo se basa en varios conceptos clave de la simulación de tráfico vehicular macroscópica:

* `Señales de Tráfico`: El modelo utiliza señales de tráfico para controlar el flujo de vehículos en la intersección. Las señales tienen tiempos de luz verde, amarilla y roja, que se actualizan en función de un temporizador. Este enfoque es similar a cómo las señales de tráfico reales controlan el flujo de vehículos en las intersecciones.

* `Vehículos y Direcciones`: Los vehículos se representan como objetos con atributos como velocidad, dirección y si se van a girar o no. Los vehículos se mueven en direcciones específicas (derecha, abajo, izquierda, arriba) y pueden girar si se les permite hacerlo. Este enfoque macroscópico permite modelar el comportamiento del tráfico a nivel de la intersección, en lugar de centrarse en el comportamiento individual de cada vehículo.

* `Movimiento de Vehículos`: Los vehículos se mueven en función de las señales de tráfico y las condiciones de la intersección. El modelo implementa lógica para manejar el movimiento de los vehículos, incluyendo cómo se detienen, giran y se mueven a través de la intersección. Esto es crucial para simular el flujo de tráfico realista en una intersección.

* `Generación de Vehículos`: El modelo genera vehículos de manera aleatoria en intervalos de tiempo, seleccionando aleatoriamente el tipo de vehículo, el carril y si se van a girar o no. Esto permite simular una variedad de situaciones de tráfico en la intersección.

* `Simulación de Tiempo`: El modelo cuenta el tiempo transcurrido en la simulación y muestra estadísticas como el número total de vehículos que han cruzado la intersección y el tiempo total transcurrido. Esto es útil para evaluar el rendimiento del sistema de señales de tráfico.

>En resumen, el modelo implementado en el código se asemeja a un modelo macroscópico de simulación de tráfico vehicular, utilizando señales de tráfico para controlar el flujo de vehículos en una intersección y representando los vehículos como objetos con atributos específicos que determinan su comportamiento. Este enfoque permite simular de manera efectiva el comportamiento del tráfico a nivel de la intersección, proporcionando una herramienta valiosa para la planificación y gestión del tráfico vehicular.

## Table of Contents
- [Prerequisites](#Prerequisites)
- [Installation](#installation)
- [Usage](#usage)

### Prerequisites

Necesitas:

-   [Python](https://www.python.org) (3.7 or newer)
## Installation

```shell
    pip install pygame
    pip install matplotlib
    pip install scipy
    pip install numpy
    pip install pandas
```

## Usage

### Run The file:

```shell
    python simulation.py
```

[Tiempo de simulacion](simulation.py) (Linea: 132):
```python
# `simulationTime` es la duración total de la simulación.
simulationTime = 300
```

### Buttons:

>Disabled (Hora Pico):

<img src="./images/buttons/buttonGo_small.png" width="115" height="115">

>Enabled (Hora Pico):

<img src="./images/buttons/buttonStop3_small.png" width="100" height="100">

>Info (Análisis de Resultados)

<img src="./images/buttons/infoBlue.png" width="100" height="100">

Que Despliega los Resultados de la simulacion:

<img src="./Docs//images/Screenshot 2024-04-07 120700.png" width="100%" height="100%">
