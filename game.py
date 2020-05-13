import pygame

#Class system made with great help from my friend https://github.com/Jcdiem
class LevelRect: #This is a basic plarform, it's the main thing in the game.
    def __init__(self, corner0, corner1, rgb):
        """ Create a rectangle for use and storage with the main game
        Each corner should be an array in [x,y] format
        RGB should be an array in [r,g,b] format
        """

        self.corner0 = corner0                      #This converts the 2 corner format to a
        self.corner1 = [corner0[0], corner1[1]]     #4 corner format to be used by the pygame renderer.
        self.corner2 = corner1
        self.corner3 = [corner1[0], corner0[1]]
        self.render_corner0 = self.corner0          #This describes the render corners, this is simply
        self.render_corner1 = self.corner1          #Copied over to be offset and then further modified later.
        self.render_corner2 = self.corner2
        self.render_corner3 = self.corner3 
        self.rgb = rgb                              #Simply the color in rgb of the level object.
    

    #The following is getters and setters, used to modify and obtain values stored in a class.
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
        self.corner0 = new_corner1
        self.corner1 = new_corner2
        self.corner2 = new_corner3
        self.corner3 = new_corner4

    #Return render corners
    def render_corners(self):
        return [self.render_corner0,self.render_corner1,self.render_corner2,self.render_corner3]

    #Used to set new render positions, does not affect collison handling
    def set_render_corners(self, new_corner1, new_corner2, new_corner3, new_corner4):
        self.render_corner0 = new_corner1
        self.render_corner1 = new_corner2
        self.render_corner2 = new_corner3
        self.render_corner3 = new_corner4

    #These two special getters are used later for collision detection.
    def get_top_left(self):
        return self.corner0

    def get_bottom_right(self):
        return self.corner2

class SpecialObject:    #This is a special object, they were never fully implemented,
                        #but they would include enemies and the goal
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
    
    #getter for this object type in particular to get the object type, used to determine collision.
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

    def get_top_left(self):
        return self.corner0

    def get_bottom_right(self):
        return self.corner3

class GameLevel:    #This class defines individual level objects, only one is ever created, but more are supported.
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

    #Used to find if an xy pos is colliding with the level and what it's colliding with.
    #Because everything is recangles, the computation is very cheap.
    def collide(self, x_pos, y_pos):
        for item in self.objects:
            minx = item.get_top_left()[0]
            miny = item.get_top_left()[1]
            maxx = item.get_bottom_right()[0]
            maxy = item.get_bottom_right()[1]
            if minx <= x_pos <= maxx:
                if miny <= y_pos <= maxy:
                    return 1
        for item in self.special_objects:
            minx = item.get_top_left()[0]
            miny = item.get_top_left()[1]
            maxx = item.get_bottom_right()[0]
            maxy = item.get_bottom_right()[1]
            if minx <= x_pos <= maxx:
                if miny <= y_pos <= maxy:
                    return item.obj_type
        return 0

class PlayerObject: #A simple object to hold player data. While more than one player could be made, only one would work.
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

    #Returns the what the xy coords would be if the current accel values were added (Largely used for collisions)
    def next_pos(self):
        return (self.xy_pos[0] + self.xy_accel[0], self.xy_pos[1] + self.xy_accel[1])

    #Updates the players position based on accel xy values
    def update(self):
        self.xy_pos = (self.xy_pos[0] + self.xy_accel[0], self.xy_pos[1] + self.xy_accel[1])

class GameInstance: #Used to control a few misc items, creating more than one wont do anything.
    def __init__(self, screen_wh, done, level_num):
        self.screen_wh = screen_wh
        self.done = done
        self.ticker = 0
        self.level_num = level_num

    #Returns width height couplet
    def screen_wh(self):
        return self.screen_wh
    
    #Asks if the game is complete, somewhat redundant as if the game is done you probably can't call this.
    def done(self):
        return self.done

    #Calling this ends the game.
    def finish(self):
        self.done = True
    
    #A general ticker used for things that dont need to be done every frame.
    def ticker(self):
        return self.ticker

    #Increment the ticker, called every frame.
    def tick(self):
        self.ticker += 1

    #returns the level number.
    def level_num(self):
        return self.level_num

    #Increments the level number / level, not implemented and therefor broken.
    def inc_level_num(self):
        curLevel = LEVELS[self.level_num]
        for dRectangle in curLevel.getRectangles:
            print(dRectangle.getCorners)

    def new_player(self, size, rgb, xy_pos, xy_accel):
        self.player = PlayerObject(size, rgb, xy_pos, xy_accel)

