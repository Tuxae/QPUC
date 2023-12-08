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
    angle = 0
    target_width = PLAYER_LONG-1*PLAYER_BORDER
    img = pygame.image.load("images/test.jpg").convert()
    rect = img.get_rect()
    scale = target_width / rect.width
    img = pygame.transform.rotozoom(img, angle, scale)
    screen.blit(
        img, 
        (
            1.5*PLAYER_BORDER+i*(PLAYER_BORDER+PLAYER_LONG), 
            5*TITLE_SIZE/2+0.5*PLAYER_BORDER
        )
    )

def draw_score(screen, i, val=0):
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
    x = PLAYER_BORDER+i*(PLAYER_BORDER+PLAYER_LONG)+PLAYER_LONG/2
    hexagon_width = W/10
    y = H-2*PLAYER_BORDER-3*hexagon_width/4
    text_qpuc = GAME_FONT.render(str(val), False, SEASHELL_RGB)
    text_rect = text_qpuc.get_rect(center=(x, y))
    screen.blit(text_qpuc, text_rect)

liste_score = [0, 0, 0, 0]
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
            if event.key == pygame.K_a:
                liste_score[0] += 1
            if event.key == pygame.K_z:
                liste_score[1] += 1
            if event.key == pygame.K_e:
                liste_score[2] += 1
            if event.key == pygame.K_r:
                liste_score[3] += 1
            if event.key == pygame.K_q:
                liste_score[0] -= 1
            if event.key == pygame.K_s:
                liste_score[1] -= 1
            if event.key == pygame.K_d:
                liste_score[2] -= 1
            if event.key == pygame.K_f:
                liste_score[3] -= 1
            if event.key == pygame.K_ESCAPE:
                quit()
    
    for i in range(4):
        draw_score(screen, i, val=liste_score[i])
    pygame.display.update()  # Or pygame.display.flip()