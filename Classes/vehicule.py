import pygame

stoppingGap = 25    # stopping gap
movingGap = 25   # moving gap


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, x: dict[str, list[int]], y: dict[str, list[int]], vehicles: dict, speeds: dict[str, float], mid: dict, stopLines: dict, lane: int, vehicleClass: str, direction_number: int, direction: str, will_turn: int, *args):
        pygame.sprite.Sprite.__init__(self)

        # String Variables
        self.vehicleClass = vehicleClass
        self.direction_number = direction_number
        self.direction = direction
        self.vehicles = vehicles
        # int Variables
        self.lane = lane
        self.x = x[self.direction][self.lane]
        self.y = y[self.direction][self.lane]
        self.crossed = 0
        self.willTurn = will_turn
        self.turned = 0
        self.rotateAngle = 0
        self.rotationAngle = 3
        self.currentGreen = 0
        self.currentYellow = 0
        self.index = len(self.vehicles[direction][lane]) - 1
        # Float Variables
        self.speed = speeds[vehicleClass]
        # dict
        self.stopLines = stopLines
        self.simulation = args[0]
        self.defaultStop = {'right': 580, 'down': 320, 'left': 810, 'up': 545}
        self.vehiclesNotTurned = {'right': {1: [], 2: []}, 'down': {
            1: [], 2: []}, 'left': {1: [], 2: []}, 'up': {1: [], 2: []}}
        self.vehicles[direction][lane].append(self)
        self.mid = mid
        self.crossedIndex = 0
        # image
        path = f"images/{direction}/{vehicleClass}.png"
        self.originalImage = pygame.image.load(path)
        self.image = pygame.image.load(path)

        if (len(self.vehicles[direction][lane]) > 1 and self.vehicles[direction][lane][self.index-1].crossed == 0):
            if (direction == 'right'):
                self.stop = self.vehicles[direction][lane][self.index-1].stop
                - self.vehicles[direction][lane][self.index -
                                                 1].image.get_rect().width
                - stoppingGap
            elif (direction == 'left'):
                self.stop = self.vehicles[direction][lane][self.index-1].stop
                + self.vehicles[direction][lane][self.index -
                                                 1].image.get_rect().width
                + stoppingGap
            elif (direction == 'down'):
                self.stop = self.vehicles[direction][lane][self.index-1].stop
                - self.vehicles[direction][lane][self.index -
                                                 1].image.get_rect().height
                - stoppingGap
            elif (direction == 'up'):
                self.stop = self.vehicles[direction][lane][self.index-1].stop
                + self.vehicles[direction][lane][self.index -
                                                 1].image.get_rect().height
                + stoppingGap
        else:
            self.stop = self.defaultStop[direction]

        # Set new starting and stopping coordinate
        if (direction == 'right'):
            temp = self.image.get_rect().width + stoppingGap
            x[direction][lane] -= temp
        elif (direction == 'left'):
            temp = self.image.get_rect().width + stoppingGap
            x[direction][lane] += temp
        elif (direction == 'down'):
            temp = self.image.get_rect().height + stoppingGap
            y[direction][lane] -= temp
        elif (direction == 'up'):
            temp = self.image.get_rect().height + stoppingGap
            y[direction][lane] += temp
        self.simulation.add(self)

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def Move_right(self):
        if (self.crossed == 0 and self.x+self.image.get_rect().width > self.stopLines[self.direction]):
            self.crossed = 1
            self.vehicles[self.direction]['crossed'] += 1
            if (self.willTurn == 0):
                self.vehiclesNotTurned[self.direction][self.lane].append(
                    self)
                self.crossedIndex = len( 
                    self.vehiclesNotTurned[self.direction][self.lane]) - 1
        if (self.willTurn == 1):
            if (self.lane == 1):
                if (self.crossed == 0 or self.x+self.image.get_rect().width < self.stopLines[self.direction]+40):
                    if ((self.x+self.image.get_rect().width <= self.stop or (self.currentGreen == 0 and self.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.x+self.image.get_rect().width < (self.vehicles[self.direction][self.lane][self.index-1].x - movingGap) or self.vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.x += self.speed
                else:
                    if (self.turned == 0):
                        self.rotateAngle += self.rotationAngle
                        self.image = pygame.transform.rotate(
                            self.originalImage, self.rotateAngle)
                        self.x += 2.4
                        self.y -= 2.8
                        if (self.rotateAngle == 90):
                            self.turned = 1
                            self.vehiclesTurned[self.direction][self.lane].append(
                                self)
                            self.crossedIndex = len(
                                self.vehiclesTurned[self.direction][self.lane]) - 1
                    else:
                        if (self.crossedIndex == 0 or (self.y > (self.vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].y + self.vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().height + movingGap))):
                            self.y -= self.speed
            elif (self.lane == 2):
                if (self.crossed == 0 or self.x+self.image.get_rect().width < self.mid[self.direction]['x']):
                    if ((self.x+self.image.get_rect().width <= self.stop or (self.currentGreen == 0 and self.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.x+self.image.get_rect().width < (self.vehicles[self.direction][self.lane][self.index-1].x - movingGap) or self.vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.x += self.speed
                else:
                    if (self.turned == 0):
                        self.rotateAngle += self.rotationAngle
                        self.image = pygame.transform.rotate(
                            self.originalImage, -self.rotateAngle)
                        self.x += 2
                        self.y += 1.8
                        if (self.rotateAngle == 90):
                            self.turned = 1
                            self.vehiclesTurned[self.direction][self.lane].append(
                                self)
                            self.crossedIndex = len(
                                self.vehiclesTurned[self.direction][self.lane]) - 1
                    else:
                        if (self.crossedIndex == 0 or ((self.y+self.image.get_rect().height) < (self.vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].y - movingGap))):
                            self.y += self.speed
        else:
            if (self.crossed == 0):
                if ((self.x+self.image.get_rect().width <= self.stop or (self.currentGreen == 0 and self.currentYellow == 0)) and (self.index == 0 or self.x+self.image.get_rect().width < (self.vehicles[self.direction][self.lane][self.index-1].x - movingGap))):
                    self.x += self.speed
            else:
                if ((self.crossedIndex == 0) or (self.x+self.image.get_rect().width < (self.vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].x - movingGap))):
                    self.x += self.speed

    def Move_down(self):
        if (self.crossed == 0 and self.y+self.image.get_rect().height > self.stopLines[self.direction]):
            self.crossed = 1
            self.vehicles[self.direction]['crossed'] += 1
            if (self.willTurn == 0):
                self.vehiclesNotTurned[self.direction][self.lane].append(
                    self)
                self.crossedIndex = len(
                    self.vehiclesNotTurned[self.direction][self.lane]) - 1
        if (self.willTurn == 1):
            if (self.lane == 1):
                if (self.crossed == 0 or self.y+self.image.get_rect().height < self.stopLines[self.direction]+50):
                    if ((self.y+self.image.get_rect().height <= self.stop or (self.currentGreen == 1 and self.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.y+self.image.get_rect().height < (self.vehicles[self.direction][self.lane][self.index-1].y - movingGap) or self.vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.y += self.speed
                else:
                    if (self.turned == 0):
                        self.rotateAngle += self.rotationAngle
                        self.image = pygame.transform.rotate(
                            self.originalImage, self.rotateAngle)
                        self.x += 1.2
                        self.y += 1.8
                        if (self.rotateAngle == 90):
                            self.turned = 1
                            self.vehiclesTurned[self.direction][self.lane].append(
                                self)
                            self.crossedIndex = len(
                                self.vehiclesTurned[self.direction][self.lane]) - 1
                    else:
                        if (self.crossedIndex == 0 or ((self.x + self.image.get_rect().width) < (self.vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].x - movingGap))):
                            self.x += self.speed
            elif (self.lane == 2):
                if (self.crossed == 0 or self.y+self.image.get_rect().height < self.mid[self.direction]['y']):
                    if ((self.y+self.image.get_rect().height <= self.stop or (self.currentGreen == 1 and self.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.y+self.image.get_rect().height < (self.vehicles[self.direction][self.lane][self.index-1].y - movingGap) or self.vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.y += self.speed
                else:
                    if (self.turned == 0):
                        self.rotateAngle += self.rotationAngle
                        self.image = pygame.transform.rotate(
                            self.originalImage, -self.rotateAngle)
                        self.x -= 2.5
                        self.y += 2
                        if (self.rotateAngle == 90):
                            self.turned = 1
                            self.vehiclesTurned[self.direction][self.lane].append(
                                self)
                            self.crossedIndex = len(
                                self.vehiclesTurned[self.direction][self.lane]) - 1
                    else:
                        if (self.crossedIndex == 0 or (self.x > (self.vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].x + self.vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().width + movingGap))):
                            self.x -= self.speed
        else:
            if (self.crossed == 0):
                if ((self.y+self.image.get_rect().height <= self.stop or (self.currentGreen == 1 and self.currentYellow == 0)) and (self.index == 0 or self.y+self.image.get_rect().height < (self.vehicles[self.direction][self.lane][self.index-1].y - movingGap))):
                    self.y += self.speed
            else:
                if ((self.crossedIndex == 0) or (self.y+self.image.get_rect().height < (self.vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].y - movingGap))):
                    self.y += self.speed

    def Move_left(self):
        if (self.crossed == 0 and self.x < self.stopLines[self.direction]):
            self.crossed = 1
            self.vehicles[self.direction]['crossed'] += 1
            if (self.willTurn == 0):
                self.vehiclesNotTurned[self.direction][self.lane].append(
                    self)
                self.crossedIndex = len(
                    self.vehiclesNotTurned[self.direction][self.lane]) - 1
        if (self.willTurn == 1):
            if (self.lane == 1):
                if (self.crossed == 0 or self.x > self.stopLines[self.direction]-70):
                    if ((self.x >= self.stop or (self.currentGreen == 2 and self.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.x > (self.vehicles[self.direction][self.lane][self.index-1].x + self.vehicles[self.direction][self.lane][self.index-1].image.get_rect().width + movingGap) or self.vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.x -= self.speed
                else:
                    if (self.turned == 0):
                        self.rotateAngle += self.rotationAngle
                        self.image = pygame.transform.rotate(
                            self.originalImage, self.rotateAngle)
                        self.x -= 1
                        self.y += 1.2
                        if (self.rotateAngle == 90):
                            self.turned = 1
                            self.vehiclesTurned[self.direction][self.lane].append(
                                self)
                            self.crossedIndex = len(
                                self.vehiclesTurned[self.direction][self.lane]) - 1
                    else:
                        if (self.crossedIndex == 0 or ((self.y + self.image.get_rect().height) < (self.vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].y - movingGap))):
                            self.y += self.speed
            elif (self.lane == 2):
                if (self.crossed == 0 or self.x > self.mid[self.direction]['x']):
                    if ((self.x >= self.stop or (self.currentGreen == 2 and self.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.x > (self.vehicles[self.direction][self.lane][self.index-1].x + self.vehicles[self.direction][self.lane][self.index-1].image.get_rect().width + movingGap) or self.vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.x -= self.speed
                else:
                    if (self.turned == 0):
                        self.rotateAngle += self.rotationAngle
                        self.image = pygame.transform.rotate(
                            self.originalImage, -self.rotateAngle)
                        self.x -= 1.8
                        self.y -= 2.5
                        if (self.rotateAngle == 90):
                            self.turned = 1
                            self.vehiclesTurned[self.direction][self.lane].append(
                                self)
                            self.crossedIndex = len(
                                self.vehiclesTurned[self.direction][self.lane]) - 1
                    else:
                        if (self.crossedIndex == 0 or (self.y > (self.vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].y + self.vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().height + movingGap))):
                            self.y -= self.speed
        else:
            if (self.crossed == 0):
                if ((self.x >= self.stop or (self.currentGreen == 2 and self.currentYellow == 0)) and (self.index == 0 or self.x > (self.vehicles[self.direction][self.lane][self.index-1].x + self.vehicles[self.direction][self.lane][self.index-1].image.get_rect().width + movingGap))):
                    self.x -= self.speed
            else:
                if ((self.crossedIndex == 0) or (self.x > (self.vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].x + self.vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().width + movingGap))):
                    self.x -= self.speed

    def Move_up(self):
        if (self.crossed == 0 and self.y < self.stopLines[self.direction]):
            self.crossed = 1
            self.vehicles[self.direction]['crossed'] += 1
            if (self.willTurn == 0):
                self.vehiclesNotTurned[self.direction][self.lane].append(
                    self)
                self.crossedIndex = len(
                    self.vehiclesNotTurned[self.direction][self.lane]) - 1
        if (self.willTurn == 1):
            if (self.lane == 1):
                if (self.crossed == 0 or self.y > self.stopLines[self.direction]-60):
                    if ((self.y >= self.stop or (self.currentGreen == 3 and self.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.y > (self.vehicles[self.direction][self.lane][self.index-1].y + self.vehicles[self.direction][self.lane][self.index-1].image.get_rect().height + movingGap) or self.vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.y -= self.speed
                else:
                    if (self.turned == 0):
                        self.rotateAngle += self.rotationAngle
                        self.image = pygame.transform.rotate(
                            self.originalImage, self.rotateAngle)
                        self.x -= 2
                        self.y -= 1.2
                        if (self.rotateAngle == 90):
                            self.turned = 1
                            self.vehiclesTurned[self.direction][self.lane].append(
                                self)
                            self.crossedIndex = len(
                                self.vehiclesTurned[self.direction][self.lane]) - 1
                    else:
                        if (self.crossedIndex == 0 or (self.x > (self.vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].x + self.vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().width + movingGap))):
                            self.x -= self.speed
            elif (self.lane == 2):
                if (self.crossed == 0 or self.y > self.mid[self.direction]['y']):
                    if ((self.y >= self.stop or (self.currentGreen == 3 and self.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.y > (self.vehicles[self.direction][self.lane][self.index-1].y + self.vehicles[self.direction][self.lane][self.index-1].image.get_rect().height + movingGap) or self.vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.y -= self.speed
                else:
                    if (self.turned == 0):
                        self.rotateAngle += self.rotationAngle
                        self.image = pygame.transform.rotate(
                            self.originalImage, -self.rotateAngle)
                        self.x += 1
                        self.y -= 1
                        if (self.rotateAngle == 90):
                            self.turned = 1
                            self.vehiclesTurned[self.direction][self.lane].append(
                                self)
                            self.crossedIndex = len(
                                self.vehiclesTurned[self.direction][self.lane]) - 1
                    else:
                        if (self.crossedIndex == 0 or (self.x < (self.vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].x - self.vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().width - movingGap))):
                            self.x += self.speed
        else:
            if (self.crossed == 0):
                if ((self.y >= self.stop or (self.currentGreen == 3 and self.currentYellow == 0)) and (self.index == 0 or self.y > (self.vehicles[self.direction][self.lane][self.index-1].y + self.vehicles[self.direction][self.lane][self.index-1].image.get_rect().height + movingGap))):
                    self.y -= self.speed
            else:
                if ((self.crossedIndex == 0) or (self.y > (self.vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].y + self.vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().height + movingGap))):
                    self.y -= self.speed

    def move(self):
        directios = {
            'right': self.Move_right,
            'down': self.Move_down,
            'left': self.Move_left,
            'up': self.Move_up
        }
        directios[self.direction]()

    def Move2(self):
        if (self.direction == 'right'):
            if (self.crossed == 0 and self.x+self.image.get_rect().width > self.stopLines[self.direction]):
                self.crossed = 1
                self.vehicles[self.direction]['crossed'] += 1
                if (self.willTurn == 0):
                    self.vehiclesNotTurned[self.direction][self.lane].append(
                        self)
                    self.crossedIndex = len(
                        self.vehiclesNotTurned[self.direction][self.lane]) - 1
            if (self.willTurn == 1):
                if (self.lane == 1):
                    if (self.crossed == 0 or self.x+self.image.get_rect().width < self.stopLines[self.direction]+40):
                        if ((self.x+self.image.get_rect().width <= self.stop or (self.currentGreen == 0 and self.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.x+self.image.get_rect().width < (self.vehicles[self.direction][self.lane][self.index-1].x - movingGap) or self.vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                            self.x += self.speed
                    else:
                        if (self.turned == 0):
                            self.rotateAngle += self.rotationAngle
                            self.image = pygame.transform.rotate(
                                self.originalImage, self.rotateAngle)
                            self.x += 2.4
                            self.y -= 2.8
                            if (self.rotateAngle == 90):
                                self.turned = 1
                                self.vehiclesTurned[self.direction][self.lane].append(
                                    self)
                                self.crossedIndex = len(
                                    self.vehiclesTurned[self.direction][self.lane]) - 1
                        else:
                            if (self.crossedIndex == 0 or (self.y > (self.vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].y + self.vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().height + movingGap))):
                                self.y -= self.speed
                elif (self.lane == 2):
                    if (self.crossed == 0 or self.x+self.image.get_rect().width < self.mid[self.direction]['x']):
                        if ((self.x+self.image.get_rect().width <= self.stop or (self.currentGreen == 0 and self.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.x+self.image.get_rect().width < (self.vehicles[self.direction][self.lane][self.index-1].x - movingGap) or self.vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                            self.x += self.speed
                    else:
                        if (self.turned == 0):
                            self.rotateAngle += self.rotationAngle
                            self.image = pygame.transform.rotate(
                                self.originalImage, -self.rotateAngle)
                            self.x += 2
                            self.y += 1.8
                            if (self.rotateAngle == 90):
                                self.turned = 1
                                self.vehiclesTurned[self.direction][self.lane].append(
                                    self)
                                self.crossedIndex = len(
                                    self.vehiclesTurned[self.direction][self.lane]) - 1
                        else:
                            if (self.crossedIndex == 0 or ((self.y+self.image.get_rect().height) < (self.vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].y - movingGap))):
                                self.y += self.speed
            else:
                if (self.crossed == 0):
                    if ((self.x+self.image.get_rect().width <= self.stop or (self.currentGreen == 0 and self.currentYellow == 0)) and (self.index == 0 or self.x+self.image.get_rect().width < (self.vehicles[self.direction][self.lane][self.index-1].x - movingGap))):
                        self.x += self.speed
                else:
                    if ((self.crossedIndex == 0) or (self.x+self.image.get_rect().width < (self.vehiclesNotTurned[self.direction][self.lane][self.crossedIndex-1].x - movingGap))):
                        self.x += self.speed
                        
        elif (self.direction == 'down'):
            if (self.crossed == 0 and self.y+self.image.get_rect().height > self.stopLines[self.direction]):
                self.crossed = 1
                self.vehicles[self.direction]['crossed'] += 1
                if (self.willTurn == 0):
                    self.vehiclesNotTurned[self.direction][self.lane].append(
                        self)
                    self.crossedIndex = len(
                        self.vehiclesNotTurned[self.direction][self.lane]) - 1
            if (self.willTurn == 1):
                if (self.lane == 1):
                    if (self.crossed == 0 or self.y+self.image.get_rect().height < self.stopLines[self.direction]+50):
                        if ((self.y+self.image.get_rect().height <= self.stop or (self.currentGreen == 1 and self.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.y+self.image.get_rect().height < (self.vehicles[self.direction][self.lane][self.index-1].y - movingGap) or self.vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                            self.y += self.speed
                    else:
                        if (self.turned == 0):
                            self.rotateAngle += self.rotationAngle
                            self.image = pygame.transform.rotate(
                                self.originalImage, self.rotateAngle)
                            self.x += 1.2
                            self.y += 1.8
                            if (self.rotateAngle == 90):
                                self.turned = 1
                                self.vehiclesTurned[self.direction][self.lane].append(
                                    self)
                                self.crossedIndex = len(
                                    self.vehiclesTurned[self.direction][self.lane]) - 1
                        else:
                            if (self.crossedIndex == 0 or ((self.x + self.image.get_rect().width) < (self.vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].x - movingGap))):
                                self.x += self.speed
                elif (self.lane == 2):
                    if (self.crossed == 0 or self.y+self.image.get_rect().height < self.mid[self.direction]['y']):
                        if ((self.y+self.image.get_rect().height <= self.stop or (self.currentGreen == 1 and self.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.y+self.image.get_rect().height < (self.vehicles[self.direction][self.lane][self.index-1].y - movingGap) or self.vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                            self.y += self.speed
                    else:
                        if (self.turned == 0):
                            self.rotateAngle += self.rotationAngle
                            self.image = pygame.transform.rotate(
                                self.originalImage, -self.rotateAngle)
                            self.x -= 2.5
                            self.y += 2
                            if (self.rotateAngle == 90):
                                self.turned = 1
                                self.vehiclesTurned[self.direction][self.lane].append(
                                    self)
                                self.crossedIndex = len(
                                    self.vehiclesTurned[self.direction][self.lane]) - 1
                        else:
                            if (self.crossedIndex == 0 or (self.x > (self.vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].x + self.vehiclesTurned[self.direction][self.lane][self.crossedIndex-1].image.get_rect().width + movingGap))):
                                self.x -= self.speed
