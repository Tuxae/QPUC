import pygame
from constants import * 

"""
Ceci est le code pour le 9 points gagnants

"""

successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))

W = 1920
H = 1080

TITLE_SIZE = H//12

GAME_FONT = pygame.font.SysFont('Comic Sans MS', TITLE_SIZE)
screen = pygame.display.set_mode((W, H))
PLAYER_BORDER = H*0.06
PLAYER_LONG = (W - 5*PLAYER_BORDER)/4
# 720 / 4 180
# 
clock = pygame.time.Clock()
FPS = 60  # Frames per second.

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def write_title(screen, title, y_pos):
    text_qpuc = GAME_FONT.render(title, False, SEASHELL_RGB)
    text_rect = text_qpuc.get_rect(center=(W/2, y_pos))
    screen.blit(text_qpuc, text_rect)

def draw_hexagon(screen, x, y, width=0, height=0):
    pygame.draw.polygon(
        screen, 
        GOLD_RGB, 
        ((x+65, y+350), (x+115, y+350), (x+140, y+375), (x+115, y+400), (x+65, y+400), (x+40, y+375), (x+65, y+350))
    )

def draw_player_zone(screen, i=0):
    pygame.draw.rect(
        screen, 
        POWDER, 
        pygame.Rect(
            PLAYER_BORDER+i*(PLAYER_BORDER+PLAYER_LONG), 
            5*TITLE_SIZE/2, 
            PLAYER_LONG, 
            H-5*TITLE_SIZE/2-PLAYER_BORDER
        )
    )
    draw_hexagon(screen, 
                 PLAYER_BORDER+i*(PLAYER_BORDER+PLAYER_LONG))

def draw_score(screen, x=0, y=0, val=0):

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
screen.fill(BLUE_RGB)

write_title(screen, "Question pour un champion", TITLE_SIZE/2)
write_title(screen, "9 points gagnants", 3*TITLE_SIZE/2)
draw_player_zone(screen, i=0)
draw_player_zone(screen, i=1)
draw_player_zone(screen, i=2)
draw_player_zone(screen, i=3)

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                pass
            if event.key == pygame.K_ESCAPE:
                quit()
    pygame.display.update()  # Or pygame.display.flip()