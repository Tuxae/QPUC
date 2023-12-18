import pygame
import pygame.gfxdraw
from constants import *
from pygame import mixer
# Initialize Pygame
pygame.init()
W = 1920
H = 1080

# Initialize the font module after Pygame initialization
TITLE_SIZE = H//12
PLAYER_BORDER = H*0.06
TITTLE_FONT = pygame.font.SysFont('Comic Sans MS', TITLE_SIZE)
GAME_FONT = pygame.font.SysFont('futura', TITLE_SIZE // 2)

def write_title(screen, title, y_pos):
    text_qpuc = TITTLE_FONT.render(title, False, SEASHELL_RGB)
    text_rect = text_qpuc.get_rect(center=(W/2, y_pos))
    screen.blit(text_qpuc, text_rect)

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
        fill_color = ORANGE_RGB if i == current_polygon_index else BLUE_RGB

        # Border color logic
        if score > border_index:
            border_color = POWDER_RGB 
        else:
            border_color = GOLD_RGB

        pygame.draw.polygon(screen, fill_color, points)
        pygame.draw.lines(screen, border_color, True, points, 10)  # 10 is the border thickness

        text_surface = GAME_FONT.render(str(score), False, SEASHELL_RGB)
        text_rect = text_surface.get_rect(center=(75 * polygon_size, y_offset + 25 * polygon_size))
        screen.blit(text_surface, text_rect)

    # Draw the name of the selected menu item at the bottom
    is_last_menu = (selected_index == len(menu_items) - 1)
    i = selected_index
    rect_height = max_text_height
    start_menu_y = 900 
    rect_top = start_menu_y 
    rect_color = ORANGE_RGB # Adjust brightness to 80%
    rect_border_color = ORANGE_RGB
    draw_rounded_rect(screen, pygame.Rect(1920 // 2 - max_text_width // 2, rect_top, max_text_width, rect_height),
                        rect_color, rect_border_color, 20)

    font = GAME_FONT
    text_color = SEASHELL_RGB
    outline_color = (0, 0, 0)
    item = "Mystérieux et paranormal" if i == len(menu_items) - 1 else menu_items[i]
    draw_outlined_text(font, item, text_color, outline_color, (W // 2, rect_top + rect_height // 2))


# Set up the display
screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption('Menu and Polygons Screen')

# Menu items
menu_items = ["Donner du sens aux données", "Les rotations en science", "L'éxécutif sous la Ve république", "Thème mystère"]
selected_items = [False, False, False, False]

# Scores for each polygon
scores = [4, 3, 2, 1, 0]
selected_index = 0


# Game loop
menu_screen = True
running = True
timer_active = False
timer_start = 0
timer_duration = 40  # Duration of the timer in seconds

# Logos

# Load sound files
tic_sound = pygame.mixer.Sound('sounds/tic.wav')
dudu_sound = pygame.mixer.Sound('sounds/Dudu.wav')
dun_sound = pygame.mixer.Sound('sounds/Dun.wav')
dundundun_sound = pygame.mixer.Sound('sounds/DunDunDun.wav')
while running:
    current_time = pygame.time.get_ticks()  # Current time in milliseconds
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if menu_screen:
                # Initialize current polygon index
                current_polygon_index = len(scores) - 1
                border_index = 0
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    index = event.key - pygame.K_1
                    selected_index = index
                    selected_items[index] = not selected_items[index]  # Toggle the selected state
                    menu_screen = False
            elif not menu_screen:
                if event.key == pygame.K_i and not timer_active:
                    timer_start = current_time
                    timer_active = True
                    tic_sound.play(loops=-1)  # Play tic sound when timer starts
                if timer_active:
                    if event.key == pygame.K_o:
                        if current_polygon_index > 0:
                            if border_index == 4 - current_polygon_index:
                                border_index += 1
                                dun_sound.play()
                            if border_index == 4:
                                dundundun_sound.play()
                            current_polygon_index -= 1

                    elif event.key == pygame.K_p:
                        if current_polygon_index < len(scores) - 1:
                            current_polygon_index = len(scores) - 1

                    elif event.key == pygame.K_ESCAPE:
                        # Go back to the menu screen if Escape is pressed
                        menu_screen = True
                        timer_active = False
                        tic_sound.stop()

    # Clear the screen
    screen.fill(BLUE_RGB)
    write_title(screen, "Questions pour un champion", (H//12)/2)
    write_title(screen, "Quatre à la suite", 3*(H//12)/2)
    # Affichage Logo
    target_heigth = TITLE_SIZE*2

    img_src = "images/ENSAE2.png"
    img = pygame.image.load(img_src).convert_alpha()
    rect = img.get_rect()
    img = pygame.transform.rotozoom(img, 0, target_heigth/rect.height)
    screen.blit(img, (PLAYER_BORDER, PLAYER_BORDER//2))

    img_src = "images/TUXAE.png"
    img = pygame.image.load(img_src).convert_alpha()
    rect = img.get_rect()
    img = pygame.transform.rotozoom(img, 0, target_heigth/rect.height)
    screen.blit(img, (W - PLAYER_BORDER-img.get_width(), PLAYER_BORDER//2))
    if menu_screen:
        max_text_width = max(GAME_FONT.size(item)[0] for item in menu_items) + 900
        max_text_height = GAME_FONT.size(max(menu_items, key=len))[1] + 40
        vertical_gap = 20

        for i, item in enumerate(menu_items):
            is_last_menu = i == len(menu_items) - 1
            rect_height = max_text_height
            start_menu_y = (1080 - len(menu_items) * rect_height - (len(menu_items) - 1) * vertical_gap) // 2

            rect_top = start_menu_y + i * (rect_height + vertical_gap)
            rect_color = (ORANGE_RGB if not is_last_menu else GREEN_RGB) if not selected_items[i] else SATO_RGB
            rect_border_color = (ORANGE_RGB if not is_last_menu else GREEN_RGB) if not selected_items[i] else SATO_RGB

            draw_rounded_rect(screen, pygame.Rect(1920 // 2 - max_text_width // 2, rect_top, max_text_width, rect_height),
            
                              rect_color, rect_border_color, 20)

            font = GAME_FONT if selected_items[i] else GAME_FONT
            text_color = SEASHELL_RGB
            outline_color = (0, 0, 0)
            draw_outlined_text(font, item, text_color, outline_color, (W // 2, rect_top + rect_height // 2))
    else:
        if timer_active:
            time_elapsed = (current_time - timer_start) / 1000  # Convert to seconds
            remaining_time = max(timer_duration - int(time_elapsed), 0)  # Calculate remaining time
            timer_text = f"{remaining_time} s"
            timer_surface = GAME_FONT.render(timer_text, True, SEASHELL_RGB)
            timer_rect = timer_surface.get_rect(left=W // 2 + 450 + 300 + 50, top = H - 75 - 85)
            rect_width = 100  # Padding for the rectangle
            rect_height = 100
            rect_x = timer_rect.left - 5   # 5 pixels padding on left
            rect_y = timer_rect.top - 15 # 5 pixels padding on top
            
            # Draw the rectangle
            pygame.draw.rect(screen, (0, 0, 0), (rect_x - 2, rect_y - 2, rect_width + 2 * 2, rect_height + 2 * 2))

            pygame.draw.rect(screen, PINK_RGB, (rect_x, rect_y, rect_width, rect_height))
            
            screen.blit(timer_surface, timer_rect)
            if remaining_time == 0:
                timer_active = False
                dudu_sound.play()
                tic_sound.stop()

        draw_scores(screen, scores, current_polygon_index, border_index)
        

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
