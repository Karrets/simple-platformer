import pygame
from shapely.geometry import Point, Polygon

#TODO: Get "special objects working, (Enemies?, Level Goal, ETC"

pygame.init()

SCREEN_X = 1280
SCREEN_Y = 700
SCREEN = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
DONE = False

PLAYER_SIZE = 45
PLAYER_COLOR = (0, 128, 255)
PLAYER_X = 0
PLAYER_Y = 0
PLAYER_ACCEL_X = 0
PLAYER_ACCEL_Y = 0

LEVEL_NUM = 0

LEVELS_COLLISION_MAP = [
    [#DEBUG LEVEL
        [
            [0, 460], [1024, 460], [1024, 576], [0, 576]
        ], #Main Floor
        [
            [0, 300], [300, 300], [300, 350], [0, 350]
        ], #Platform
        [
            [1000, 460], [1000, 0], [1024, 0], [1024, 460]
        ] #Right wall
    ],
    [
        [
            [0, 460], [1024, 460], [1024, 576], [0, 576]
        ],
        [
            [0, 300], [300, 300], [300, 350], [0, 350]
        ],
        [
            [1000, 460], [1000, 0], [1024, 0], [1024, 460]
        ]
    ]
]
LEVELS = [
    [#DEBUG LEVEL
        [
            [[0, 460], [1024, 460], [1024, 576], [0, 576]],
            [255, 128, 0]
        ], #Main Floor
        [
            [[0, 300], [300, 300], [300, 350], [0, 350]],
            [255, 128, 255]
        ], #Platform
        [
            [[1000, 460], [1000, 0], [1024, 0], [1024, 460]],
            [0, 255, 128]
        ] #Right wall
    ],
    [
        [
            [[0, 460], [1024, 460], [1024, 576], [0, 576]],
            [255, 128, 0]
        ], #Main Floor
        [
            [[0, 300], [300, 300], [300, 350], [0, 350]],
            [255, 128, 255]
        ], #Platform
        [
            [[1000, 460], [1000, 0], [1024, 0], [1024, 460]],
            [0, 255, 128]
        ] #Right wall
    ]
]

def next_level(level_num):
    for level_object in LEVELS[level_num]:
        for coord_set in level_object[0]:
            coord_set[0] /= 2
            coord_set[1] /= 2

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

    pygame.display.flip()
    CLOCK.tick(60)
