import random
import time
import threading
import pygame
import sys
import os

# Default values of signal timers
defaultGreen = {
    0: 10,
    1: 10,
    2: 10,
    3: 10
}
# Default red signal time
defaultRed = 150
# Default yellow signal time
defaultYellow = 5

# Signals list
signals = []

# Number of signals
noOfSignals = 4

# Indicates which signal is green currently
currentGreen = 0

# Indicates which signal will turn green next
nextGreen = (currentGreen+1) % noOfSignals

# Indicates whether yellow signal is on or off
currentYellow = 0

# average speeds of vehicles
speeds = {
    'car': 2.25,
    'bus': 1.8,
    'truck': 1.8,
    'bike': 2.5
}

# Coordinates of vehicles' start
x = {
    'right': [0, 0, 0],
    'down': [755, 727, 697],
    'left': [1400, 1400, 1400],
    'up': [602, 627, 657]
}

y = {
    'right': [348, 370, 398],
    'down': [0, 0, 0],
    'left': [498, 466, 436],
    'up': [800, 800, 800]
}

# Caracteristic vehicles
vehicles = {
    'right': {0: [], 1: [], 2: [], 'crossed': 0},
    'down': {0: [], 1: [], 2: [], 'crossed': 0},
    'left': {0: [], 1: [], 2: [], 'crossed': 0},
    'up': {0: [], 1: [], 2: [], 'crossed': 0}
}

vehicleTypes = {0: 'car', 1: 'bus', 2: 'truck', 3: 'bike'}

# Directions
directionNumbers = {0: 'right', 1: 'down', 2: 'left', 3: 'up'}

# Coordinates of signal image, timer, and vehicle count
signalCoods = [(530, 230), (810, 230), (810, 570), (530, 570)]
signalTimerCoods = [(530, 210), (810, 210), (810, 550), (530, 550)]

# Coordinates of stop lines
stopLines = {'right': 590, 'down': 330, 'left': 800, 'up': 535}
defaultStop = {'right': 580, 'down': 320, 'left': 810, 'up': 545}

# Gap between vehicles
stoppingGap = 25    # stopping gap
movingGap = 25   # moving gap

# set allowed vehicle types here
allowedVehicleTypes = {'car': True, 'bus': True, 'truck': True, 'bike': True}
allowedVehicleTypesList = []
vehiclesTurned = {
    'right': {1: [], 2: []},
    'down': {1: [], 2: []},
    'left': {1: [], 2: []},
    'up': {1: [], 2: []}
}
vehiclesNotTurned = {
    'right': {1: [], 2: []},
    'down': {1: [], 2: []},
    'left': {1: [], 2: []},
    'up': {1: [], 2: []}
}
rotationAngle = 3

# `mid` es un diccionario que almacena las coordenadas centrales para cada dirección en la simulación.
# 'right', 'down', 'left', 'up' son las posibles direcciones.
# 'x' y 'y' son las coordenadas en el plano 2D de la simulación.
mid = {
    'right': {'x': 705, 'y': 445},
    'down': {'x': 695, 'y': 450},
    'left': {'x': 695, 'y': 425},
    'up': {'x': 695, 'y': 400}
}

# set random or default green signal time here
randomGreenSignalTimer = True
# set random green signal time range here
randomGreenSignalTimerRange = [10, 20]


# `timeElapsed` es una variable que lleva la cuenta del tiempo transcurrido en la simulación.
timeElapsed = 0

# `simulationTime` es la duración total de la simulación.
simulationTime = 300

# `timeElapsedCoods` son las coordenadas en la pantalla donde se mostrará el tiempo transcurrido.
timeElapsedCoods = (1100, 50)

# `vehicleCountTexts` es una lista que contiene el número de vehículos en cada dirección como cadenas de texto.
vehicleCountTexts = ["0", "0", "0", "0"]

# `vehicleCountCoods` son las coordenadas en la pantalla donde se mostrará el recuento de vehículos para cada dirección.
vehicleCountCoods = [(480, 210), (880, 210), (880, 550), (480, 550)]


# Pygame initialization
pygame.init()
simulation = pygame.sprite.Group()


