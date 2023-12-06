import pygame
import pygame.gfxdraw

# Initialize Pygame
pygame.init()

# Constants for colors
GOLD_RGB = (255, 215, 0)
BLUE_RGB = (0, 0, 255)
SEASHELL_RGB = (255, 245, 238)
GRAY_RGB = (169, 169, 169)  # Gray color

# Initialize the font module after Pygame initialization
GAME_FONT = pygame.font.Font(None, 36)
BOLD_FONT = pygame.font.Font(None, 36)
BOLD_FONT.set_bold(True)  # Set the font to bold

def draw_rounded_rect(screen, rect, color, border_color, border_radius):
    pygame.gfxdraw.box(screen, rect, color)
    pygame.draw.rect(screen, border_color, rect, border_radius=border_radius)
    pygame.draw.rect(screen, border_color, rect, width=2)  # Width of 2 for the border

def draw_outlined_text(font, text, color, outline_color, pos):
    text_surface = font.render(text, True, color)
    outline_surface = font.render(text, True, outline_color)

    text_rect = text_surface.get_rect(center=pos)
    outline_rect = outline_surface.get_rect(center=pos)

    screen.blit(outline_surface, outline_rect)
    screen.blit(text_surface, text_rect)

def draw_scores(screen, scores, selected_item, x=0, y=0):
    # Calculate the total height of the polygons
    total_height = len(scores) * 100

    # Calculate the starting y-coordinate to center vertically
    start_y = (1080 - total_height) // 2

    # Draw the four polygons centered vertically on the left
    for i, val in enumerate(scores):
        # Adjust y-coordinate for vertical spacing
        y_offset = i * 100

        # Draw Gold Polygon
        pygame.draw.polygon(
            screen,
            GOLD_RGB,
            ((50, start_y + y_offset), (100, start_y + y_offset), (125, start_y + 25 + y_offset),
            (100, start_y + 50 + y_offset), (50, start_y + 50 + y_offset), (25, start_y + 25 + y_offset), (50, start_y + y_offset))
        )

        bx = 6  # Border
        by = 4  # Border
        # Draw Blue Polygon with Border
        pygame.draw.polygon(
            screen,
            BLUE_RGB,
            ((50, start_y + by + y_offset), (100, start_y + by + y_offset),
            (125 - bx, start_y + 25 + y_offset), (100, start_y + 50 - by + y_offset),
            (50, start_y + 50 - by + y_offset), (25 + bx, start_y + 25 + y_offset), (50, start_y + by + y_offset))
        )

        # Draw Score Text
        text_surface = GAME_FONT.render(str(val), False, SEASHELL_RGB)
        screen.blit(text_surface, (75 - 18 / 2, start_y + 2 + y_offset))

    # Draw the name of the selected menu item at the bottom
    text_surface = BOLD_FONT.render(selected_item, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(W // 2, H - 100))
    screen.blit(text_surface, text_rect)


def adjust_brightness(color, factor):
    # Adjust the brightness of a color
    return tuple(int(min(max(0, c * factor), 255)) for c in color)

# Set up the display
W = 1920
H = 1080
screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
pygame.display.set_caption('Menu and Polygons Screen')

# Menu items
menu_items = ["Le chant dans le monde", "Sainteté et canonisation", "Traditions du Pays basque", "Thème mystère"]
selected_items = [False, False, False, False]

# Scores for each polygon
scores = [4, 3, 2, 1]

# Game loop
menu_screen = True
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if menu_screen:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    index = event.key - pygame.K_1
                    selected_items[index] = not selected_items[index]  # Toggle the selected state
                    menu_screen = False
            elif event.key == pygame.K_ESCAPE:
                # Go back to the menu screen if Escape is pressed
                menu_screen = True

    # Clear the screen
    screen.fill((255, 255, 255))

    if menu_screen:
        max_text_width = max(GAME_FONT.size(item)[0] for item in menu_items) + 500
        max_text_height = GAME_FONT.size(max(menu_items, key=len))[1] + 20
        vertical_gap = 20

        for i, item in enumerate(menu_items):
            is_last_menu = i == len(menu_items) - 1
            rect_height = max_text_height
            start_menu_y = (1080 - len(menu_items) * rect_height - (len(menu_items) - 1) * vertical_gap) // 2

            rect_top = start_menu_y + i * (rect_height + vertical_gap)
            rect_color = adjust_brightness((50, 205, 50) if is_last_menu else (255, 228, 54), 0.8) if selected_items[i] else ((50, 205, 50) if is_last_menu else (255, 228, 54))  # Adjust brightness to 80%
            rect_border_color = adjust_brightness((50, 205, 50) if is_last_menu else (255, 228, 54), 0.8) if selected_items[i] else ((50, 205, 50) if is_last_menu else (255, 228, 54))

            draw_rounded_rect(screen, pygame.Rect(1920 // 2 - max_text_width // 2, rect_top, max_text_width, rect_height),
                              rect_color, rect_border_color, 20)

            font = BOLD_FONT if selected_items[i] else GAME_FONT
            text_color = (255, 255, 255)
            outline_color = (0, 0, 0)
            draw_outlined_text(font, item, text_color, outline_color, (W // 2, rect_top + rect_height // 2))
    else:
        draw_scores(screen, scores, menu_items[selected_items.index(True)])

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()