#This is the only level ever seen by the player, It's labeled as level zero, as if I ever continue this
#Project this level would be skipped.
#Name of level         id
LEVEL_ZERO = GameLevel(0,[
        #Array of level objects

        #Main Floor
        #New Rect  Corner1    Corner2     R   G  B
        LevelRect([0, 460], [1024, 576], [255,128,0]),
    
        #Platform
        #New Rect  Corner1    Corner2   R    G    B
        LevelRect([0, 300], [300, 350],[255, 128, 255]),
    
        #Right Wall
        #New Rect  Corner1      Corner2    R   G    B
        LevelRect([1000, 0], [1024, 460],[255, 128, 0])
    ],
    [
        #Level End
        #New Level Goal  Corner1      Corner2    Corner3     Corner4      id   R   G   B
        SpecialObject([1000, 400], [1000, 460], [1060, 400], [1060, 460], 0, [0, 0, 255])
    ]
)

#This is simply a duplicate of the first level.
LEVEL_ONE = GameLevel(1,[
        LevelRect([0, 460], [1024, 576], [255,128,0]), #Main Floor
        LevelRect([0, 300], [300, 350], [255, 128, 255]), #Platform
        LevelRect([1000, 0], [1024, 460], [255, 128, 0]) #Right Wall
    ],[
        SpecialObject([1000, 400], [1000, 460], [1060, 400], [1060, 460], 0, [0, 0, 255]) #Level End
    ])

#A list of all the levels.
LEVELS = [
    LEVEL_ZERO,
    LEVEL_ONE
]

#Check all four corners for collision. As soon as one collision is found it reports it, it does not tell wou
#which corner. (Only worries about next horizontal step.)
def player_collision_x(player):
    failed = 0
    if LEVELS[Game.level_num].collide(player.next_pos()[0], player.xy_pos[1]) != 0:
        return True
    if LEVELS[Game.level_num].collide(player.next_pos()[0] + player.size, player.xy_pos[1]) != 0:
        return True
    if LEVELS[Game.level_num].collide(player.next_pos()[0], player.xy_pos[1] + player.size) != 0:
        return True
    if LEVELS[Game.level_num].collide(player.next_pos()[0] + player.size, player.xy_pos[1] + player.size) != 0:
        return True

    return False

#Same as prior, but only worries about vertical steps.
def player_collision_y(player):
    failed = 0
    if LEVELS[Game.level_num].collide(player.xy_pos[0], player.next_pos()[1]) != 0:
        failed += 1
    if LEVELS[Game.level_num].collide(player.xy_pos[0] + player.size, player.next_pos()[1]) != 0:
        failed += 1
    if LEVELS[Game.level_num].collide(player.xy_pos[0], player.next_pos()[1] + player.size) != 0:
        failed += 1
    if LEVELS[Game.level_num].collide(player.xy_pos[0] + player.size, player.next_pos()[1] + player.size) != 0:
        failed += 1

    return bool(failed > 0)

#All things input handler. ANy keypress that should be factored is here.
def input_handler(player):
    PRESSED = pygame.key.get_pressed() #A shortcut to make it easier to call this function.

    #Adds acceleration if keys are pressed.
    if PRESSED[pygame.K_w] or PRESSED[pygame.K_SPACE]:
        if LEVELS[Game.level_num].collide(player.xy_pos[0], player.next_pos()[1] + player.size + 1):
            player.set_xy_accel(player.xy_accel[0], -30)
        elif LEVELS[Game.level_num].collide(player.xy_pos[0] - 4, player.next_pos()[1] + player.size + 1):
            player.set_xy_accel(15, -20)
        if LEVELS[Game.level_num].collide(player.xy_pos[0] + player.size, player.next_pos()[1] + player.size + 1):
            player.set_xy_accel(player.xy_accel[0], -30)            
        elif LEVELS[Game.level_num].collide(player.xy_pos[0] + player.size + 4, player.next_pos()[1] + player.size + 1):
            player.set_xy_accel(-15, -20)
    if PRESSED[pygame.K_a]:
        player.set_xy_accel(player.xy_accel[0] - 0.8, player.xy_accel[1])
    if PRESSED[pygame.K_d]:
        player.set_xy_accel(player.xy_accel[0] + 0.8, player.xy_accel[1])

    #Some extra stuff to make the player more floaty when the spacebar is held down.
    if (PRESSED[pygame.K_w] or PRESSED[pygame.K_SPACE]) and player.xy_accel[1] < 0:
        player.set_xy_accel(player.xy_accel[0], player.xy_accel[1] + 0.9)
    else:
        player.set_xy_accel(player.xy_accel[0], player.xy_accel[1] + 1.8)

    #A run button, makes you go just a bit faster.
    if (PRESSED[pygame.K_LSHIFT] or PRESSED[pygame.K_LCTRL]):
        player.set_xy_accel(player.xy_accel[0] / 1.03, player.xy_accel[1] / 1.05)
    else:
        player.set_xy_accel(player.xy_accel[0] / 1.05, player.xy_accel[1] / 1.05)

    #Used by the upcoming to determine what the acceleration was before they tampered with it.
    premod_xy_accel = Game.player.xy_accel

    #Makes sure the next step is in bounds.
    #Fix x accel
    while player_collision_x(player):
        if premod_xy_accel[0] >= 0:
            player.set_xy_accel(player.xy_accel[0] - 0.1, player.xy_accel[1])
        if premod_xy_accel[0] < 0:
            player.set_xy_accel(player.xy_accel[0] + 0.1, player.xy_accel[1])
    #Fix y accel
    while player_collision_y(player):
        if premod_xy_accel[1] >= 0:
            player.set_xy_accel(player.xy_accel[0], player.xy_accel[1] - 0.1)
        if premod_xy_accel[1] < 0:
            player.set_xy_accel(player.xy_accel[0], player.xy_accel[1] + 0.1)

    #Calls the function to upddate player position based on acceleration.
    player.update()

