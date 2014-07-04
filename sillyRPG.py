import sys, pygame, json

class Field(object):

    def __init__(self, field_data):
        self.field_elements = []
        for field_element_data in field_data["field elements"]:
                self.field_elements.append(Field_Element(field_element_data))

    def move(self, direction):
        for field_element in self.field_elements:
            field_element.reposition(direction)

    def collision_detected(self, other_field_element):
        for field_element in self.field_elements:
            if field_element.obstacle_rect:
                if field_element.collision_detected(other_field_element):
                    return True
        return False

    def blit(self, screen):
        for field_element in self.field_elements:
            field_element.blit(screen)

class Field_Element(object):

    def __init__(self, field_element_data):
        self.image = False
        self.rect = False
        self.obstacle_rect = False
        if "image" in field_element_data:
            self.set_image(field_element_data["image"])
            self.rect = self.image.get_rect()
        if "collision rectangle" in field_element_data:
            self.obstacle_rect = pygame.Rect(field_element_data["collision rectangle"][0], 
                                             field_element_data["collision rectangle"][1],
                                             field_element_data["collision rectangle"][2],
                                             field_element_data["collision rectangle"][3])
        #Since the inital position is always 0,0 we can give position as position offset
        if "position" in field_element_data:
            self.reposition(field_element_data["position"])

    def blit(self, screen):
        screen.blit(self.image, self.rect)

    def reposition(self, position_offset):
        self.rect = self.rect.move(position_offset)
        if(self.obstacle_rect):
            self.obstacle_rect = self.obstacle_rect.move(position_offset)

    def collision_detected(self, field_element):
        return self.obstacle_rect.colliderect(field_element.obstacle_rect)

    def set_image(self, image_path, flip = False):
        self.image = pygame.image.load(image_path)
        if flip:
            self.image = pygame.transform.flip(self.image, True, False)

class Animated_Field_Element(Field_Element):

    def __init__(self, animated_field_element_data):
        Field_Element.__init__(self, animated_field_element_data)
        self.animation_states = animated_field_element_data["animation states"]
        self.animation_states["current"] = ""
        self.set_animation_state(self.animation_states["start"])
        self.set_animation_frame() #sets image
        self.rect = self.image.get_rect()

    def set_animation_state(self, new_animation_state):
        if new_animation_state in self.animation_states and \
           self.animation_states["current"] is not new_animation_state:
            self.animation_states["current"] = new_animation_state
            self.current_frame = 0
            self.counter = 0

    def set_animation_frame(self):
        flip = False
        current_animation_state_data = \
            self.animation_states[self.animation_states["current"]]
        if "static image" in current_animation_state_data:
            image = current_animation_state_data["static image"]
            if "transform" in current_animation_state_data and \
               current_animation_state_data["transform"] == "flip":
                flip = True
        else:
            image = current_animation_state_data["frames directory"]
            image_data = current_animation_state_data["frames"][self.current_frame]
            image += image_data["image"]
            if "transform" in image_data and \
               image_data["transform"] == "flip":
                flip = True
        self.set_image(image, flip)

    def current_animation_state(self):
        return self.animation_states["current"]

    def tick(self):
        current_animation_state_data = \
            self.animation_states[self.animation_states["current"]]
        if "frames" in current_animation_state_data:
            self.counter += 1
            if self.counter > current_animation_state_data["frames"][self.current_frame]["delay"]:
                self.counter = 0
                self.current_frame += 1
                if self.current_frame > len(current_animation_state_data["frames"]) - 1:
                    self.current_frame = 0
                self.set_animation_frame()

class Player(Animated_Field_Element):

    def __init__(self, screen, player_data):
        Animated_Field_Element.__init__(self, player_data)
        screen_rect = screen.get_rect()
        self.rect.centerx = screen_rect.centerx
        self.rect.centery = screen_rect.centery
        self.obstacle_rect = self.obstacle_rect.move([self.rect.left, self.rect.top])
            
game_data = json.loads(open('assets/json/sillyRPG.json', 'r').read())

#TODO speed, screen size, and frame rate should be in the json
speed = 5
right = [speed, 0]
left = [-1 * speed, 0]
up = [0, -1 * speed]
down = [0, speed]

pygame.init()
screen_size = width, height = 800, 600
screen = pygame.display.set_mode(screen_size)
black = 0, 0, 0

player = Player(screen, game_data["player"])
field = Field(game_data["field"])

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

    player.tick()

    #TODO this if-block sure looks ugly
    #TODO some variant of the command pattern I think
    #TODO with a dictionary matching keys to directions, and a dictionary for opposite directions
    #TODO also collision detection in this if-block is bad
    #player.move(field, direction_map[.......
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        field.move(right)
        player.set_animation_state("walking west")
        if field.collision_detected(player):
            field.move(left)
    elif keys[pygame.K_RIGHT]:
        field.move(left)
        player.set_animation_state("walking east")
        if field.collision_detected(player):
            field.move(right)
    elif keys[pygame.K_DOWN]:
        field.move(up)
        player.set_animation_state("walking south")
        if field.collision_detected(player):
            field.move(down)
    elif keys[pygame.K_UP]:
        field.move(down)
        player.set_animation_state("walking north")
        if field.collision_detected(player):
            field.move(up)
    else:
        if(player.current_animation_state() is "walking south"):
            player.set_animation_state("standing south")
        elif(player.current_animation_state() is "walking north"):
            player.set_animation_state("standing north")
        elif(player.current_animation_state() is "walking west"):
            player.set_animation_state("standing west")
        elif(player.current_animation_state() is "walking east"):
            player.set_animation_state("standing east")

    screen.fill(black)
    field.blit(screen)
    player.blit(screen)
    pygame.display.update()
