from main import *
import time

env = Environment()

clock = pygame.time.Clock()
win = False
winning_score = 100

while not win:
    score_increased = False
    game_over = False
    _ = env.reset()
    pygame.display.set_caption("Game")
    while not game_over:
        #clock.tick(27)
        env.render(WINDOW=screen, human=True)
        game_over = env.game_over

    #time.sleep(0.5)
    screen.fill(env.BLACK)
    if env.score >= winning_score:
        win = True

    pygame.display.update()
