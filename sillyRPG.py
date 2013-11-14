import sys, pygame

class Game_Object(object):
    def __init__(self, image_path, position_offset, obstacle_rect = 0):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.obstacle_rect = obstacle_rect
        self.reposition(position_offset)
    def blit(self, screen):
        screen.blit(self.image, self.rect)
    def reposition(self, position_offset):
        self.rect = self.rect.move(position_offset)
        if(self.obstacle_rect):
            self.obstacle_rect = self.obstacle_rect.move(position_offset)

class Field(object):
    def __init__(self):
        self.field_objects = [Game_Object("assets/images/grass.png", [0, 0], pygame.Rect(0, 0, 218, 145)),
                              Game_Object("assets/images/sidewalk.png", [218, 145])]
    def move(self, direction):
        for field_object in self.field_objects:
            field_object.reposition(direction)
    def collision_detected(self, player):
        for field_object in self.field_objects:
            if field_object.obstacle_rect:
                if field_object.obstacle_rect.colliderect(player.obstacle_rect):
                    return 1
        return 0
    def blit(self, screen):
        for field_object in self.field_objects:
            field_object.blit(screen)

class Player(Game_Object):
    def __init__(self, image_path, screen):
        Game_Object.__init__(self, image_path, [0, 0], pygame.Rect(0, 0, 27, 17))
        screen_rect = screen.get_rect()
        self.rect.centerx = screen_rect.centerx
        self.rect.centery = screen_rect.centery
        self.obstacle_rect = pygame.Rect(self.rect.left + 29, self.rect.top + 75, 25, 15)
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