class TrafficSignal:
    """
    La clase `TrafficSignal` en Python representa una señal de tráfico con duraciones de luz roja,
    amarilla y verde.

    """

    def __init__(self, red: int, yellow: int, green: int):
        """
        Esta función de Python inicializa un objeto con valores enteros para rojo, amarillo y verde, junto
        con una cadena vacía para signalText.

        """
        self.red = red
        self.yellow = yellow
        self.green = green
        self.signalText = ""


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane: int, vehicleClass: str, direction_number: int, direction: str, will_turn: int):
        """
        Esta función inicializa un objeto de vehículo con atributos y coordenadas específicos según la
        dirección y el carril.

        :param `lane` int: 
            Representa el carril en el que se encuentra el vehículo. 

        :param `vehicleClass` str:
            Representa la clase o tipodel vehículo que se está inicializando. 

        :param `direction_number` int: 
            Representa el valor numérico asociado con la dirección en la que se mueve el vehículo up,down... 

        :param `direction` str: 
            Representa la dirección en la que se mueve el vehículo. 

        :param `will_turn` int: 
            Representa si elvehículo girará o no. 

        """
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.vehicleClass = vehicleClass
        self.speed = speeds[vehicleClass]
        self.direction_number = direction_number
        self.direction = direction
        self.x = x[direction][lane]
        self.y = y[direction][lane]
        self.crossed = 0
        self.willTurn = will_turn
        self.turned = 0
        self.rotateAngle = 0
        vehicles[direction][lane].append(self)
        self.index = len(vehicles[direction][lane]) - 1
        self.crossedIndex = 0
        # path of vehicle image
        path = f"images/{direction}/{vehicleClass}.png"
        self.originalImage = pygame.image.load(path)
        self.image = pygame.image.load(path)
        previousVehicle = vehicles[direction][lane][self.index-1]
        self.image_width = self.image.get_rect().width
        self.image_height = self.image.get_rect().height

        # Set stopping coordinate
        if (len(vehicles[direction][lane]) > 1 and previousVehicle.crossed == 0):
            width = previousVehicle.image.get_rect().width
            height = previousVehicle.image.get_rect().height
            if (direction == 'right'):
                self.stop = previousVehicle.stop
                - width
                - stoppingGap
            elif (direction == 'left'):
                self.stop = previousVehicle.stop
                + width
                + stoppingGap
            elif (direction == 'down'):
                self.stop = previousVehicle.stop
                - height
                - stoppingGap
            elif (direction == 'up'):
                self.stop = previousVehicle.stop
                + height
                + stoppingGap
        else:
            self.stop = defaultStop[direction]

        # Set new starting and stopping coordinate
        if (direction == 'right'):
            temp = self.image_width + stoppingGap
            x[direction][lane] -= temp
        elif (direction == 'left'):
            temp = self.image_width + stoppingGap
            x[direction][lane] += temp
        elif (direction == 'down'):
            temp = self.image_height + stoppingGap
            y[direction][lane] -= temp
        elif (direction == 'up'):
            temp = self.image_height + stoppingGap
            y[direction][lane] += temp
        simulation.add(self)

    def render(self, screen):
        """
        La función `render` en Python toma un parámetro de `pantalla` y borra la `imagen` en las coordenadas
        `(x, y)`.

        :param screen: 
            Este parámetro se utiliza con el método `blit`
            para dibujar la imagen en las coordenadas especificadas `(self.x, self.y)` en la pantalla
        """
        screen.blit(self.image, (self.x, self.y))

    def Move_right(self):
        """
        La función `Move_right` en Python maneja el movimiento de vehículos en función de diversas
        condiciones, como cruzar líneas de parada, girar y mantener espacios entre vehículos.
        """
        if (self.crossed == 0 and self.x + self.image_width > stopLines[self.direction]):
            self.crossed = 1
            vehicles[self.direction]['crossed'] += 1
            if (self.willTurn == 0):
                vehiclesNotTurned[self.direction][self.lane].append(self)
                self.crossedIndex = len(
                    vehiclesNotTurned[self.direction][self.lane]) - 1
        if (self.willTurn == 1):
            last_Vehicule = vehicles[self.direction][self.lane][self.index-1]
            x_with_width = self.x + self.image_width
            last_vehicles_turned = vehiclesTurned[self.direction][self.lane][self.crossedIndex -
                                                                             1] if self.crossedIndex != 0 else None

            if self.lane == 1:
                if self.crossed == 0 or x_with_width < stopLines[self.direction]+40:
                    can_move_forward = x_with_width <= self.stop or (
                        currentGreen == 0 and currentYellow == 0) or self.crossed == 1
                    is_first_vehicle_or_has_gap = self.index == 0 or x_with_width < (
                        last_Vehicule.x - movingGap) or last_Vehicule.turned == 1

                    if can_move_forward and is_first_vehicle_or_has_gap:
                        self.x += self.speed
                else:
                    if self.turned == 0:
                        self.rotateAngle += rotationAngle
                        self.image = pygame.transform.rotate(
                            self.originalImage, self.rotateAngle)
                        self.x += 2.4
                        self.y -= 2.8

                        if self.rotateAngle == 90:
                            self.turned = 1
                            vehiclesTurned[self.direction][self.lane].append(
                                self)
                            self.crossedIndex = len(
                                vehiclesTurned[self.direction][self.lane]) - 1
                    else:
                        has_gap_to_previous_turned_vehicle = self.crossedIndex == 0 or self.y > (
                            last_vehicles_turned.y + last_vehicles_turned.image.get_rect().height + movingGap)

                        if has_gap_to_previous_turned_vehicle:
                            self.y -= self.speed
            elif self.lane == 2:
                x_with_width = self.x + self.image_width
                y_with_height = self.y + self.image_height

                if self.crossed == 0 or x_with_width < mid[self.direction]['x']:
                    can_move_forward = x_with_width <= self.stop or (
                        currentGreen == 0 and currentYellow == 0) or self.crossed == 1
                    is_first_vehicle_or_has_gap = self.index == 0 or x_with_width < (
                        last_Vehicule.x - movingGap) or last_Vehicule.turned == 1

                    if can_move_forward and is_first_vehicle_or_has_gap:
                        self.x += self.speed
                else:
                    if self.turned == 0:
                        self.rotateAngle += rotationAngle
                        self.image = pygame.transform.rotate(
                            self.originalImage, -self.rotateAngle)
                        self.x += 2
                        self.y += 1.8

                        if self.rotateAngle == 90:
                            self.turned = 1
                            vehiclesTurned[self.direction][self.lane].append(
                                self)
                            self.crossedIndex = len(
                                vehiclesTurned[self.direction][self.lane]) - 1
                    else:
                        has_gap_to_previous_turned_vehicle = self.crossedIndex == 0 or y_with_height < (
                            vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].y - movingGap)

                        if has_gap_to_previous_turned_vehicle:
                            self.y += self.speed
        else:
            if (self.crossed == 0):
                if ((self.x+self.image_width <= self.stop or (currentGreen == 0 and currentYellow == 0)) and (self.index == 0 or self.x+self.image_width < (vehicles[self.direction][self.lane][self.index-1].x - movingGap))):
                    self.x += self.speed
            else:
                if ((self.crossedIndex == 0) or (self.x+self.image_width < (vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].x - movingGap))):
                    self.x += self.speed

    def Move_down(self):
        """
        Esta función controla el movimiento de los vehículos en una simulación, incluido el manejo de cruces
        de intersecciones y giros.
        """
        if (self.crossed == 0 and self.y+self.image_height > stopLines[self.direction]):
            self.crossed = 1
            vehicles[self.direction]['crossed'] += 1
            if (self.willTurn == 0):
                vehiclesNotTurned[self.direction][self.lane].append(self)
                self.crossedIndex = len(
                    vehiclesNotTurned[self.direction][self.lane]) - 1
        if (self.willTurn == 1):
            if (self.lane == 1):
                if (self.crossed == 0 or self.y+self.image_height < stopLines[self.direction]+50):
                    if ((self.y+self.image_height <= self.stop or (currentGreen == 1 and currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.y+self.image_height < (vehicles[self.direction][self.lane][self.index-1].y - movingGap) or vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.y += self.speed
                else:
                    if (self.turned == 0):
                        self.rotateAngle += rotationAngle
                        self.image = pygame.transform.rotate(
                            self.originalImage, self.rotateAngle)
                        self.x += 1.2
                        self.y += 1.8
                        if (self.rotateAngle == 90):
                            self.turned = 1
                            vehiclesTurned[self.direction][self.lane].append(
                                self)
                            self.crossedIndex = len(
                                vehiclesTurned[self.direction][self.lane]) - 1
                    else:
                        if (self.crossedIndex == 0 or ((self.x + self.image_width) < (vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].x - movingGap))):
                            self.x += self.speed
            elif (self.lane == 2):
                if (self.crossed == 0 or self.y+self.image_height < mid[self.direction]['y']):
                    if ((self.y+self.image_height <= self.stop or (currentGreen == 1 and currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.y+self.image_height < (vehicles[self.direction][self.lane][self.index-1].y - movingGap) or vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.y += self.speed
                else:
                    if (self.turned == 0):
                        self.rotateAngle += rotationAngle
                        self.image = pygame.transform.rotate(
                            self.originalImage, -self.rotateAngle)
                        self.x -= 2.5
                        self.y += 2
                        if (self.rotateAngle == 90):
                            self.turned = 1
                            vehiclesTurned[self.direction][self.lane].append(
                                self)
                            self.crossedIndex = len(
                                vehiclesTurned[self.direction][self.lane]) - 1
                    else:
                        if (self.crossedIndex == 0 or (self.x > (vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].x + vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().width + movingGap))):
                            self.x -= self.speed
        else:
            if (self.crossed == 0):
                if ((self.y+self.image_height <= self.stop or (currentGreen == 1 and currentYellow == 0)) and (self.index == 0 or self.y+self.image_height < (vehicles[self.direction][self.lane][self.index-1].y - movingGap))):
                    self.y += self.speed
            else:
                if ((self.crossedIndex == 0) or (self.y+self.image_height < (vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].y - movingGap))):
                    self.y += self.speed

    def Move_left(self):
        """
        Esta función define el comportamiento de movimiento de un objeto de vehículo en una simulación,
        incluidas las condiciones para girar y cambiar de carril.
        """
        if (self.crossed == 0 and self.x < stopLines[self.direction]):
            self.crossed = 1
            vehicles[self.direction]['crossed'] += 1
            if (self.willTurn == 0):
                vehiclesNotTurned[self.direction][self.lane].append(self)
                self.crossedIndex = len(
                    vehiclesNotTurned[self.direction][self.lane]) - 1
        if (self.willTurn == 1):
            if (self.lane == 1):
                if (self.crossed == 0 or self.x > stopLines[self.direction]-70):
                    if ((self.x >= self.stop or (currentGreen == 2 and currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.x > (vehicles[self.direction][self.lane][self.index-1].x + vehicles[self.direction][self.lane][self.index-1].image.get_rect().width + movingGap) or vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.x -= self.speed
                else:
                    if (self.turned == 0):
                        self.rotateAngle += rotationAngle
                        self.image = pygame.transform.rotate(
                            self.originalImage, self.rotateAngle)
                        self.x -= 1
                        self.y += 1.2
                        if (self.rotateAngle == 90):
                            self.turned = 1
                            vehiclesTurned[self.direction][self.lane].append(
                                self)
                            self.crossedIndex = len(
                                vehiclesTurned[self.direction][self.lane]) - 1
                    else:
                        if (self.crossedIndex == 0 or ((self.y + self.image_height) < (vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].y - movingGap))):
                            self.y += self.speed
            elif (self.lane == 2):
                if (self.crossed == 0 or self.x > mid[self.direction]['x']):
                    if ((self.x >= self.stop or (currentGreen == 2 and currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.x > (vehicles[self.direction][self.lane][self.index-1].x + vehicles[self.direction][self.lane][self.index-1].image.get_rect().width + movingGap) or vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.x -= self.speed
                else:
                    if (self.turned == 0):
                        self.rotateAngle += rotationAngle
                        self.image = pygame.transform.rotate(
                            self.originalImage, -self.rotateAngle)
                        self.x -= 1.8
                        self.y -= 2.5
                        if (self.rotateAngle == 90):
                            self.turned = 1
                            vehiclesTurned[self.direction][self.lane].append(
                                self)
                            self.crossedIndex = len(
                                vehiclesTurned[self.direction][self.lane]) - 1
                    else:
                        if (self.crossedIndex == 0 or (self.y > (vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].y + vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().height + movingGap))):
                            self.y -= self.speed
        else:
            if (self.crossed == 0):
                if ((self.x >= self.stop or (currentGreen == 2 and currentYellow == 0)) and (self.index == 0 or self.x > (vehicles[self.direction][self.lane][self.index-1].x + vehicles[self.direction][self.lane][self.index-1].image.get_rect().width + movingGap))):
                    self.x -= self.speed
            else:
                if ((self.crossedIndex == 0) or (self.x > (vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].x + vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().width + movingGap))):
                    self.x -= self.speed

    def Move_up(self):
        """
        La función "Move_up" controla el movimiento vertical de los vehículos en función de diversas
        condiciones, como cruzar líneas, girar, carriles y señales de tráfico.
        """
        if (self.crossed == 0 and self.y < stopLines[self.direction]):
            self.crossed = 1
            vehicles[self.direction]['crossed'] += 1
            if (self.willTurn == 0):
                vehiclesNotTurned[self.direction][self.lane].append(self)
                self.crossedIndex = len(
                    vehiclesNotTurned[self.direction][self.lane]) - 1
        if (self.willTurn == 1):
            if (self.lane == 1):
                if (self.crossed == 0 or self.y > stopLines[self.direction]-60):
                    if ((self.y >= self.stop or (currentGreen == 3 and currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.y > (vehicles[self.direction][self.lane][self.index-1].y + vehicles[self.direction][self.lane][self.index-1].image.get_rect().height + movingGap) or vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.y -= self.speed
                else:
                    if (self.turned == 0):
                        self.rotateAngle += rotationAngle
                        self.image = pygame.transform.rotate(
                            self.originalImage, self.rotateAngle)
                        self.x -= 2
                        self.y -= 1.2
                        if (self.rotateAngle == 90):
                            self.turned = 1
                            vehiclesTurned[self.direction][self.lane].append(
                                self)
                            self.crossedIndex = len(
                                vehiclesTurned[self.direction][self.lane]) - 1
                    else:
                        if (self.crossedIndex == 0 or (self.x > (vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].x + vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().width + movingGap))):
                            self.x -= self.speed
            elif (self.lane == 2):
                if (self.crossed == 0 or self.y > mid[self.direction]['y']):
                    if ((self.y >= self.stop or (currentGreen == 3 and currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.y > (vehicles[self.direction][self.lane][self.index-1].y + vehicles[self.direction][self.lane][self.index-1].image.get_rect().height + movingGap) or vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.y -= self.speed
                else:
                    if (self.turned == 0):
                        self.rotateAngle += rotationAngle
                        self.image = pygame.transform.rotate(
                            self.originalImage, -self.rotateAngle)
                        self.x += 1
                        self.y -= 1
                        if (self.rotateAngle == 90):
                            self.turned = 1
                            vehiclesTurned[self.direction][self.lane].append(
                                self)
                            self.crossedIndex = len(
                                vehiclesTurned[self.direction][self.lane]) - 1
                    else:
                        if (self.crossedIndex == 0 or (self.x < (vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].x - vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().width - movingGap))):
                            self.x += self.speed
        else:
            if (self.crossed == 0):
                if ((self.y >= self.stop or (currentGreen == 3 and currentYellow == 0)) and (self.index == 0 or self.y > (vehicles[self.direction][self.lane][self.index-1].y + vehicles[self.direction][self.lane][self.index-1].image.get_rect().height + movingGap))):
                    self.y -= self.speed
            else:
                if ((self.crossedIndex == 0) or (self.y > (vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].y + vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().height + movingGap))):
                    self.y -= self.speed

    def move(self):
        """
        La función `move` en Python selecciona una dirección de movimiento basada en un diccionario y llama
        al método correspondiente.
        """
        directios = {
            'right': self.Move_right,
            'down': self.Move_down,
            'left': self.Move_left,
            'up': self.Move_up
        }
        directios[self.direction]()

# Initialization of signals with default values


def initialize():
    """
    Esta función inicializa las señales de tráfico con valores aleatorios o predeterminados del
    temporizador de señal verde.
    """
    minTime = randomGreenSignalTimerRange[0]
    maxTime = randomGreenSignalTimerRange[1]
    if (randomGreenSignalTimer):
        ts1 = TrafficSignal(0, defaultYellow, random.randint(minTime, maxTime))
        signals.append(ts1)
        ts2 = TrafficSignal(ts1.red+ts1.yellow+ts1.green,
                            defaultYellow, random.randint(minTime, maxTime))
        signals.append(ts2)
        ts3 = TrafficSignal(defaultRed, defaultYellow,
                            random.randint(minTime, maxTime))
        signals.append(ts3)
        ts4 = TrafficSignal(defaultRed, defaultYellow,
                            random.randint(minTime, maxTime))
        signals.append(ts4)
    else:
        ts1 = TrafficSignal(0, defaultYellow, defaultGreen[0])
        signals.append(ts1)
        ts2 = TrafficSignal(ts1.yellow+ts1.green,
                            defaultYellow, defaultGreen[1])
        signals.append(ts2)
        ts3 = TrafficSignal(defaultRed, defaultYellow, defaultGreen[2])
        signals.append(ts3)
        ts4 = TrafficSignal(defaultRed, defaultYellow, defaultGreen[3])
        signals.append(ts4)
    repeat()

# Print the signal timers on cmd


def printStatus():
    """
    Esta función recorre en iteración una lista de señales e imprime su estado según su color y estado
    actual.
    """
    for i in range(0, 4):
        if (signals[i] != None):
            if (i == currentGreen):
                if (currentYellow == 0):
                    print(" GREEN TS", i+1, "-> r:",
                          signals[i].red, " y:", signals[i].yellow, " g:", signals[i].green)
                else:
                    print("YELLOW TS", i+1, "-> r:",
                          signals[i].red, " y:", signals[i].yellow, " g:", signals[i].green)
            else:
                print("   RED TS", i+1, "-> r:",
                      signals[i].red, " y:", signals[i].yellow, " g:", signals[i].green)
    print()


def repeat():
    """
    Esta función de Python controla los tiempos de las señales de tráfico y las transiciones entre las
    señales verdes, amarillas y rojas en un bucle.
    """
    global currentGreen, currentYellow, nextGreen
    # while the timer of current green signal is not zero
    while (signals[currentGreen].green > 0):
        printStatus()
        updateValues()
        time.sleep(1)
    currentYellow = 1   # set yellow signal on
    # reset stop coordinates of lanes and vehicles
    for i in range(0, 3):
        for vehicle in vehicles[directionNumbers[currentGreen]][i]:
            vehicle.stop = defaultStop[directionNumbers[currentGreen]]
    # while the timer of current yellow signal is not zero
    while (signals[currentGreen].yellow > 0):
        printStatus()
        updateValues()
        time.sleep(1)
    currentYellow = 0   # set yellow signal off

    # reset all signal times of current signal to default/random times
    if (randomGreenSignalTimer):
        signals[currentGreen].green = random.randint(
            randomGreenSignalTimerRange[0], randomGreenSignalTimerRange[1])
    else:
        signals[currentGreen].green = defaultGreen[currentGreen]
    signals[currentGreen].yellow = defaultYellow
    signals[currentGreen].red = defaultRed

    currentGreen = nextGreen  # set next signal as green signal
    nextGreen = (currentGreen+1) % noOfSignals    # set next green signal
    # set the red time of next to next signal as (yellow time + green time) of next signal
    signals[nextGreen].red = signals[currentGreen].yellow + \
        signals[currentGreen].green
    repeat()


# Update values of the signal timers after every second
def updateValues():
    """
    La función `updateValues` itera a través de un rango de señales y disminuye sus valores verde,
    amarillo o rojo según ciertas condiciones.
    """
    for i in range(0, noOfSignals):
        if (i == currentGreen):
            if (currentYellow == 0):
                signals[i].green -= 1
            else:
                signals[i].yellow -= 1
        else:
            signals[i].red -= 1


# Generating vehicles in the simulation
def generateVehicles():
    """
    La función "generar vehículos" selecciona aleatoriamente tipos de vehículos, números de carril,
    probabilidades de giro e indicaciones para crear vehículos en intervalos de 1 segundo.
    """
    while True:
        vehicle_type = random.choice(allowedVehicleTypesList)
        lane_number = random.randint(1, 2)
        will_turn = random.randint(0, 99) < 40 if lane_number in [1, 2] else 0

        temp = random.randint(0, 99)
        dist = [25, 50, 75, 100]
        direction_number = next(i for i, val in enumerate(dist) if temp < val)

        Vehicle(lane_number, vehicleTypes[vehicle_type], direction_number,
                directionNumbers[direction_number], will_turn)
        time.sleep(1)


def showStats():
    """
    La función `showStats` calcula y muestra el número total de vehículos que han cruzado en cada
    dirección y el tiempo total transcurrido.
    """
    totalVehicles = 0
    print('Direction-wise Vehicle Counts')
    for i in range(0, 4):
        if (signals[i] != None):
            print('Direction', i+1, ':',
                  vehicles[directionNumbers[i]]['crossed'])
            totalVehicles += vehicles[directionNumbers[i]]['crossed']
    print('Total vehicles passed:', totalVehicles)
    print('Total time:', timeElapsed)


def simTime():
    """
    La función `simTime` incrementa `timeElapsed` en 1 cada segundo hasta llegar a `simulationTime`,
    momento en el que muestra estadísticas y sale del programa.
    """
    global timeElapsed, simulationTime
    while (True):
        timeElapsed += 1
        time.sleep(1)
        if (timeElapsed == simulationTime):
            showStats()
            os._exit(1)


class Main:
    global allowedVehicleTypesList
    i = 0
    for vehicleType in allowedVehicleTypes:
        if (allowedVehicleTypes[vehicleType]):
            allowedVehicleTypesList.append(i)
        i += 1
    thread1 = threading.Thread(
        name="initialization", target=initialize, args=())    # initialization
    thread1.daemon = True
    thread1.start()

    # Colours
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Screensize
    screenWidth = 1400
    screenHeight = 800
    screenSize = (screenWidth, screenHeight)

    # Setting background image i.e. image of intersection
    background = pygame.image.load('images/intersection.png')

    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("SIMULATION")

    # Loading signal images and font
    redSignal = pygame.image.load('images/signals/red.png')
    yellowSignal = pygame.image.load('images/signals/yellow.png')
    greenSignal = pygame.image.load('images/signals/green.png')
    font = pygame.font.Font(None, 30)

    # threads (hilos de ejecucion) for generating vehicles and time of simulation

    # Generating vehicles
    thread2 = threading.Thread(
        name="generateVehicles", target=generateVehicles, args=())
    thread2.daemon = True
    thread2.start()

    # Time of simulation
    thread3 = threading.Thread(name="simTime", target=simTime, args=())
    thread3.daemon = True
    thread3.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                showStats()
                sys.exit()

        screen.blit(background, (0, 0))   # display background in simulation

        # display signal and set timer according to current status: green, yello, or red
        for i in range(0, noOfSignals):
            if (i == currentGreen):
                if (currentYellow == 1):
                    signals[i].signalText = signals[i].yellow
                    screen.blit(yellowSignal, signalCoods[i])
                else:
                    signals[i].signalText = signals[i].green
                    screen.blit(greenSignal, signalCoods[i])
            else:
                if (signals[i].red <= 10):
                    signals[i].signalText = signals[i].red
                else:
                    signals[i].signalText = "---"
                screen.blit(redSignal, signalCoods[i])
        signalTexts = ["", "", "", ""]

        # display signal timer
        for i in range(0, noOfSignals):
            signalTexts[i] = font.render(
                str(signals[i].signalText), True, white, black)
            screen.blit(signalTexts[i], signalTimerCoods[i])

        # display vehicle count
        for i in range(0, noOfSignals):
            displayText = vehicles[directionNumbers[i]]['crossed']
            vehicleCountTexts[i] = font.render(
                str(displayText), True, black, white)
            screen.blit(vehicleCountTexts[i], vehicleCountCoods[i])

        # display time elapsed
        timeElapsedText = font.render(
            ("Time Elapsed: "+str(timeElapsed)), True, black, white)
        screen.blit(timeElapsedText, timeElapsedCoods)

        # display the vehicles
        for vehicle in simulation:
            screen.blit(vehicle.image, [vehicle.x, vehicle.y])
            vehicle.move()
        pygame.display.update()
