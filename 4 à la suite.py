import pygame
import pygame.gfxdraw
from constants import *

# Initialize Pygame
pygame.init()
W = 1920
H = 1080
# Initialize the font module after Pygame initialization
TITTLE_FONT = pygame.font.SysFont('Comic Sans MS', H//12)
GAME_FONT = pygame.font.Font(None, 36)
BOLD_FONT = pygame.font.Font(None, 36)
BOLD_FONT.set_bold(True)  # Set the font to bold

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
        fill_color = GREEN_RGB if i == current_polygon_index else POWDER_RGB

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
    is_last_menu = selected_index == len(menu_items) - 1
    i = selected_index
    rect_height = max_text_height
    start_menu_y = 1000 
    rect_top = start_menu_y 
    rect_color = (255, 190, 0) # Adjust brightness to 80%
    rect_border_color = (255, 190, 0)
    draw_rounded_rect(screen, pygame.Rect(1920 // 2 - max_text_width // 2, rect_top, max_text_width, rect_height),
                        rect_color, rect_border_color, 20)

    font = BOLD_FONT if selected_items[i] else GAME_FONT
    text_color = (255, 255, 255)
    outline_color = (0, 0, 0)
    item = "Attaque et défense chez les animaux" if i == len(menu_items) - 1 else menu_items[i]
    draw_outlined_text(font, item, text_color, outline_color, (W // 2, rect_top + rect_height // 2))


def adjust_brightness(color, factor):
    # Adjust the brightness of a color
    return tuple(int(min(max(0, c * factor), 255)) for c in color)

# Set up the display
screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
pygame.display.set_caption('Menu and Polygons Screen')

# Menu items
menu_items = ["Le chant dans le monde", "Sainteté et canonisation", "Traditions du Pays basque", "Thème mystère"]
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
                if timer_active:
                    if event.key == pygame.K_o:
                        if current_polygon_index > 0:
                            if border_index == 4 - current_polygon_index:
                                border_index += 1
                            current_polygon_index -= 1

                    elif event.key == pygame.K_p:
                        if current_polygon_index < len(scores) - 1:
                            current_polygon_index = len(scores) - 1

                    elif event.key == pygame.K_ESCAPE:
                        # Go back to the menu screen if Escape is pressed
                        menu_screen = True
                        timer_active = False
    # Clear the screen
    screen.fill(BLUE_RGB)
    write_title(screen, "Question pour un champion", (H//12)/2)
    write_title(screen, "Quatre à la suite", 3*(H//12)/2)
    if menu_screen:
        max_text_width = max(GAME_FONT.size(item)[0] for item in menu_items) + 500
        max_text_height = GAME_FONT.size(max(menu_items, key=len))[1] + 20
        vertical_gap = 20

        for i, item in enumerate(menu_items):
            is_last_menu = i == len(menu_items) - 1
            rect_height = max_text_height
            start_menu_y = (1080 - len(menu_items) * rect_height - (len(menu_items) - 1) * vertical_gap) // 2

            rect_top = start_menu_y + i * (rect_height + vertical_gap)
            rect_color = adjust_brightness((50, 205, 50) if is_last_menu else (255, 190, 0), 0.8) if selected_items[i] else ((50, 205, 50) if is_last_menu else (255, 190, 0))
            rect_border_color = adjust_brightness((50, 205, 50) if is_last_menu else (255, 190, 0), 0.8) if selected_items[i] else ((50, 205, 50) if is_last_menu else (255, 190, 0))

            draw_rounded_rect(screen, pygame.Rect(1920 // 2 - max_text_width // 2, rect_top, max_text_width, rect_height),
                              rect_color, rect_border_color, 20)

            font = BOLD_FONT if selected_items[i] else GAME_FONT
            text_color = (255, 255, 255)
            outline_color = (0, 0, 0)
            draw_outlined_text(font, item, text_color, outline_color, (W // 2, rect_top + rect_height // 2))
    else:
        if timer_active:
            time_elapsed = (current_time - timer_start) / 1000  # Convert to seconds
            remaining_time = max(timer_duration - int(time_elapsed), 0)  # Calculate remaining time
            timer_text = f"{remaining_time} s"
            timer_surface = GAME_FONT.render(timer_text, True, (255, 255, 255))
            timer_rect = timer_surface.get_rect(left=W // 2 + 450, top = H - 75)
            rect_width = 60  # Padding for the rectangle
            rect_height = 50
            rect_x = timer_rect.left -8   # 5 pixels padding on left
            rect_y = timer_rect.top -10  # 5 pixels padding on top

            # Draw the rectangle
            pygame.draw.rect(screen, (0, 0, 0), (rect_x - 2, rect_y - 2, rect_width + 2 * 2, rect_height + 2 * 2))

            pygame.draw.rect(screen, PINK_RGB, (rect_x, rect_y, rect_width, rect_height))
            
            screen.blit(timer_surface, timer_rect)

        draw_scores(screen, scores, current_polygon_index, border_index)
        

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
