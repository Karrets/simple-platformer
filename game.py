import pygame
from shapely.geometry import Point, Polygon

#DrawnRectangle and GameLevel by https://github.com/Jcdiem; Modified to better suit my needs
class DrawnRectangle:
    def __init__(self, corner1, corner2, corner3, corner4, rgb):
        """ Create a rectangle for use and storage with the main game
        Each corner should be an array in [x,y] format
        RGB should be an array in [r,g,b] format
        """
        self.corner1 = corner1
        self.corner2 = corner2
        self.corner3 = corner3
        self.corner4 = corner4
        self.render_corner1 = corner1
        self.render_corner2 = corner2
        self.render_corner3 = corner3
        self.render_corner4 = corner4 
        self.rgb = rgb
    
    #Returns the RGB array
    def getRGB(self):
        return self.rgb

    #Returns corners X,Y values in order from 1-4
    def getCorners(self):
        return [self.corner1,self.corner2,self.corner3,self.corner4]

    #Return render corners
    def getCorners(self):
        return [self.render_corner1,self.render_corner2,self.render_corner3,self.render_corner4]

class GameLevel:
    """Create a game level for parsing
    id should be the numerical value of the level
    rectangles should be an array of DrawnRectangle objects
    """
    def __init__(self, id, rectangles):
        self.id = id
        self.rectangles = rectangles
    
    def getRectangles(self):
        return self.rectangles

pygame.init()

SCREEN_X = 1280
SCREEN_Y = 700
SCREEN = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
DONE = False

TICKER = 0

PLAYER_SIZE = 45
PLAYER_COLOR = (0, 128, 255)
PLAYER_X = 0
PLAYER_Y = 0
PLAYER_ACCEL_X = 0
PLAYER_ACCEL_Y = 0

LEVEL_NUM = 0

#START EXAMPLE CODE

#Name of level      new lvl  id  start of rectangle array
exampleDebugLevel = GameLevel(0,[#Open bracket for start of levels array
    #Main Floor
    #New Rect       Corner1    Corner2     Corner3      Corner4    R   G  B
    DrawnRectangle([0, 460], [1024, 460], [1024, 576], [0, 576], [255,128,0]),
    #Platform
    DrawnRectangle([0, 300], [300, 300], [300, 350], [0, 350],[255, 128, 255]),
    #Right Wall
    DrawnRectangle([1000, 460], [1000, 0], [1024, 0], [1024, 460],[255, 128, 0])
    ]#End rectangles
)#End making level

#Less cluttered version
exampleDebugNoClutter = GameLevel(0,[
    DrawnRectangle([0, 460], [1024, 460], [1024, 576], [0, 576], [255,128,0]), #Main Floor
    DrawnRectangle([0, 300], [300, 300], [300, 350], [0, 350],[255, 128, 255]), #Platform
    DrawnRectangle([1000, 460], [1000, 0], [1024, 0], [1024, 460],[255, 128, 0]) #Right Wall
    ])

LEVELS = [
    exampleDebugLevel,
    exampleDebugNoClutter
]

def level_iterate():
    curLevel = BETTER_LEVEL_LIST[0]
    for dRectangle in curLevel.getRectangles:
        print(dRectangle.getCorners)

#END EXAMPLE CODE

def next_level(level_num):
    for level_object in LEVELS[level_num]:
        for coord_set in level_object[0]:
            coord_set[0] /= 2
            coord_set[1] /= 2
        for color in level_object[1]:
            color /= 2
    

def init_level_offset():
    for level in LEVELS:
        for level_object in level:
            for coord_set in level_object[0]:
                coord_set[0] += SCREEN_X * (3 / 8)
                coord_set[1] += SCREEN_Y / 2


def draw_player(size, speed, color):
    points = [
        [SCREEN_X * (3 / 8), SCREEN_Y / 2],
        [SCREEN_X * (3 / 8) + size, SCREEN_Y / 2],
        [SCREEN_X * (3 / 8) + size, SCREEN_Y / 2+ size],
        [SCREEN_X * (3 / 8), SCREEN_Y / 2+ size]
        ]

    softened_speed = [0, 0]
    if abs(speed[0]) <= 1: softened_speed[0] = 0
    else: softened_speed[0] = speed[0]

    if abs(speed[1]) <= 1: softened_speed[1] = 0
    else: softened_speed[1] = speed[1]

    points[0][1] -= softened_speed[1] * 0.75
    points[1][1] -= softened_speed[1] * 0.75
    points[0][0] += softened_speed[0] * 0.75
    points[1][0] += softened_speed[0] * 0.75

    tuple_points = [
        (points[0][0], points[0][1]),
        (points[1][0], points[1][1]),
        (points[2][0], points[2][1] + 1),
        (points[3][0], points[3][1] + 1)
        ]
    pygame.draw.polygon(SCREEN, color, tuple_points)

def draw_level(level_num, speed):
    for level_object in LEVELS[level_num - 1]:
        for coord_set in level_object[0]:
            coord_set[0] -= speed[0] * 2
            coord_set[1] -= speed[1]
        pygame.draw.polygon(SCREEN, level_object[1], level_object[0])
    for level_object in LEVELS[level_num]:
        for coord_set in level_object[0]:
            coord_set[0] -= speed[0]
            coord_set[1] -= speed[1]
        pygame.draw.polygon(SCREEN, level_object[1], level_object[0])

