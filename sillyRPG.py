# http://www.pygame.org/docs/tut/MoveIt.html
# http://www.pygame.org/docs/tut/newbieguide.html
# http://www.libsdl.org/
# http://www.brunningonline.net/simon/python/quick-ref2_0.html
# http://docs.python.org/release/1.5.1p1/tut/contents.html

#TODO put this up on github
#TODO make sure the player is always in the dead center
#TODO collision detection http://stackoverflow.com/questions/8195649/python-pygame-collision-detection-with-rects
#TODO animation (think earthbound, two frames for each direction, flip for left and
#     right
#TODO load json data files
#TODO game editor, only keyboard controlled for now, keep it updated with features of game
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

class GameObject:
    def __init__(self, imagePath, location):
        self.image = pygame.image.load(imagePath)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(location)
    def blit(self, screen):
        screen.blit(self.image, self.rect)

class Field:
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
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
black = 0, 0, 0

player = GameObject("assets/images/player.png", [400, 300])
field = Field()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

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
