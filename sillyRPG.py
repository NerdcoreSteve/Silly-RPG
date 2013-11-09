# http://www.pygame.org/docs/tut/MoveIt.html
# http://www.pygame.org/docs/tut/newbieguide.html
# http://www.libsdl.org/
# http://www.brunningonline.net/simon/python/quick-ref2_0.html
# http://docs.python.org/release/1.5.1p1/tut/contents.html

#TODO get rid of camel case
#TODO process_events(event)
#TODO player.move(pygame.key.get_pressed, field)
#TODO directions are members of field
#TODO speed should be a member of player
#TODO collision detection http://stackoverflow.com/questions/8195649/python-pygame-collision-detection-with-rects
#     make art for some object and make 
#TODO collision rects of a size different than their images
#TODO animation (think earthbound, two frames for each direction, flip for left and
#     right
#TODO load json data files
#TODO game editor, mouse controlled w hotkeys? keep it updated with features of game
#TODO make more images and make more game content with editor
#TODO document all in wiki, where to put todo?
#TODO interact with people and objects
#     text and drawing primitives for word balloons and other menus
#TODO adventure game inventory
#TODO Battle engine: final fantasy? chrono trigger? earthbound?
#TODO attack, pyshcic powers
#TODO armor, weapons, items, etc
#TODO find items in field, treasure chests, people
#TODO money and shopping
#TODO and so on.

import sys, pygame

class GameObject(object):
    def __init__(self, imagePath, location):
        self.image = pygame.image.load(imagePath)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(location)
    def blit(self, screen):
        screen.blit(self.image, self.rect)

class Player(GameObject):
    def __init__(self, imagePath, screen):
        GameObject.__init__(self, imagePath, [0, 0])
        screenRect = screen.get_rect()
        self.rect.centerx = screenRect.centerx
        self.rect.centery = screenRect.centery

class Field(object):
    def __init__(self):
        self.fieldObjects = [GameObject("assets/images/grass.png", [0, 0]),
                             GameObject("assets/images/sidewalk.png", [218, 145])]
    def move(self, direction):
        for fieldObject in self.fieldObjects:
            fieldObject.rect = fieldObject.rect.move(direction)
    def blit(self, screen):
        for fieldObject in self.fieldObjects:
            fieldObject.blit(screen)

speed = 3
right = [speed, 0]
left = [-1 * speed, 0]
up = [0, -1 * speed]
down = [0, speed]

pygame.init()
screenSize = width, height = 800, 600
screen = pygame.display.set_mode(screenSize)
black = 0, 0, 0

player = Player("assets/images/player.png", screen)
field = Field()

while 1:
    #TODO process_events(event)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

    #TODO player.move(pygame.key.get_pressed, field)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        field.move(right)
    if keys[pygame.K_RIGHT]:
        field.move(left)
    if keys[pygame.K_DOWN]:
        field.move(up)
    if keys[pygame.K_UP]:
        field.move(down)

    screen.fill(black)
    field.blit(screen)
    player.blit(screen)
    pygame.display.flip()
