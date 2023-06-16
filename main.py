import pygame, math
from pygame.math import Vector2

# Initialize Pygame
pygame.init()

# Set the width and height of the canvas
width, height = 400, 400

# Create the canvas surface
canvas = pygame.display.set_mode((width, height))
image_path = r'C:\Users\Theri\Escritorio\tello_draw_path\drone.png'
# Fill the canvas with white color
canvas.fill((255, 255, 255))

# Variables to track the drawing state
drawing = False
start_pos = None
end_pos = None
path = []  # List to store the drawn path
dots = []  # List to store the dots representing the path

static_drone = False  # Variable to track the static drone stat



def load_image(image_path,resize_width,resize_height):
    # Load the drone image
    drone_image = pygame.image.load(image_path)

    # Resize the image
    drone_image = pygame.transform.scale(drone_image, (resize_width, resize_height))

    return drone_image

drone_image = load_image(image_path, 50, 50)  # Load the drone image



def draw_path(canvas, path, drone_image, drawing, start_pos):
    # Draw the path
    if len(path) > 1:
        pygame.draw.lines(canvas, (0, 0, 0), False, path, 2)

    # Draw the drone image at each path position with rotation based on current mouse position
    for pos in path[:-1]:
        # Calculate the angle between the drone position and current mouse position
        current_pos = Vector2(pygame.mouse.get_pos())
        direction = current_pos - pos
        angle = math.degrees(math.atan2(direction.y, direction.x))

        # Adjust the angle by adding 90 degrees
        angle += 90

        # Rotate the drone image
        rotated_image = pygame.transform.rotate(drone_image, -angle)
        image_pos = Vector2(pos) - Vector2(rotated_image.get_size()) / 2

        # Draw the rotated drone image
        canvas.blit(rotated_image, image_pos)

    # Draw the drone image at the latest position (current mouse position)
    if path:
        current_pos = path[-1]

        # Calculate the angle between the drone position and current mouse position
        if start_pos is not None:
            direction = Vector2(pygame.mouse.get_pos()) - current_pos
            angle = math.degrees(math.atan2(direction.y, direction.x))

            # Adjust the angle by adding 90 degrees
            angle += 90

            # Rotate the drone image
            rotated_image = pygame.transform.rotate(drone_image, -angle)
            image_pos = Vector2(current_pos) - Vector2(rotated_image.get_size()) / 2

            # Draw the rotated drone image
            canvas.blit(rotated_image, image_pos)

    # Draw the line while drawing is True
    if drawing and start_pos is not None:
        current_pos = Vector2(pygame.mouse.get_pos())
        pygame.draw.line(canvas, (0, 0, 0), path[-1], current_pos, 2)

        # Calculate and display the angle
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

    direction = end_pos - start_pos
    distance = direction.length()
    return distance

def store_segments(path):

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


show_segments = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                show_segments = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_h:
                show_segments = False
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
    if show_segments:
        tracking_path = store_segments(path)
        print(tracking_path)

    # Clear the canvas
    canvas.fill((255, 255, 255))

    # Call the function to draw the path, dots, and line
    draw_path(canvas, path, drone_image, drawing, start_pos)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
print(tracking_path)