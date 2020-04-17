import pygame
from shapely.geometry import Point, Polygon

#Class system made with great help from my friend https://github.com/Jcdiem
class LevelRect:
    def __init__(self, corner0, corner1, corner2, corner3, rgb):
        """ Create a rectangle for use and storage with the main game
        Each corner should be an array in [x,y] format
        RGB should be an array in [r,g,b] format
        """
        self.corner0 = corner0
        self.corner1 = corner1
        self.corner2 = corner2
        self.corner3 = corner3
        self.render_corner0 = corner0
        self.render_corner1 = corner1
        self.render_corner2 = corner2
        self.render_corner3 = corner3 
        self.rgb = rgb
    
    #Returns the RGB array
    def get_rgb(self):
        return self.rgb

    #Sets the rgb value of the Rect
    def set_rgb(self, new_val):
        self.rgb = new_val

    #Returns corners X,Y values in order from 1-4
    def get_corners(self):
        return [self.corner1,self.corner2,self.corner3,self.corner4]

    #Used to set new collision values, for example to make a moving platform
    def set_corners(self, new_corner1, new_corner2, new_corner3, new_corner4):
        self.corner0 = new_corner0
        self.corner1 = new_corner1
        self.corner2 = new_corner2
        self.corner3 = new_corner3

    #Return render corners
    def get_render_corners(self):
        return [self.render_corner1,self.render_corner2,self.render_corner3,self.render_corner4]

    #Used to set new render positions, does not affect collison handling
    def set_render_corners(self, new_corner1, new_corner2, new_corner3, new_corner4):
        self.render_corner0 = new_corner0
        self.render_corner1 = new_corner1
        self.render_corner2 = new_corner2
        self.render_corner3 = new_corner3

class SpecialObject:
    def __init__(self, corner0, corner1, corner2, corner3, obj_type, rgb):
        """ Create a special object for use and storage with the main game
        Each corner should be an array in [x,y] format
        obj_type is an int value with the following vals
        0 = Level Goal
        1 = Enemy
        RGB should be an array in [r,g,b] format
        """
        self.corner0 = corner0
        self.corner1 = corner1
        self.corner2 = corner2
        self.corner3 = corner3
        self.render_corner0 = corner0
        self.render_corner1 = corner1
        self.render_corner2 = corner2
        self.render_corner3 = corner3 
        self.obj_type = obj_type
        self.rgb = rgb
    
    #Returns the RGB array
    def get_rgb(self):
        return self.rgb

    #Sets the rgb value of the Rect
    def set_rgb(self, new_val):
        self.rgb = new_val

    #Returns corners X,Y values in order from 1-4
    def get_corners(self):
        return [self.corner1,self.corner2,self.corner3,self.corner4]

    #Used to set new collision values, for example to make a moving platform
    def set_corners(self, new_corner1, new_corner2, new_corner3, new_corner4):
        self.corner0 = new_corner0
        self.corner1 = new_corner1
        self.corner2 = new_corner2
        self.corner3 = new_corner3

    #Return render corners
    def get_render_corners(self):
        return [self.render_corner1,self.render_corner2,self.render_corner3,self.render_corner4]

    #Used to set new render positions, does not affect collison handling
    def set_render_corners(self, new_corner1, new_corner2, new_corner3, new_corner4):
        self.render_corner0 = new_corner0
        self.render_corner1 = new_corner1
        self.render_corner2 = new_corner2
        self.render_corner3 = new_corner3

class GameLevel:
    """Create a game level for parsing
    id should be the numerical value of the level
    rectangles should be an array of LevelRect objects
    """
    def __init__(self, id, rectangles, special_objects):
        self.id = id
        self.rectangles = rectangles
        self.special_objects = special_objects
    
    #Levels should not allow dynamically adding or removing objects.

    #Hands out the rectangles of a given level
    def get_rectangles(self):
        return self.rectangles
    
    #Hands out special objects such as enemies or level goals
    def get_special_objects(self):
        return self.special_objects

