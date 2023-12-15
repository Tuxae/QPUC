import pygame
import pygame.gfxdraw
from constants import *
from buzzer import SuperArduino, ShadowSuperArduino
import math
from pygame import mixer
# Initialize Pygame
pygame.init()
# super_arduino = SuperArduino("/dev/cu.usbmodem14112101")
super_arduino = ShadowSuperArduino("/dev/cu.usbmodem14112101")
                               
W = 1920
H = 1080

TITLE_SIZE = H//12

GAME_FONT = pygame.font.SysFont('Comic Sans MS', TITLE_SIZE)
TEXT_FONT = pygame.font.Font(None, 60)
BOLD_FONT = pygame.font.Font(None, 36)
BOLD_FONT.set_bold(True)  # Set the font to bold

screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN|pygame.SCALED)
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
        ORANGE_RGB, 
        ((x+65, y+350), (x+115, y+350), (x+140, y+375), (x+115, y+400), (x+65, y+400), (x+40, y+375), (x+65, y+350))
    )

def draw_polygon(screen, x, y, polygon_size, polygon_colour):
    """
    Draws a polygon centered at (x, y) with a size of 'polygon_size' and filled with 'polygon_colour'.
    
    :param screen: Pygame screen where to draw the polygon.
    :param x: X-coordinate of the center of the polygon.
    :param y: Y-coordinate of the center of the polygon.
    :param polygon_size: Size of the polygon (diameter for circumscribed circle).
    :param polygon_colour: Color to fill the polygon.
    """
    # Number of sides for the polygon, can be changed to create different shapes
    num_sides = 6

    # Calculating the points of the polygon
    points = []
    for i in range(num_sides):
        angle = 2 * math.pi * i / num_sides
        point_x = x + polygon_size * math.cos(angle)
        point_y = y + polygon_size * math.sin(angle)
        points.append((point_x, point_y))

    # Drawing the polygon
    pygame.draw.polygon(screen, polygon_colour, points)

