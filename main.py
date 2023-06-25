import pygame, math, json, cv2
from threading import Thread
from djitellopy import Tello
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

#Set variables for buttons
font = pygame.font.SysFont('Arial', 20)
objects = []

#Set Tello's Speed

ms = 100
ns = 60
ss = 30

dir = []
speed = []
class Background(pygame.sprite.Sprite):

    def __init__(self, image, location, scale):
        pygame.sprite.Sprite.__init__(self)  # Call superclass
        self.image = pygame.image.load(image)
        self.image = pygame.transform.rotozoom(self.image, 0, scale)  # transform the image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress

        self.fillColors = {
            'normal': '#555555',
            'hover': '#666666',
            'pressed': '#333333',
            'right_pressed': '#00FF00'
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

        self.alreadyPressed = False

        objects.append(self)
    def process(self):

        mousePos = pygame.mouse.get_pos()

        self.buttonSurface.fill(self.fillColors['normal'])

        rounding_radius = 10
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])


            if pygame.mouse.get_pressed(num_buttons=3)[2]: # Right button
                self.buttonSurface.fill(self.fillColors['pressed'])

                if self.onePress:
                    self.onclickFunction()

                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        window.blit(self.buttonSurface, self.buttonRect)
def button_forward():

    print('Button Forward')
    dir.append(1)

def button_left():
    print('Button Left')
    dir.append(2)

def button_right():
    print('Button Right')
    dir.append(3)
def button_max_speed():
    print('Button Max_Speed')
    speed.append(100)
def button_normal_speed():
    print('Button Normal_Speed')
    speed.append(60)
def button_slow_speed():
    print('Button Slow_Speed')
    speed.append(30)

def button_test ():
    print('test')


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

customButton = Button(10,  20, 70, 40, 'Forward', button_forward)
customButton = Button(100, 20, 70, 40, 'Left', button_left)
customButton = Button(200, 20, 70, 40, 'Right', button_right)
customButton = Button(300, 20, 90, 40, 'Max_Speed', button_max_speed)
customButton = Button(420, 20, 110, 40, 'Normal_Speed', button_normal_speed)
customButton = Button(560, 20, 100, 40, 'Slow_Speed', button_slow_speed)


# Load Image
bground = Background('image.png', [0, 0], 1.2)  # The given image can be rescaled change last parameter
window.blit(bground.image, bground.rect)



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                drawing = True
                pos = pygame.mouse.get_pos()
                path.append(pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left button
                drawing = False

                if index > 0:
                    pygame.draw.line(window, black, path[index - 1], pos, 2)
                index += 1

    for object in objects:
        object.process()
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
path_dir = []
path_speed = []


for index in range(len(path_dist_cm)):
    waypoints.append({
        "dir": dir[index],
        "dist_cm": path_dist_cm[index],
        "dist_px": path_dist_px[index],
        "angle": path_angle[index],
        "speed": speed[index]

    })

f = open('waypoint.json', 'w+')
path.pop(0)  # We do not want the dummy position

json.dump({
    "wp": waypoints,
    "pos": path
}, f, indent=4)
f.close()

"""
# TELLO #
"""