class PlayerObject:
    """Basic player object to hold player info
    This includes XY values and corosponding XY Accel values
    The player size and player color
    """
    def __init__(self, size, rgb, xy_pos, xy_accel):
        self.size = size
        self.rgb = rgb
        self.xy_pos = xy_pos
        self.xy_accel = xy_accel

    #returns size as a single int
    def get_size(self):
        return self.size
    
    #returns rgb value as array of length 3
    def get_rgb(self):
        return self.rgb

    #returns xy couplet
    def get_xy_pos(self):
        return self.xy_pos

    #Sets xy values to given values
    def set_xy_pos(self, new_x, new_y):
        self.xy_pos = (new_x, new_y)

    #returns couplet of x and y accel values
    def get_xy_accel(self):
        return self.xy_accel

    #Sets xy accel values to given values
    def set_xy_accel(self, new_x_accel, new_y_accel):
        self.xy_accel = (new_x_accel, new_y_accel)

class GameInstance:
    def __init__(self, screen_wh, done, level_num):
        self.screen_wh = screen_wh
        self.done = done
        self.ticker = 0
        self.level_num = level_num

    def get_screen_wh(self):
        return self.screen_wh
    
    def done(self):
        return self.done

    def finish(self):
        self.done = True
    
    def get_ticker(self):
        return self.ticker

    def inc_ticker(self):
        self.ticker += 1

    def get_level_num(self):
        return self.level_num

    def inc_level_num(self):
        curLevel = LEVELS[self.level_num]
        for dRectangle in curLevel.getRectangles:
            print(dRectangle.getCorners)

#Name of level         id
LEVEL_ZERO = GameLevel(0,[
        #Array of level objects

        #Main Floor
        #New Rect  Corner1    Corner2     Corner3      Corner4    R   G  B
        LevelRect([0, 460], [1024, 460], [1024, 576], [0, 576], [255,128,0]),
    
        #Platform
        #New Rect  Corner1    Corner2    Corner3    Corner4    R    G    B
        LevelRect([0, 300], [300, 300], [300, 350], [0, 350],[255, 128, 255]),
    
        #Right Wall
        #New Rect  Corner1      Corner2    Corner3     Corner4     R   G   B
        LevelRect([1000, 460], [1000, 0], [1024, 0], [1024, 460],[255, 128, 0])
    ],
    [
        #Level End
        #New Level Goal  Corner1      Corner2    Corner3     Corner4      id   R   G   B
        SpecialObject([1000, 460], [1000, 400], [1060, 400], [1060, 460], 0, [0, 0, 255])
    ]
)

LEVEL_ONE = GameLevel(1,[
        LevelRect([0, 460], [1024, 460], [1024, 576], [0, 576], [255,128,0]), #Main Floor
        LevelRect([0, 300], [300, 300], [300, 350], [0, 350],[255, 128, 255]), #Platform
        LevelRect([1000, 460], [1000, 0], [1024, 0], [1024, 460],[255, 128, 0]) #Right Wall
    ],[
        SpecialObject([1000, 460], [1000, 400], [1060, 400], [1060, 460], 0, [0, 0, 255]) #Level End
    ])

LEVELS = [
    LEVEL_ZERO,
    LEVEL_ONE
]

def input_handler(player):
    PRESSED = pygame.key.get_pressed()
    if PRESSED[pygame.K_w] or PRESSED[pygame.K_SPACE]:
        if abs(player.get_xy_accel[1]) < 18:
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


CLOCK = pygame.time.Clock()
Game = GameInstance((1280, 700), False, 0)
SCREEN = pygame.display.set_mode(Game.get_screen_wh())

while Game.done == False:
    #Create functional quit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game.finish()

    SCREEN.fill((50, 100, 255))

    




    pygame.display.flip()
    Game.inc_ticker()
    CLOCK.tick(60)