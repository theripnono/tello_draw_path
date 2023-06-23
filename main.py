"""
The initial code is based on the RobotAndCode YT video.
Big thanks to him to show the bases of the path planning GUI.
"""

import pygame, math, json

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
width = 720
height = 720

# Colors Palette
black = (0, 0, 0)
white = (255, 255, 255)

# Create the window
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Drone Tracking")
window.fill(white)


"""
# RESCALE MAP SIZE #
As an example I will assume that 20 pixels of the image is equal to 500 cm
20px = 500cm --> 500 / 20 = 25
"""
map_size = 25

path = []
index = 0
drawing = False


class Background(pygame.sprite.Sprite):

    def __init__(self, image, location, scale):
        pygame.sprite.Sprite.__init__(self)  # Call superclass
        self.image = pygame.image.load(image)
        self.image = pygame.transform.rotozoom(self.image, 0, scale)  # transform the image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def get_distance(p0: tuple, p1: tuple) -> int:
    """
    Get Distance between 2 points
    :param p0: First tuple position
    :param p1: Second tuple position
    :return: It returns the distance between these 2 points
    """
    x = abs(p0[0] - p1[0])
    y = abs(p0[1] - p1[1])

    # distance in pixels and cm
    dist_px = int(math.hypot(x, y))
    dist_cm = int(dist_px * map_size)  # This value can change depends on or your specific requirements

    return dist_px, dist_cm


def get_angle(p0: tuple, p1: tuple, p_ref: tuple) -> float:
    """
    Get angle between two lines respective to p_ref
    :param p0: First tuple position
    :param p1: Second tuple position
    :param p_ref: The referenced created angle between these two points
    :return: It returns the angle
    """
    dx1 = p1[0] - p_ref[0]
    dy1 = p1[1] - p_ref[1]
    dx0 = p0[0] - p_ref[0]
    dy0 = p0[1] - p_ref[1]

    angle1 = math.atan2(dy1, dx1)
    angle0 = math.atan2(dy0, dx0)

    angle = int(math.degrees(angle1 - angle0))

    return angle


# Load Image
bground = Background('image.png', [0, 0], 1.2)  # The given image can be rescaled change last parameter
window.blit(bground.image, bground.rect)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            pos = pygame.mouse.get_pos()
            path.append(pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False

            if index > 0:
                pygame.draw.line(window, black, path[index - 1], pos, 2)
            index += 1

    pygame.display.update()

#Append first p_ref
path.insert(0, (path[0][0], path[0][1] - 10)) #Dummy pos_ref

# Compute the waypoints
path_dist_cm = []
path_dist_px = []
path_angle = []

for index in range(len(path)):
    #skip the first and second index
    if index > 1:
        dist_px, dist_cm = get_distance(path[index - 1], path[index])
        path_dist_cm.append(dist_cm)
        path_dist_px.append(dist_px)

    # skip the first and last index
    if index > 0 and index < (len(path) - 1):
        angle = get_angle(path[index - 1], path[index + 1], path[index])
        path_angle.append(angle)


# Generate JSON Waypoints

waypoints = []

for index in range(len(path_dist_cm)):
    waypoints.append({
        "dist_cm": path_dist_cm[index],
        "dist_px": path_dist_px[index],
        "dist_angle": path_angle[index],
    })

f = open('waypoint.json', 'w+')
path.pop(0)  # We do not want the dummy position
json.dump({
    "wp": waypoints,
    "pos": path
}, f, indent=4)
f.close()