def draw_progress_bar(screen, x, y, size, fill_percentage):
    height = 2 * size * math.sin(2 * math.pi / 6)
    progress_height = height * fill_percentage / 100
    pygame.draw.rect(screen, ORANGE_RGB, [x - size, y + height // 2 - progress_height + 2, 2 * size, progress_height])

    points = []
    points1 = []
    for i in range(6):
        angle = 2 * math.pi * i / 6
        point_x = x + (size + 15)* math.cos(angle)
        point_y = y + (size + 15) * math.sin(angle)
        points.append((point_x, point_y))
        point_x1 = x + (size) * math.cos(angle)
        point_y1 = y + (size) * math.sin(angle)
        points1.append((point_x1, point_y1))
    hex_height =  size * math.sin(2 * math.pi / 6) 
    half_width = size 
    half_height = hex_height 

    # Coordinates for the four corner triangles
    top_left_triangle = [points[0] , points[1], (x + half_width, y + half_height)]
    top_right_triangle = [points[2], points[3], (x - half_width, y + half_height)]
    bottom_left_triangle = [points[3], points[4], (x - half_width, y - half_height)]
    bottom_right_triangle = [points[5], points[0], (x + half_width, y - half_height)]
    top_left_triangle1 = [points1[0] , points1[1], (x + half_width, y + half_height)]
    top_right_triangle1 = [points1[2], points1[3], (x - half_width, y + half_height)]
    bottom_left_triangle1 = [points1[3], points1[4], (x - half_width, y - half_height)]
    bottom_right_triangle1 = [points1[5], points1[0], (x + half_width, y - half_height)]

    # Drawing the triangles
    pygame.draw.polygon(screen, GOLD_RGB, top_left_triangle1)
    pygame.draw.polygon(screen, GOLD_RGB, top_right_triangle1)
    pygame.draw.polygon(screen, GOLD_RGB, bottom_left_triangle1)
    pygame.draw.polygon(screen, GOLD_RGB, bottom_right_triangle1)
 
    pygame.draw.polygon(screen, BLUE_RGB, top_left_triangle)
    pygame.draw.polygon(screen, BLUE_RGB, top_right_triangle)
    pygame.draw.polygon(screen, BLUE_RGB, bottom_left_triangle)
    pygame.draw.polygon(screen, BLUE_RGB, bottom_right_triangle)


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

def in_interval(item,list):
     return list[0] < item <= list[1]


screen.fill(BLUE_RGB)
write_title(screen, "Questionsd pour un champion", TITLE_SIZE/2)
write_title(screen, "Face à face", 3*TITLE_SIZE/2)

score = [0, 0]
points = [4, 3, 2, 1]

timer_active = False
timer_start = 0
timer_duration = 20  # Duration of the timer in seconds
left = [True, False, True, False]
intervals = [[13.5,20],[8.5,13.5],[4,8.5],[0,4]]
pause = False
timer_paused_at = 0 
mixer.init()
tic_sound = mixer.Sound("sounds/Tic.wav")
dudu_sound = pygame.mixer.Sound('sounds/Dudu.wav')

super_arduino.turn_on_buzzer([False, False, False, False])
while True:
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()  # Current time in milliseconds
    if timer_active:
        
        if pause:
            pass
        if not pause:
            res = super_arduino.get_winner(turn_on=False)

            remaining_time = timer_duration - (current_time - timer_start) / 1000
        if remaining_time <= 0:
            timer_active = False
            tic_sound.stop()  # Stop tic sound when timer ends
            dudu_sound.play() # Play dudu sound when timer ends
        if remaining_time <= 0:
            timer_active = False
            tic_sound.stop()  # Stop tic sound when timer ends
            dudu_sound.play() # Play dudu sound when timer ends

        if remaining_time > 0:
            i = [in_interval(remaining_time, intervals[i]) for i in range(4)].index(True)
            super_arduino.turn_on_buzzer([left[i], False, False, not left[i]])
            if (res == 0 and (not pause) and left[i]):
                tic_sound.stop()
                pause = not pause
                if pause:
                    timer_paused_at = current_time
                    tic_sound.stop()  # Stop tic sound when timer is paused
            elif (res == 3 and (not pause) and not left[i]):
                tic_sound.stop()
                pause = not pause
                if pause:
                    timer_paused_at = current_time
                    tic_sound.stop()
                    
    for event in pygame.event.get():
        print(timer_active)
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                timer_active = False
                pause = False
            if event.key == pygame.K_i and not timer_active:
                    timer_start = current_time
                    timer_active = True
                    tic_sound.play(loops=-1)  # Play tic sound when timer starts
            if event.key == pygame.K_q:
                    left = [True, False, True, False]
            
            if event.key == pygame.K_d:
                    left = [False, True, False, True]
            if timer_active:
                        
                        if left[i] and pause:
                            if event.key == pygame.K_o:
                                timer_start = timer_start + current_time - timer_paused_at
                                score[0] += points[i]
                                timer_active = False
                                pause = False
                            elif event.key == pygame.K_p:
                                timer_start = timer_start + current_time - timer_paused_at
                                left[i] = False
                                for j in range(i + 1, 4):
                                    if left[j]:
                                        left[j] = False
                                    else:
                                        break
                                pause = False
                                tic_sound.play(loops=-1)  # Play tic sound when timer resumes

                        elif not left[i] and pause:
                            if event.key == pygame.K_o:
                                timer_start = timer_start + current_time - timer_paused_at
                                score[1] += points[i]
                                timer_active = False
                                pause = False

                            elif event.key == pygame.K_p: 
                                timer_start = timer_start + current_time - timer_paused_at
                                left[i] = True
                                for j in range(i + 1, 4):
                                    if not left[j]:
                                        left[j] = True 
                                    else:
                                        break
                                pause = False     
                                tic_sound.play(loops=-1)  # Play tic sound when timer resumes  
            if not timer_active:
                tic_sound.stop()





    draw_player_zone(screen, score[0], i=0)
    draw_player_zone(screen, score[1], i=3)
    if not timer_active:
            screen.fill(BLUE_RGB)
            write_title(screen, "Questions pour un champion", TITLE_SIZE/2)
            write_title(screen, "Face à face", 3*TITLE_SIZE/2)
            draw_player_zone(screen, score[0], i=0)
            draw_player_zone(screen, score[1], i=3)
            for i, point in enumerate(points):
                    polygon_size = 100
                    polygon_height = (polygon_size * math.sin(2 * math.pi / 6))
                    polygon_spacing = polygon_height + 100
                    total_height = len(points) * polygon_spacing
                    start_y = (H - total_height) // 2 + 250
                    y_offset = start_y + i * polygon_spacing
                    
                    fill_color = ORANGE_RGB
                    border_color = GOLD_RGB
                    draw_polygon(screen, W//2, y_offset, polygon_size, border_color)
                    draw_polygon(screen, W//2, y_offset, polygon_size - 15, fill_color)
                    text_surface = TEXT_FONT.render(str(point), False, SEASHELL_RGB)
                    text_rect = text_surface.get_rect(center=(W//2, y_offset))
                    screen.blit(text_surface, text_rect)
    elif timer_active and not pause:
        remaining_time = timer_duration - (current_time - timer_start) / 1000
        if remaining_time <= 0:
            timer_active = False
            remaining_time = 0
            mixer.music.load("sounds/Dudu.wav")
            mixer.music.play()
        screen.fill(BLUE_RGB)
        write_title(screen, "Questions pour un champion", TITLE_SIZE/2)
        write_title(screen, "Face à face", 3*TITLE_SIZE/2)
        draw_player_zone(screen, score[0], i=0)
        draw_player_zone(screen, score[1], i=3)
        
        for i, point in enumerate(points):
            polygon_size = 100
            polygon_height = 2 * (polygon_size * math.sin(math.pi / 6))
            polygon_spacing = polygon_height + 100
            total_height = len(points) * polygon_spacing
            start_y = (H - total_height) // 2 + 250
            y_offset = start_y + i * polygon_spacing
            
            fill_color = BLUE_RGB
            border_color = GOLD_RGB
            x = W//2 - polygon_size//2 if left[i] else W//2 + polygon_size//2
            draw_polygon(screen, x, y_offset, polygon_size, border_color)
            draw_polygon(screen, x, y_offset, polygon_size - 15, fill_color)
            if intervals[i][0] < remaining_time <= intervals[i][1]:
                draw_progress_bar(screen, x, y_offset, polygon_size - 15, (remaining_time - intervals[i][0])/(intervals[i][1] - intervals[i][0])*100)
            elif remaining_time >= intervals[i][0]:
                draw_polygon(screen, x, y_offset, polygon_size - 15, ORANGE_RGB)
            text_surface = TEXT_FONT.render(str(point), False, SEASHELL_RGB)
            text_rect = text_surface.get_rect(center=(x, y_offset))
            screen.blit(text_surface, text_rect)


    pygame.display.update()  # Or pygame.display.flip()

pygame.quit()