def player_collision(x_pos, y_pos, size, x_speed, y_speed, level_num):
    failed = 0
    for item in LEVELS_COLLISION_MAP[level_num]:
        if Point(x_pos + x_speed, y_pos + y_speed).within(Polygon(item)): failed += 1
        if Point(x_pos + x_speed + size, y_pos + y_speed).within(Polygon(item)): failed += 1
        if Point(x_pos + x_speed, y_pos + y_speed + size).within(Polygon(item)): failed += 1
        if Point(x_pos + x_speed + size, y_pos + y_speed + size).within(Polygon(item)): failed += 1

    return bool(failed > 0)

def collide_generic(x_pos, y_pos, level_num):
    failed = 0
    for item in LEVELS_COLLISION_MAP[level_num]:
        if Point(x_pos, y_pos).within(Polygon(item)): failed += 1

    return bool(failed > 0)

def special_object_tests(x_pos, y_pos, size, level_num):
    for level_object in SPECIAL_OBJECTS[level_num]:
        if Point(x_pos + size / 2, y_pos + size / 2).within(Polygon(level_object[1])):
            return level_object[0]


CLOCK = pygame.time.Clock()

init_level_offset()

while not DONE:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            DONE = True

    SCREEN.fill((10, 10, 10))

    PRESSED = pygame.key.get_pressed()
    if PRESSED[pygame.K_w] or PRESSED[pygame.K_SPACE]:
        if abs(PLAYER_ACCEL_Y) < 18:
            if collide_generic(PLAYER_X, PLAYER_Y + PLAYER_SIZE + 2.5, LEVEL_NUM) or collide_generic(PLAYER_X + PLAYER_SIZE, PLAYER_Y + PLAYER_SIZE + 2.5, LEVEL_NUM):
                PLAYER_ACCEL_Y = -17
                PLAYER_ACCEL_X /= 1.5
            elif PLAYER_ACCEL_Y > -5:
                if collide_generic(PLAYER_X + 4 + PLAYER_SIZE, PLAYER_Y + PLAYER_SIZE / 1.25, LEVEL_NUM):
                    PLAYER_ACCEL_Y = -10
                    PLAYER_ACCEL_X = -16
                if collide_generic(PLAYER_X - 4, PLAYER_Y + PLAYER_SIZE / 1.25, LEVEL_NUM):
                    PLAYER_ACCEL_Y = -10
                    PLAYER_ACCEL_X = 16
    if PRESSED[pygame.K_a]:
        if not PRESSED[pygame.K_LSHIFT]:
            PLAYER_ACCEL_X -= 0.7
            if PLAYER_ACCEL_X < -7.5:
                PLAYER_ACCEL_X = -7.5
        else:
            PLAYER_ACCEL_X -= 1
            if PLAYER_ACCEL_X < -12:
                PLAYER_ACCEL_X = -12.5
    if PRESSED[pygame.K_d]:
        if not PRESSED[pygame.K_LSHIFT]:
            PLAYER_ACCEL_X += 0.7
            if PLAYER_ACCEL_X > 7.5:
                PLAYER_ACCEL_X = 7.5
        else:
            PLAYER_ACCEL_X += 1
            if PLAYER_ACCEL_X > 12:
                PLAYER_ACCEL_X = 12.5
    if PRESSED[pygame.K_s]:
        next_level(LEVEL_NUM)
        LEVEL_NUM = 1

    if (PRESSED[pygame.K_w] or PRESSED[pygame.K_SPACE]) and PLAYER_ACCEL_Y < 0:
        PLAYER_ACCEL_Y += 0.5
    else:
        PLAYER_ACCEL_Y += 1.5

    if PLAYER_ACCEL_X > 0: PLAYER_ACCEL_X -= 0.25
    if PLAYER_ACCEL_X < 0: PLAYER_ACCEL_X += 0.25
    if abs(PLAYER_ACCEL_X) <= 0.25: PLAYER_ACCEL_X = 0
    if abs(PLAYER_ACCEL_Y) <= 0.25: PLAYER_ACCEL_Y = 0

    PREMOD_ACCEL_X = PLAYER_ACCEL_X
    while player_collision(PLAYER_X, PLAYER_Y, PLAYER_SIZE, PLAYER_ACCEL_X, 0, LEVEL_NUM):
        if PREMOD_ACCEL_X > 0:
            PLAYER_ACCEL_X -= 1
        if PREMOD_ACCEL_X < 0:
            PLAYER_ACCEL_X += 1
    PLAYER_X += PLAYER_ACCEL_X

    PREMOD_ACCEL_Y = PLAYER_ACCEL_Y
    while player_collision(PLAYER_X, PLAYER_Y, PLAYER_SIZE, 0, PLAYER_ACCEL_Y, LEVEL_NUM):
        if PREMOD_ACCEL_Y > 0:
            PLAYER_ACCEL_Y -= 1
        if PREMOD_ACCEL_Y < 0:
            PLAYER_ACCEL_Y += 1
    PLAYER_Y += PLAYER_ACCEL_Y

    draw_level(LEVEL_NUM, (PLAYER_ACCEL_X, PLAYER_ACCEL_Y))
    draw_player(PLAYER_SIZE, (PLAYER_ACCEL_X, PLAYER_ACCEL_Y), PLAYER_COLOR)

    if TICKER >= 10:
        result = special_object_tests(PLAYER_X, PLAYER_Y, PLAYER_SIZE, LEVEL_NUM)
        if result == 0:
            next_level(LEVEL_NUM)
            LEVEL_NUM += 1
    
    pygame.display.flip()
    TICKER += 1
    CLOCK.tick(60)
