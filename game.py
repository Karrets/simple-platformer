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
    def rgb(self):
        return self.rgb

    #Sets the rgb value of the Rect
    def set_rgb(self, new_val):
        self.rgb = new_val

    #Returns corners X,Y values in order from 1-4
    def corners(self):
        return [self.corner1,self.corner2,self.corner3,self.corner4]

    #Used to set new collision values, for example to make a moving platform
    def set_corners(self, new_corner1, new_corner2, new_corner3, new_corner4):
        self.corner0 = new_corner0
        self.corner1 = new_corner1
        self.corner2 = new_corner2
        self.corner3 = new_corner3

    #Return render corners
    def render_corners(self):
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
        obj_type is an int value with the following vals (0 and 1 reserved for air and ground)
        2 = Level Goal
        3 = Enemy
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
    
    def obj_type(self):
        return self.obj_type

    #Returns the RGB array
    def rgb(self):
        return self.rgb

    #Sets the rgb value of the Rect
    def set_rgb(self, new_val):
        self.rgb = new_val

    #Returns corners X,Y values in order from 1-4
    def corners(self):
        return [self.corner1,self.corner2,self.corner3,self.corner4]

    #Used to set new collision values, for example to make a moving platform
    def set_corners(self, new_corner1, new_corner2, new_corner3, new_corner4):
        self.corner0 = new_corner0
        self.corner1 = new_corner1
        self.corner2 = new_corner2
        self.corner3 = new_corner3

    #Return render corners
    def render_corners(self):
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
    def __init__(self, id, objects, special_objects):
        self.id = id
        self.objects = objects
        self.special_objects = special_objects
    
    #Levels should not allow dynamically adding or removing objects.

    #Hands out the rectangles of a given level
    def objects(self):
        return self.objects
    
    #Hands out special objects such as enemies or level goals
    def special_objects(self):
        return self.special_objects

    def collide(self, x_pos, y_pos):
        for item in self.objects:
            if Point(x_pos, y_pos).within(Polygon(item.corners)):
                return 1
        for item in self.special_objects:
            if Point(x_pos, y_pos).within(Polygon(item.corners)):
                return item.obj_type
        return 0

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
    def size(self):
        return self.size
    
    #returns rgb value as array of length 3
    def rgb(self):
        return self.rgb

    #returns xy couplet
    def xy_pos(self):
        return self.xy_pos

    #Sets xy values to given values
    def set_xy_pos(self, new_x, new_y):
        self.xy_pos = (new_x, new_y)

    #returns couplet of x and y accel values
    def xy_accel(self):
        return self.xy_accel

    #Sets xy accel values to given values
    def set_xy_accel(self, new_x_accel, new_y_accel):
        self.xy_accel = (new_x_accel, new_y_accel)

    #Returns the what the xy coords would be if the current accel values were added
    def next_pos(self):
        return (self.xy_pos[0] + self.xy_accel[0], self.xy_pos[1] + self.xy_accel[1])

    #Updates the players position based on accel xy values
    def update(self):
        self.xy_pos = (self.xy_pos[0] + self.xy_accel[0], self.xy_pos[1] + self.xy_accel[1])

class GameInstance:
    def __init__(self, screen_wh, done, level_num):
        self.screen_wh = screen_wh
        self.done = done
        self.ticker = 0
        self.level_num = level_num

    def screen_wh(self):
        return self.screen_wh
    
    def done(self):
        return self.done

    def finish(self):
        self.done = True
    
    def ticker(self):
        return self.ticker

    def tick(self):
        self.ticker += 1

    def level_num(self):
        return self.level_num

    def inc_level_num(self):
        curLevel = LEVELS[self.level_num]
        for dRectangle in curLevel.getRectangles:
            print(dRectangle.getCorners)

    def new_player(self, size, rgb, xy_pos, xy_accel):
        self.player = PlayerObject(size, rgb, xy_pos, xy_accel)

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
        player.set_xy_accel(player.xy_accel[0], player.xy_accel[1] - 1)
    if PRESSED[pygame.K_a]:
        player.set_xy_accel(player.xy_accel[0] - 1, player.xy_accel[1])
    if PRESSED[pygame.K_d]:
        player.set_xy_accel(player.xy_accel[0] + 1, player.xy_accel[1])
    if PRESSED[pygame.K_s]:
        player.set_xy_accel(player.xy_accel[0], player.xy_accel[1] + 1)

    premod_xy_accel = Game.player.xy_accel
    while LEVELS[Game.level_num].collide(Game.player.next_pos[0], Game.player.xy_pos[1]) != 0:
        if premod_xy_accel[0] >= 0:
            Game.player.set_xy_accel(Game.player.xy_accel[0] - 0.1, Game.player.xy_accel[1])
        if premod_xy_accel[0] < 0:
            Game.player.set_xy_accel(Game.player.xy_accel[0] + 0.1, Game.player.xy_accel[1])
    player.update()

CLOCK = pygame.time.Clock()
Game = GameInstance((1280, 700), False, 0)
Game.new_player(45, (0, 128, 255), (0, 0), (0, 0))
SCREEN = pygame.display.set_mode(Game.screen_wh)

while Game.done == False:
    #Create functional quit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game.finish()

    SCREEN.fill((50, 100, 255))

    input_handler(Game.player)

    pygame.display.flip()
    Game.tick()
    CLOCK.tick(60)