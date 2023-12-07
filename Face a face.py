import pygame
import pygame.gfxdraw
from constants import *
from buzzer import SuperArduino

# Initialize Pygame
pygame.init()
#super_arduino = SuperArduino()
#super_arduino.get_winner() # None ou valeur entre 0 et 3, si buzzer quelconque éteint alors get_winner() va les rallumer, et pour éviter ca on peut faire turn_on = False en paramètre de get_winner()
# Si on veut pas qu'il emmmete de son on peut faire play_sound = False en paramètre de get_winner()                                    
W = 1920
H = 1080

TITLE_SIZE = H//12

GAME_FONT = pygame.font.SysFont('Comic Sans MS', TITLE_SIZE)
screen = pygame.display.set_mode((W, H))
PLAYER_BORDER = H*0.06
PLAYER_LONG = (W - 5*PLAYER_BORDER)/4
clock = pygame.time.Clock()
FPS = 60  # Frames per second.

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
                 PLAYER_BORDER + i*(PLAYER_BORDER+PLAYER_LONG) + PLAYER_LONG//4 + 10, H - 500)

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

screen.fill(BLUE_RGB)
write_title(screen, "Question pour un champion", TITLE_SIZE/2)
write_title(screen, "Face à face", 3*TITLE_SIZE/2)
draw_player_zone(screen, i=0)
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