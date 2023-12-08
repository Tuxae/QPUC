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

def draw_hexagon(screen, x, y, color=GOLD_RGB, width=100):
    # height = width / 2
    width_scale = width/100
    height_scale = width/100
    pygame.draw.polygon(
        screen, 
        color, 
        (
            (x-25*width_scale, y+0), 
            (x+25*width_scale, y+0), 
            (x+50*width_scale, y+25*height_scale), 
            (x+25*width_scale, y+50*height_scale), 
            (x-25*width_scale, y+50*height_scale), 
            (x-50*width_scale, y+25*height_scale), 
            (x-25*width_scale, y+0)
        )
    )

def draw_player_zone(screen, i=0):
    rectangle_height = H-5*TITLE_SIZE/2-2*PLAYER_BORDER
    pygame.draw.rect(
        screen, 
        GOLD_RGB, 
        pygame.Rect(
            PLAYER_BORDER+i*(PLAYER_BORDER+PLAYER_LONG), 
            5*TITLE_SIZE/2, 
            PLAYER_LONG, 
            rectangle_height
        )
    )
    pygame.draw.rect(
        screen, 
        POWDER, 
        pygame.Rect(
            PLAYER_BORDER+i*(PLAYER_BORDER+PLAYER_LONG), 
            5*TITLE_SIZE/2+rectangle_height*0.01, 
            PLAYER_LONG, 
            rectangle_height*0.98
        )
    )
    hexagon_width = W/10
    draw_hexagon(
        screen, 
        PLAYER_BORDER+i*(PLAYER_BORDER+PLAYER_LONG)+PLAYER_LONG/2, 
        H-2*PLAYER_BORDER-hexagon_width,
        GOLD_RGB,
        width=hexagon_width
    )
    draw_hexagon(
        screen, 
        PLAYER_BORDER+i*(PLAYER_BORDER+PLAYER_LONG)+PLAYER_LONG/2, 
        H-2*PLAYER_BORDER-hexagon_width*0.96,
        SEASHELL_RGB,
        width=hexagon_width*0.84
    )
    draw_hexagon(
        screen, 
        PLAYER_BORDER+i*(PLAYER_BORDER+PLAYER_LONG)+PLAYER_LONG/2, 
        H-2*PLAYER_BORDER-hexagon_width*0.95,
        BLUE_RGB,
        width=hexagon_width*0.8
    )

def draw_score(screen, i, val=0):
    x = PLAYER_BORDER+i*(PLAYER_BORDER+PLAYER_LONG)+PLAYER_LONG/2
    hexagon_width = W/10
    y = H-2*PLAYER_BORDER-hexagon_width
    text_qpuc = GAME_FONT.render(str(val), False, SEASHELL_RGB)
    text_rect = text_qpuc.get_rect(center=(x, y))
    screen.blit(text_qpuc, text_rect)

liste_score = []
screen.fill(BLUE_RGB)

write_title(screen, "Question pour un champion", TITLE_SIZE/2)
write_title(screen, "9 points gagnants", 3*TITLE_SIZE/2)
draw_player_zone(screen, i=0)
draw_player_zone(screen, i=1)
draw_player_zone(screen, i=2)
draw_player_zone(screen, i=3)
for i in range(4):
    draw_score(screen, i, val=0)

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