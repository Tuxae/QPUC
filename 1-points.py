import pygame
from constants import * 

"""
Ceci est le code pour le 9 points gagnants

"""

successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))

W = 1920
H = 1080

GAME_FONT = pygame.font.SysFont('Comic Sans MS', 30)
screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
# 720 / 4 180
# 
clock = pygame.time.Clock()
FPS = 60  # Frames per second.

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def draw_score(screen, x=0, y=0, val=0):
    pygame.draw.polygon(
        screen, 
        GOLD_RGB, 
        ((x+65, y+350), (x+115, y+350), (x+140, y+375), (x+115, y+400), (x+65, y+400), (x+40, y+375), (x+65, y+350))
    )
    bx = 6 # Border
    by = 4 # Border
    pygame.draw.polygon(
        screen, 
        BLUE_RGB, 
        ((x+65, y+350+by), (x+115, y+350+by), (x+140-bx, y+375), (x+115, y+400-by), (x+65, y+400-by), (x+40+bx, y+375), (x+65, y+350+by))
    )
    text_surface = GAME_FONT.render(str(val), False, SEASHELL_RGB)
    screen.blit(text_surface, (x+90-18/2, y+352))

liste_score = []

while True:
    clock.tick(FPS)
    screen.fill(BLUE_RGB)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                pass
            if event.key == pygame.K_ESCAPE:
                quit()
    draw_score(screen, )
    draw_score(screen, 180)
    draw_score(screen, 2*180)
    draw_score(screen, 3*180)
    pygame.display.update()  # Or pygame.display.flip()