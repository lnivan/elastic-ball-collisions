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

    def EM(self, other):
        return(self.x * other.x + self.y * other.y)

    def normalize(self):
        return(Vector2(self.x / self.module, self.y / self.module))

    def turn(self, radian):
        newRadian = math.atan2(self.y, self.x) + radian
        self.x = math.cos(newRadian) * self.module
        self.y = math.sin (newRadian) * self.module


class Ball:
    def __init__(self, mass, position, velocity):
        self.mass = mass
        self.radius = math.sqrt(mass / math.pi)
        self.position = position
        self.velocity = velocity
        self.forcesAddedToNextFrame = Vector2(0, 0)

    def update(self):
        self.position = self.position + self.velocity * 0.05
        if self.position.x + self.radius > gameLength or self.position.x - self.radius < 0:
            self.velocity.x = self.velocity.x * -1
        if self.position.y + self.radius > gameWidth or self.position.y - self.radius < 0:
            self.velocity.y = self.velocity.y * -1

    def addForces(self):
        self.velocity = self.velocity + self.forcesAddedToNextFrame * (1 / self.mass)
        self.forcesAddedToNextFrame = Vector2(0, 0)


    def draw(self):
        pygame.draw.circle(screen, white, [self.position.x, self.position.y], self.radius, 0)


#ball = Ball(5000, Vector2(100, 400), Vector2(0, 0))

#ball2 = Ball(500, Vector2(1300, 400), Vector2(40, 0))

#for x in range(12):
 #   for y in range(6):
  #      ballArray.append(Ball(random.randint(100, 5000), Vector2(x * 100 + 100, y * 100 + 100), Vector2(random.randint(-20, 20), random.randint(-20, 20))))

for ball in range(10):
    ballArray.append(Ball(random.randint(100, 10000), Vector2(random.randint(100, 1300), random.randint(100, 700)), Vector2(random.randint(-20, 20), random.randint(-20, 20))))

f = 1
running = True
while running == True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    #font = pygame.font.SysFont(None, 24)
    #img = font.render('hello', True, white)
    #screen.blit(img, (20, 20))

    if f / 100 == int(f / 100):
        momentX = 0
        momentY = 0
        moment = 0
        kineticEnergy = 0
        for ball in ballArray:
            momentX = momentX + ball.velocity.x * ball.mass
            momentY = momentY + ball.velocity.y * ball.mass
            moment = moment + ball.velocity.module * ball.mass
            kineticEnergy = kineticEnergy + ball.mass / 2 * ball.velocity.module ** 2
        print('Momento X: ' + str(momentX) + ' Momento Y: ' + str(momentY) + ' Momento: ' + str(moment) + ' Energia cinetica: ' + str(kineticEnergy))


    f = f + 1
    screen.fill(black)
    for ball in ballArray:
        ball.draw()
    pygame.display.flip()
    i = 0
    for ball1 in ballArray:
        for ball2 in ballArray[i + 1:len(ballArray)]:
            if (ball1.position - ball2.position).module < ball1.radius + ball2.radius:
                nextBall1Velocity = ball1.velocity - (ball1.position - ball2.position) * (2 * ball2.mass / (ball1.mass + ball2.mass)) * ((ball1.velocity - ball2.velocity).EM(ball1.position - ball2.position) / (ball1.position - ball2.position).module ** 2)
                nextBall2VElocity = ball2.velocity - (ball2.position - ball1.position) * (2 * ball1.mass / (ball2.mass + ball1.mass)) * ((ball2.velocity - ball1.velocity).EM(ball2.position - ball1.position) / (ball2.position - ball1.position).module ** 2)
                ball1.velocity = nextBall1Velocity
                ball2.velocity = nextBall2VElocity
        i = i + 1
    for ball in ballArray:
        ball.update()