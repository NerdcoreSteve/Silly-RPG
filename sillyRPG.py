#TODO collision rects of a size different than their images
#     draw a refrigerator and put it in the grass, make the grass not obst
#     refrige is obst with separate coll rect
#TODO animation (think earthbound, two frames for each direction, flip for left and
#     right
#TODO load json data files
#TODO game editor, mouse controlled w hotkeys? keep it updated with features of game
#TODO make more images and make more game content with editor
#TODO document all in wiki, where to put todo?
#TODO interact with people and objects
#     switches and doors and stuff.
#     text and drawing primitives for word balloons and other menus
#     avatars in dialog boxes, timed printing out of dialog
#TODO re-read homestuck for inspiration
#TODO adventure game inventory
#TODO armor, weapons, items, etc
#TODO find items in field, treasure chests, people
#TODO money and shopping
#TODO Battle engine: final fantasy? chrono trigger? earthbound?
#TODO attack, pyshcic powers
#TODO in field, reading minds, pyschic influence, telekinesis to move and retrieve things
#TODO replay or research kotor for inspiration
#TODO experience rewards: items that gain exp?
#TODO limit your feature set so you can finish this thing.

import sys, pygame

class Game_Object(object):
    def __init__(self, image_path, location, is_obstacle):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(location)
        self.is_obstacle = is_obstacle
    def blit(self, screen):
        screen.blit(self.image, self.rect)

class Field(object):
    def __init__(self):
        self.field_objects = [Game_Object("assets/images/grass.png", [0, 0], True),
                              Game_Object("assets/images/sidewalk.png", [218, 145], False)]
    def move(self, direction):
        for field_object in self.field_objects:
            field_object.rect = field_object.rect.move(direction)
    def collision_detected(self, player):
        for field_object in self.field_objects:
            if field_object.is_obstacle:
                if field_object.rect.colliderect(player.rect):
                    return 1
        return 0
    def blit(self, screen):
        for field_object in self.field_objects:
            field_object.blit(screen)

class Player(Game_Object):
    def __init__(self, image_path, screen):
        Game_Object.__init__(self, image_path, [0, 0], False)
        screen_rect = screen.get_rect()
        self.rect.centerx = screen_rect.centerx
        self.rect.centery = screen_rect.centery
    def move(self, direction, field):
        field.move(direction)
        if field.collision_detected(self):
            field.move([-1 * direction[0], -1 * direction[1]])

speed = 3
right = [speed, 0]
left = [-1 * speed, 0]
up = [0, -1 * speed]
down = [0, speed]

pygame.init()
screen_size = width, height = 800, 600
screen = pygame.display.set_mode(screen_size)
black = 0, 0, 0

player = Player("assets/images/player.png", screen)
field = Field()

frame_rate = 60
clock = pygame.time.Clock()

while 1:
    clock.tick(frame_rate)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(right, field)
    if keys[pygame.K_RIGHT]:
        player.move(left, field)
    if keys[pygame.K_DOWN]:
        player.move(up, field)
    if keys[pygame.K_UP]:
        player.move(down, field)

    screen.fill(black)
    field.blit(screen)
    player.blit(screen)
    pygame.display.update()
