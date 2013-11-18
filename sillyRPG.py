import sys, pygame

class Field_Object(object):
    def __init__(self, image_path, position_offset, obstacle_rect_points = 0):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        if obstacle_rect_points:
            self.obstacle_rect = pygame.Rect(obstacle_rect_points[0], obstacle_rect_points[1],
                                             obstacle_rect_points[2], obstacle_rect_points[3])
        else:
            self.obstacle_rect = False
        self.reposition(position_offset)
    def blit(self, screen):
        screen.blit(self.image, self.rect)
    def reposition(self, position_offset):
        self.rect = self.rect.move(position_offset)
        if(self.obstacle_rect):
            self.obstacle_rect = self.obstacle_rect.move(position_offset)
    def collision_detected(self, field_object):
        return self.obstacle_rect.colliderect(field_object.obstacle_rect)

class Animated_Field_Object(Field_Object):
    def __init__(self, image_path, position_offset, obstacle_rect_points = 0, states):
        Field_Object.__init__(self, image_path, position_offset, obstacle_rect_points)
        #"current state":<the current animated state name>
        #<name of state>:"array":<an array of frame image paths in order>
        #<name of state>:"dict":<keys are image paths from array, values are frame delay of that image>
        self.states = states 
        self.current_frame = 0
        self.counter = 0
    def change_state(self, state):
        if state in self.states:
            self.states["current state"] = state
            self.counter = 0
    def count_or_next_frame(self):
        self.counter++
        current_state = self.states["current state"]
        delay = current_state["array"][self.current_frame]
        if delay > self.counter:
            self.current_frame++
            if self.current_frame > len(current_state["array"]) - 1:
                self.current_frame = 0
            self.image_path = current_state["array"][self.current_frame]

class Player(Animated_Field_Object):
    def __init__(self, image_path, screen):
        Animated_Field_Object.__init__(self, image_path, [0, 0], [29, 75, 25, 15])
        screen_rect = screen.get_rect()
        self.rect.centerx = screen_rect.centerx
        self.rect.centery = screen_rect.centery
        self.obstacle_rect = self.obstacle_rect.move([self.rect.left, self.rect.top])
    def move(self, direction, field):
        field.move(direction)
        if field.collision_detected(self):
            field.move([-1 * direction[0], -1 * direction[1]])
        #change_animation_state("walk " + direction)

class Field(object):
    def __init__(self):
        self.field_objects = [Field_Object("assets/images/grass.png", [0, 0], [0, 0, 218, 145]),
                              Field_Object("assets/images/sidewalk.png", [218, 145])]
    def move(self, direction):
        for field_object in self.field_objects:
            field_object.reposition(direction)
    def collision_detected(self, player):
        for field_object in self.field_objects:
            if field_object.obstacle_rect:
                if field_object.collision_detected(player):
                    return True
        return False
    def blit(self, screen):
        for field_object in self.field_objects:
            field_object.blit(screen)

speed = 3
right = [speed, 0]
left = [-1 * speed, 0]
up = [0, -1 * speed]
down = [0, speed]

pygame.init()
screen_size = width, height = 800, 600
screen = pygame.display.set_mode(screen_size)
black = 0, 0, 0

player = Player("assets/images/player/player_front1.png", screen)
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
        #player.move("right", field) #for animation
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
