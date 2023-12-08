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
TEXT_FONT = pygame.font.Font(None, 54)
BOLD_FONT = pygame.font.Font(None, 36)
BOLD_FONT.set_bold(True)  # Set the font to bold

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

def draw_player_zone(screen, score, i=0):
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
    text_surface = TEXT_FONT.render(str(score), False, SEASHELL_RGB)
    text_rect = text_surface.get_rect(center=(PLAYER_BORDER+ i*(PLAYER_BORDER+PLAYER_LONG) + PLAYER_LONG//2, H - 120))
    screen.blit(text_surface, text_rect)

def draw_rounded_rect(screen, rect, color, border_color, border_radius):
    pygame.gfxdraw.box(screen, rect, color)
    pygame.draw.rect(screen, border_color, rect, border_radius=border_radius)
    pygame.draw.rect(screen, (0, 0, 0), rect, width=2)  # Width of 2 for the border

def draw_outlined_text(font, text, color, outline_color, pos):
    text_surface = font.render(text, True, color)
    outline_surface = font.render(text, True, outline_color)

    text_rect = text_surface.get_rect(center=pos)
    outline_rect = outline_surface.get_rect(center=pos)

    screen.blit(outline_surface, outline_rect)
    screen.blit(text_surface, text_rect)

def draw_scores(screen, scores, current_polygon_index, border_index, x=0, y=0):
    polygon_size = 2
    polygon_spacing = 60 * polygon_size

    total_height = len(scores) * polygon_spacing
    start_y = (H - total_height) // 2

    for i, score in enumerate(scores):
        y_offset = start_y + i * polygon_spacing

        points = [(x * polygon_size, y * polygon_size + y_offset) for x, y in
                  [(50, 0), (100, 0), (125, 25),
                   (100, 50), (50, 50), (25, 25), (50, 0)]]

        # Fill color is GREEN_RGB for the selected polygon and POWDER_RGB for others
        fill_color = GREEN_RGB if i == current_polygon_index else BLUE_RGB

        # Border color logic
        if score > border_index:
            border_color = POWDER_RGB 
        else:
            border_color = GOLD_RGB

        pygame.draw.polygon(screen, fill_color, points)
        pygame.draw.lines(screen, border_color, True, points, 10)  # 10 is the border thickness

        text_surface = TEXT_FONT.render(str(score), False, SEASHELL_RGB)
        text_rect = text_surface.get_rect(center=(75 * polygon_size, y_offset + 25 * polygon_size))
        screen.blit(text_surface, text_rect)


screen.fill(BLUE_RGB)
write_title(screen, "Question pour un champion", TITLE_SIZE/2)
write_title(screen, "Face à face", 3*TITLE_SIZE/2)

score = [0, 0]
points = [1, 2, 3, 4]

timer_active = False
timer_start = 0
timer_duration = 20  # Duration of the timer in seconds
middle = 0
while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        current_time = pygame.time.get_ticks()  # Current time in milliseconds
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i and not timer_active:
                    timer_start = current_time
                    timer_active = True
            if timer_active:
                if event.key == pygame.K_ESCAPE:
                    middle = 0
                if event.key == pygame.K_q:
                    middle = -1
                if event.key == pygame.K_d:
                    middle = 1

                if middle == 0:
                    for i, point in enumerate(points):
                            polygon_size = 2
                            polygon_spacing = 60 * polygon_size
                            total_height = len(points) * polygon_spacing
                            start_y = (H - total_height) // 2
                            y_offset = start_y + i * polygon_spacing

                            p = [(x * polygon_size, y * polygon_size + y_offset) for x, y in
                                    [(H//2 - 50, 0), ( H//2, 0), (25 + H//2, 25),
                                    ( H//2, 50), (H//2 -50, 50), (H//2-75, 25), (H//2-50, 0)]]
                            # Fill color is GREEN_RGB for the selected polygon and POWDER_RGB for others
                            fill_color = BLUE_RGB
                            border_color = GOLD_RGB
                            pygame.draw.polygon(screen, fill_color, p)
                            pygame.draw.lines(screen, border_color, True, p, 10)  # 10 is the border thickness
                            text_surface = TEXT_FONT.render(str(point), False, SEASHELL_RGB)
                            text_rect = text_surface.get_rect(center=(75 * polygon_size, y_offset + 25 * polygon_size))
                            screen.blit(text_surface, text_rect)
                    if event.key == pygame.K_a:

                        score[0] += 1
                    elif event.key == pygame.K_z:
                        left = False
                else:
                    if event.key == pygame.K_a:
                        score[1] += 1
                    elif event.key == pygame.K_z:
                        left = True
    draw_player_zone(screen, score[0], i=0)
    draw_player_zone(screen, score[1], i=3)
    
    pygame.display.update()  # Or pygame.display.flip()

pygame.quit()