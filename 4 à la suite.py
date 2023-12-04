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

# Set up the display
W = 1920
H = 1080
screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
pygame.display.set_caption('Menu and Polygons Screen')

# Menu items
menu_items = ["THEME 1", "THEME 2", "THEME 3", "THEME MYSTERE"]
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
        # Draw rounded rectangles for menu items
        max_text_width = max(GAME_FONT.size(item)[0] for item in menu_items) + 40
        max_text_height = GAME_FONT.size(max(menu_items, key=len))[1] + 20
        vertical_gap = 20  # Adjust this value to set the gap between rectangles

        for i, item in enumerate(menu_items):
            is_last_menu = i == len(menu_items) - 1
            rect_height = max_text_height
            start_menu_y = (1080 - len(menu_items) * rect_height - (len(menu_items) - 1) * vertical_gap) // 2  # Calculate starting y-coordinate

            rect_top = start_menu_y + i * (rect_height + vertical_gap)
            rect_color = (0, 255, 0) if is_last_menu else (255, 255, 0)
            rect_border_color = (0, 0, 255) if is_last_menu else (255, 215, 0)  # Blue border for the last menu
            border_radius = 20

            draw_rounded_rect(screen, pygame.Rect(1920 // 2 - max_text_width // 2, rect_top, max_text_width, rect_height),
                              rect_color, rect_border_color, border_radius)

            font = BOLD_FONT if selected_items[i] else GAME_FONT
            text_surface = font.render(item, True, GRAY_RGB if selected_items[i] else (0, 0, 0))
            text_rect = text_surface.get_rect(center=(1920 // 2, rect_top + rect_height // 2))
            screen.blit(text_surface, text_rect)
    else:
        # Draw the polygons and the selected menu item
        draw_scores(screen, scores, menu_items[selected_items.index(True)])

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()