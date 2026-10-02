import pygame
import math
import random

gameLength = 1400
gameWidth = 800

white = (255, 255, 255)
black = (0, 0, 0)

ballArray = []

pygame.init()
screen = pygame.display.set_mode([gameLength, gameWidth])


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.module = math.sqrt(x**2 + y**2)
    
    def __add__(self, other):
        return(Vector2(self.x + other.x, self.y + other.y))

    def __sub__(self, other):
        return(Vector2(self.x - other.x, self.y - other.y))

    def __mul__(self, other):
        return(Vector2(self.x * other, self.y * other))

    def normalize(self):
        return(Vector2(self.x / self.module, self.y / self.module))

    def turn(self, radian):
        newRadian = math.atan2(self.y, self.x) + radian
        self.x = math.cos(newRadian) * self.module
        self.y = math.sin (newRadian) * self.module


class Ball:
    def __init__(self, mass, position, velocity):
        ballArray.append(self)
        self.mass = mass
        self.radius = math.sqrt(mass / math.pi)
        self.position = position
        self.velocity = velocity
        self.forcesAddedToNextFrame = Vector2(0, 0)

    def update(self):
        self.position = self.position + self.velocity * 0.1
        if self.position.x + self.radius > gameLength or self.position.x - self.radius < 0:
            self.velocity.x = self.velocity.x * -1
        if self.position.y + self.radius > gameWidth or self.position.y - self.radius < 0:
            self.velocity.y = self.velocity.y * -1
        for ball in ballArray:
            if ball != self and math.sqrt((self.position.x - ball.position.x) ** 2 + (self.position.y - ball.position.y) ** 2) < self.radius + ball.radius:
                self.position = self.position - self.velocity.normalize() * 5
                hitAngle = math.atan2((ball.position.y - self.position.y), (ball.position.x - self.position.x))
                forcesVector = self.velocity - ball.velocity
                forcesVector.turn(-hitAngle)
                forceToOtherBall = Vector2(forcesVector.x, 0) * self.mass
                forceToOtherBall.turn(hitAngle)
                ball.forcesAddedToNextFrame = ball.forcesAddedToNextFrame + forceToOtherBall 
                self.velocity = self.velocity - forceToOtherBall * (1 / self.mass)

    def addForces(self):
        self.velocity = self.velocity + self.forcesAddedToNextFrame * (1 / self.mass)
        self.forcesAddedToNextFrame = Vector2(0, 0)


    def draw(self):
        pygame.draw.circle(screen, white, [self.position.x, self.position.y], self.radius, 0)


#ball = Ball(5000, Vector2(100, 400), Vector2(0, 0))

#ball2 = Ball(500, Vector2(1300, 400), Vector2(40, 0))

for x in range(12):
    for y in range(6):
        ballArray.append(Ball(1000, Vector2(x * 100 + 100, y * 100 + 100), Vector2(random.randint(-20, 20), random.randint(-20, 20))))


f = 1
running = True
while running == True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    #font = pygame.font.SysFont(None, 24)
    #img = font.render('hello', True, white)
    #screen.blit(img, (20, 20))

    print(f)
    f = f + 1
    screen.fill(black)
    for ball in ballArray:
        ball.draw()
    pygame.display.flip()
    for ball in ballArray:
        ball.update()
    for ball in ballArray:
        ball.addForces()