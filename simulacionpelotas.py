import time
import pygame
import math

gameLength = 800
gameWidth = 800


lastFrameTime = time.time()
pelotas = []
white = (255, 255, 255)
black = (0, 0, 0)


pygame.init()
screen = pygame.display.set_mode([gameLength, gameWidth])


def anguloVector(vector):
    return(math.degrees(math.atan2(vector.y, vector.x)))

a = pygame.Vector2(-5, 1)
print(anguloVector(a))

class Sphere:
    def __init__(self, posicion, masa, ):

        pixelsPorKilo = (5 ** 2 * math.pi) / 1
        self.masa = masa
        self.radio = math.sqrt((pixelsPorKilo * self.masa) / math.pi)
        self.posicion = posicion
        self.velocidad = pygame.Vector2(0, 0)




    
    def addForce(self, fuerza):
        
        self.velocidad = self.velocidad + fuerza / self.masa


    def Update(self):

        self.posicion = self.posicion + self.velocidad * deltaTime




running = True
while running:
    deltaTime = time.time() - lastFrameTime
    lastFrameTime = time.time()
