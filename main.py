import pygame
import sys
import random
import numpy as np


def init():
    pygame.init()
    global screen, WIDTH, HEIGHT, WHITE, BLACK
    WIDTH = 800
    HEIGHT = 600
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))


init()


class Player:
    def __init__(self, player: int):
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
            self.x = WIDTH - 80

        self.y = (HEIGHT // 2) - self.length

        self.rect = pygame.Rect(self.x, self.y, self.length, self.width)

    def changeDirection(self, direction):
        if direction == 1:
            self.moveUp()
        elif direction == 2:
            self.moveDown()

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

    def reset(self):
        self.dy = -1
        # Set player position
        if self.player == 1:
            self.x = 50
        else:
            self.x = WIDTH - 50

        self.y = (HEIGHT // 2) - self.length

        self.rect = self.rect.move(self.x, self.y)


class Ball:
    def __init__(self):
        self.radius = 5

        self.x = WIDTH // 2
        self.y = HEIGHT // 2

        # Initial starting Velocity & Direction
        self.dx = .5
        self.dy = -.5

    def move(self, p1, p2):
        if int(self.y) <= 0:
            self.dy = -self.dy
        if p1.rect.topleft[0] <= int(self.x) <= p1.rect.topright[0] and p1.rect.topright[1] <= int(self.y) <= \
                p1.rect.bottomright[1]:
            self.dx = abs(self.dx)
        if p2.rect.topright[0] >= int(self.x) >= p2.rect.topleft[0] and p2.rect.topleft[1] <= int(self.y) <= \
                p2.rect.bottomleft[1]:
            self.dx = -abs(self.dx)
        if int(self.y) >= HEIGHT:
            self.dy = -self.dy

        if self.x <= 0:
            p2.score()
            self.reset(p1, p2)
        elif self.x >= WIDTH:
            p1.score()
            self.reset(p1, p2)

        self.x += self.dx
        self.y += self.dy

    def reset(self, p1, p2):
        print(f"P1: {p1.goals} P2: {p2.goals}")

        self.x = WIDTH // 2
        self.y = HEIGHT // 2

        # p1.reset()
        # p2.reset()

        # Initial starting Velocity & Direction
        self.dx = 0.5
        self.dy = round(random.uniform(-0.5, 0.5), 1)


class Field:
    """
    Class for transforming the playing field into a 2D array.

    There's a set chunksize in which the pixels are divided to.
    Default, but slow: ball diameter -> self.ball.radius * 2

    Divisions:
    p1 - 1
    p2 - 2
    ball - 3
    else - 0

    """

    def __init__(self, ball: Ball, p1: Player, p2: Player):
        self.ball = ball
        self.p1 = p1
        self.p2 = p2

        self.chunksize = self.ball.radius * 2 * 2

        # Grid is a 2D-Array of 10-wide chunks (2*radius of ball)
        self.grid = np.zeros(shape=((HEIGHT // self.chunksize), (WIDTH // self.chunksize)))

    def update(self):
        for y, row in enumerate(self.grid):
            for x in range(len(row)):
                # Update ball position in grid
                if y == (self.ball.y // self.chunksize) and x == (self.ball.x // self.chunksize):
                    self.grid[y][x] = 3
                # All points in p1 are marked 1
                elif (self.p1.rect.bottomleft[1] // self.chunksize) >= y >= (self.p1.y // self.chunksize) and (
                        self.p1.rect.bottomleft[0] // self.chunksize) <= x <= (
                        self.p1.rect.bottomright[0] // self.chunksize):
                    self.grid[y][x] = 1
                # All points in p2 are marked 2
                elif (self.p2.rect.bottomleft[1] // self.chunksize) >= y >= (self.p2.y // self.chunksize) and (
                        self.p2.rect.bottomleft[0] // self.chunksize) <= x <= (
                        self.p2.rect.bottomright[0] // self.chunksize):
                    self.grid[y][x] = 2
                else:
                    self.grid[y][x] = 0


class Environment:
    FIELD_WIDTH = WIDTH // 20
    FIELD_HEIGHT = HEIGHT // 20

    WINDOW_WIDTH = WIDTH
    WINDOW_HEIGHT = HEIGHT

    P_LENGTH = 20
    P_WIDTH = 10

    PUNISHMENT = -100
    REWARD = 10
    score = 0

    ENVIRONMENT_SHAPE = (FIELD_HEIGHT, FIELD_WIDTH, 1)
    ACTION_SPACE = [0, 1, 2]
    ACTION_SPACE_SIZE = len(ACTION_SPACE)

    frames_counter = 0

    def __init__(self):
        # Colours:
        self.WHITE = WHITE
        self.BLACK = BLACK
        self.RED = (255, 80, 80)
        self.BLUE = (80, 80, 255)

        self.field = self.p1 = self.p2 = self.ball = None
        self.current_state = self.reset()

        self.game_over = False

    def reset(self):
        self.score = 0
        self.frames_counter = 0
        self.game_over = False

        self.p1 = Player(1)
        self.p2 = Player(2)
        self.ball = Ball()

        self.field = Field(ball=self.ball, p1=self.p1, p2=self.p2)
        self.field.update()

        return self.field.grid

    def step(self, action):
        global score_increased

        self.frames_counter += 1
        reward = 0

        # If move either up or down
        if action in [1, 2]:
            self.p2.changeDirection(action)

        # Update player/ball position
        self.p1.move()
        self.p2.move()
        self.ball.move(self.p1, self.p2)

        self.field.update()

        # Increase reward +1 for every 100 frames the player survives
        if self.frames_counter % 100 == 0:
            reward += 10

        # Increase reward + self.REWARD for every goal scored

        # Lose Conditions:
        # C1 : Goal scored by opponent
        lose_conds = [self.p1.goals == 10]

        # Win conditions:
        win_conds = [self.p2.goals == 10]

        if True in lose_conds:
            self.game_over = True
            reward = self.PUNISHMENT
            return self.field.grid, reward, self.game_over

        elif True in win_conds:
            self.game_over = True
            reward = self.REWARD
            return self.field.grid, reward, self.game_over

        return self.field.grid, reward, self.game_over

    def render(self, WINDOW=None, human=False):
        if human:
            action = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    action = 2
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                    action = 1

            ########## Step ##########
            _, reward, self.game_over = self.step(action)

        ########## Draw Environment ##########
        WINDOW.fill(BLACK)
        drawPlayers(self.p1, self.p2, self.ball)
        pygame.display.flip()
        pygame.time.wait(1)


def drawPlayers(p1: Player, p2: Player, ball: Ball):
    pygame.draw.rect(screen, WHITE, pygame.Rect(p1.x, p1.y, p1.length, p1.width))
    pygame.draw.rect(screen, WHITE, pygame.Rect(p2.x, p2.y, p2.length, p2.width))
    pygame.draw.circle(screen, WHITE, (ball.x, ball.y), ball.radius)


def main():
    init()
    p1, p2 = Player(1), Player(2)
    ball = Ball()
    f = Field(ball, p1, p2)

    i = 1

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                p2.changeDirection(2)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                p2.changeDirection(1)

        screen.fill(BLACK)
        drawPlayers(p1, p2, ball)
        p1.move()
        p2.move()
        ball.move(p1, p2)

        pygame.display.flip()

        if i == 1:
            f.update()
            i = -1
        i += 1
        pygame.time.wait(1)


if __name__ == "__main__":
    main()
