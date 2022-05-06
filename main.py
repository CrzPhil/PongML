import pygame
import sys
import random


class Player:
    def __init__(self, player):
        self.dx = 0
        self.dy = -1

        self.player = player
        self.goals = 0

        self.width = 80
        self.length = 20

        # Set player position
        if self.player == 1:
            self.x = 50
        else:
            self.x = WIDTH - 50

        self.y = (HEIGHT // 2) - self.length

        self.rect = pygame.Rect(self.x, self.y, self.length, self.width)

    def moveUp(self):
        self.dy = -abs(self.dy)

    def moveDown(self):
        self.dy = abs(self.dy)

    def move(self):
        if 0 <= (self.y + self.dy) and (self.rect.bottomleft[1] + self.dy) <= HEIGHT:
            self.y += self.dy
            self.rect = self.rect.move(0, self.dy)
        else:
            self.dy = -self.dy

    def score(self):
        self.goals += 1


class Ball:
    def __init__(self):
        self.radius = 5

        self.x = WIDTH / 2
        self.y = HEIGHT / 2

        # Initial starting Velocity & Direction
        self.dx = .5
        self.dy = -.5

    def move(self, p1, p2):
        if int(self.y) <= 0:
            self.dy = -self.dy
        if int(self.x) <= p1.rect.topright[0] and p1.rect.topright[1] <= int(self.y) <= p1.rect.bottomright[1]:
            self.dx = -self.dx
        if int(self.x) >= p2.rect.topleft[0] and p2.rect.topleft[1] <= int(self.y) <= p2.rect.bottomleft[1]:
            self.dx = -self.dx
        if int(self.y) >= HEIGHT:
            self.dy = -self.dy

        # if p1.rect.collidepoint(self.x, self.y):
        #     self.dx = -self.dx
        # if p1.rect.collidepoint(self.x, self.y):
        #     self.dx = -self.dx

        if self.x == 0:
            self.reset(p1, p2)
            p2.score()
        elif self.x == WIDTH:
            self.reset(p1, p2)
            p1.score()

        self.x += self.dx
        self.y += self.dy

    def reset(self, p1, p2):
        print(f"P1: {p1.goals} P2: {p2.goals}")
        self.x = WIDTH / 2
        self.y = HEIGHT / 2

        # Initial starting Velocity & Direction
        self.dx = 0.5
        self.dy = round(random.uniform(-0.5, 0.5), 1)


def init():
    pygame.init()
    global screen, WIDTH, HEIGHT, WHITE, BLACK
    WIDTH = 800
    HEIGHT = 600
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))


def drawPlayers(p1: Player, p2: Player, ball: Ball):
    pygame.draw.rect(screen, WHITE, pygame.Rect(p1.x, p1.y, p1.length, p1.width))
    pygame.draw.rect(screen, WHITE, pygame.Rect(p2.x, p2.y, p2.length, p2.width))
    pygame.draw.circle(screen, WHITE, (ball.x, ball.y), ball.radius)


def main():
    init()
    p1, p2 = Player(1), Player(2)
    ball = Ball()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                p2.moveDown()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                p2.moveUp()

        screen.fill(BLACK)
        drawPlayers(p1, p2, ball)
        p1.move()
        p2.move()
        ball.move(p1, p2)

        pygame.display.flip()
        pygame.time.wait(1)


if __name__ == "__main__":
    main()
