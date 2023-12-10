import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

def draw_progress_bar(screen, center, size, progress):
    """
    Draw a vertical progress bar.

    :param screen: Pygame screen to draw on
    :param center: Tuple (x, y) for the center of the progress bar
    :param size: Tuple (width, height) of the progress bar
    :param progress: Float (0 to 1) indicating the progress
    """
    width, height = size
    x, y = center

    # Background rectangle
    pygame.draw.rect(screen, BLACK, [x - width // 2, y - height // 2, width, height], 2)

    # Progress rectangle
    progress_height = int(height * progress)
    pygame.draw.rect(screen, GREEN, [x - width // 2, y + height // 2 - progress_height, width, progress_height])

# Main loop
running = True
progress = 0.0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update progress
    progress += 0.01
    if progress > 1.0:
        progress = 1.0

    # Draw everything
    screen.fill((255, 255, 255))
    draw_progress_bar(screen, (screen_width // 2, screen_height // 2), (50, 300), progress)
    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()
