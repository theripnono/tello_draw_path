import pygame, math
from pygame.math import Vector2

# Initialize Pygame
pygame.init()

# Set the width and height of the canvas
width, height = 300, 300

# Create the canvas surface
canvas = pygame.display.set_mode((width, height))

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


    # Draw the line while drawing is True Calculate and display the angle
        # TODO CALCULATE IN REAL TIME ANGLES
        if len(path) >= 2:
            angle = calculate_angle(path[-2], path[-1])
            rad_text = f"Rad: {angle:.2f}"
            font = pygame.font.Font(None, 20)
            text = font.render(rad_text, True, (0, 0, 0))
            canvas.blit(text, (current_pos.x + 10, current_pos.y + 10))


def calculate_angle(start_pos:list, end_pos:list)->float:
    direction = end_pos - start_pos
    angle = math.degrees(math.atan2(direction.y, direction.x))
    return angle

def calculate_distance(start_pos, end_pos):
    """
    Calculate the distance between two positions
    :param start_pos: Starting position as a Vector2
    :param end_pos: Ending position as a Vector2
    :return: Distance between the positions as a float
    """
    direction = end_pos - start_pos
    distance = direction.length()
    return distance

def store_segments(path):
    """
    Store the segments, their angles, distances, and directions in a dictionary
    :param path: list of Vector2 objects representing the path
    :return: dictionary of segments, angles, distances, and directions
    """
    segments = {}
    for i in range(len(path) - 1):
        start_pos = path[i]
        end_pos = path[i + 1]
        direction = end_pos - start_pos
        angle = calculate_angle(start_pos, end_pos)
        distance = calculate_distance(start_pos, end_pos)
        segments[f"Segment {i+1}"] = {
            "coordinates": {
                "start_pos": tuple(start_pos),
                "end_pos": tuple(end_pos)
            },
            "vector_results": tuple(direction),
            "degrees": int(angle),
            "distance": int(distance)
        }
    return segments
# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Right mouse button
                drawing = False
                right_click_pressed = False
            elif event.button == 1:  # Left mouse button
                if not drawing:
                    drawing = True
                    start_pos = Vector2(event.pos)
                    path.append(start_pos)
                    if start_pos is not None:
                        dots.append(start_pos)

                else:
                    end_pos = Vector2(event.pos)
                    path.append(end_pos)
                    dots.append(end_pos)
                    angle = calculate_angle(path[-2], path[-1])
                    #print(f"star_pos: {start_pos}")
                    #print(f"end_pos: {end_pos}")
                    #print(f"Cosine: {angle}")

    # Clear the canvas
    canvas.fill((255, 255, 255))

    # Call the function to draw the path, dots, and line
    draw_path(canvas, path, dots, drawing, start_pos)

    # After drawing the path, call the store_segments function
    tracking_path = store_segments(path)


    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
print(tracking_path)