import pygame, math
from pygame.math import Vector2

# Initialize Pygame
pygame.init()

# Set the width and height of the canvas
width, height = 300, 300

# Create the canvas surface
canvas = pygame.display.set_mode((width, height))
print(type(canvas))
# Fill the canvas with white color
canvas.fill((255, 255, 255))

# Variables to track the drawing state
drawing = False
start_pos = None
end_pos = None
path = []  # List to store the drawn path
dots = []  # List to store the dots representing the path


def draw_path(canvas:classmethod, path:list, dots:list, drawing:bool, start_pos:bool)->None:
    """
    Draw the segments into the canvas
    :param canvas:
    :param path:
    :param dots:
    :param drawing:
    :param start_pos:
    :return:
    """

    # Draw the path
    if len(path) > 1:
        pygame.draw.lines(canvas, (0, 0, 0), False, path, 2)

    # Draw the dots
    for dot in dots:
        pygame.draw.circle(canvas, (255, 0, 0), (int(dot.x), int(dot.y)), 3)

    # Draw the line while drawing is True
    if drawing and start_pos is not None:
        current_pos = Vector2(pygame.mouse.get_pos())
        pygame.draw.line(canvas, (0, 0, 0), path[-1], current_pos, 2)

def calculate_angle(start_pos, end_pos):
    direction = end_pos - start_pos
    angle = math.degrees(math.atan2(direction.y, direction.x))
    return angle


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Right mouse button
                drawing = False
            elif event.button == 1:  # Left mouse button
                if not drawing:
                    drawing = True
                    start_pos = Vector2(event.pos)
                    path.append(start_pos)
                    dots.append(start_pos)
                else:
                    end_pos = Vector2(event.pos)
                    path.append(end_pos)
                    dots.append(end_pos)
                    angle = calculate_angle(path[-2], path[-1])
                    print(f"star_pos: {start_pos}")
                    print(f"end_pos: {end_pos}")
                    print(f"Cosine: {angle}")

    # Clear the canvas
    canvas.fill((255, 255, 255))

    # Call the function to draw the path, dots, and line
    draw_path(canvas, path, dots, drawing, start_pos)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