#Used to offset the render corners of all objects. Tampering with these number cause purely graphical changes
#But they will likely not work properly as the values are calculated based on the players position on the screen.
def init_level_render_offset(game):
    for level in LEVELS:
        for level_object in level.objects:
            level_object.set_render_corners(
            (level_object.render_corner0[0] + Game.screen_wh[0] * (3 / 8), + level_object.render_corner0[1] + Game.screen_wh[1] / 2),
            (level_object.render_corner1[0] + Game.screen_wh[0] * (3 / 8), + level_object.render_corner1[1] + Game.screen_wh[1] / 2),
            (level_object.render_corner2[0] + Game.screen_wh[0] * (3 / 8), + level_object.render_corner2[1] + Game.screen_wh[1] / 2),
            (level_object.render_corner3[0] + Game.screen_wh[0] * (3 / 8), + level_object.render_corner3[1] + Game.screen_wh[1] / 2)
        )

#Used to draw all standard level objects, special objects are not drawn even if they are there.
def draw_level(game):
    for level_object in LEVELS[Game.level_num].objects:
        level_object.set_render_corners(
            (level_object.render_corner0[0] - Game.player.xy_accel[0], + level_object.render_corner0[1] - Game.player.xy_accel[1]),
            (level_object.render_corner1[0] - Game.player.xy_accel[0], + level_object.render_corner1[1] - Game.player.xy_accel[1]),
            (level_object.render_corner2[0] - Game.player.xy_accel[0], + level_object.render_corner2[1] - Game.player.xy_accel[1]),
            (level_object.render_corner3[0] - Game.player.xy_accel[0], + level_object.render_corner3[1] - Game.player.xy_accel[1])
        )
        pygame.draw.polygon(SCREEN, level_object.rgb, level_object.render_corners())

#Draws the player to the center of the screen, applies a skew to make the player
#look like its leaning into it's movements.
def draw_player(game):
    points = [
        [Game.screen_wh[0] * (3 / 8), Game.screen_wh[1] / 2],
        [Game.screen_wh[0] * (3 / 8) + Game.player.size, Game.screen_wh[1] / 2],
        [Game.screen_wh[0] * (3 / 8) + Game.player.size, Game.screen_wh[1] / 2+ Game.player.size],
        [Game.screen_wh[0] * (3 / 8), Game.screen_wh[1] / 2+ Game.player.size]
        ]

    #Simply caps the speed so that if you somehow get too much, shape doesn't get to deformed.
    softened_speed = [0, 0]
    if abs(Game.player.xy_accel[0]) <= 1: softened_speed[0] = 0
    else: softened_speed[0] = Game.player.xy_accel[0]

    if abs(Game.player.xy_accel[1]) <= 1: softened_speed[1] = 0
    else: softened_speed[1] = Game.player.xy_accel[1]

    points[0][1] -= softened_speed[1] * 0.75
    points[1][1] -= softened_speed[1] * 0.75
    points[0][0] += softened_speed[0] * 0.75
    points[1][0] += softened_speed[0] * 0.75

    #Converst the points into tuples instead of lists becuase otherwise pygame gets angry >:(
    tuple_points = [
        (points[0][0], points[0][1]),
        (points[1][0], points[1][1]),
        (points[2][0], points[2][1] + 1),
        (points[3][0], points[3][1] + 1)
        ]
    pygame.draw.polygon(SCREEN, Game.player.rgb, tuple_points)

#Some misc variables needed for pygame to function properly.
CLOCK = pygame.time.Clock()
Game = GameInstance((1280, 720), False, 0)
Game.new_player(45, (0, 255, 255), (0, 0), (0, 0))
SCREEN = pygame.display.set_mode(Game.screen_wh)

#Done before the game starts. if you comment this out, everything will look broken.
init_level_render_offset(Game)

#The primary game loop, used to manage everything using the functions and classes made prior.
while Game.done == False:
    #Create functional quit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game.finish()

    #Makes the background all blue, this color can be changed with no repercussions.
    SCREEN.fill((50, 100, 255))

    input_handler(Game.player)
    draw_level(Game)
    draw_player(Game)

    pygame.display.flip()
    Game.tick()
    CLOCK.tick(60)