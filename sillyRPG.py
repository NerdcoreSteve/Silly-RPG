import sys, pygame, json
#TODO doesn't return to standing state
#TODO arrow keys don't work as expected, may need to get hash of bools again

game_data = json.loads(open('assets/json/sillyRPG.json', 'r').read())

#TODO player_speed and screen size should be in the json
frame_rate = 60
player_speed = 5
screen_size = width, height = 400, 300
background_color = 0, 0, 0

right = [player_speed, 0]
left = [-1 * player_speed, 0]
up = [0, -1 * player_speed]
down = [0, player_speed]
nowhere = [0,0]

def opposite(direction):
    if direction == down:
        return up
    if direction == up:
        return down
    if direction == left:
        return right
    if direction == right:
        return left
    return nowhere

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

    def animation_tick(self):
        current_animation_state_data = \
            self.animation_states[self.animation_states["current"]]
        if "frames" in current_animation_state_data:
            self.counter += 1
            delay = current_animation_state_data["frames"][self.current_frame]["delay"]
            if self.counter > delay:
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

        self.direction = nowhere

        self.animation_state_map = {}
        self.animation_state_map[pygame.K_DOWN] = "walking south"
        self.animation_state_map[pygame.K_UP] = "walking north"
        self.animation_state_map[pygame.K_LEFT] = "walking west"
        self.animation_state_map[pygame.K_RIGHT] = "walking east"
        
        self.direction_map = {}
        self.direction_map[pygame.K_DOWN] = down
        self.direction_map[pygame.K_UP] = up
        self.direction_map[pygame.K_LEFT] = left
        self.direction_map[pygame.K_RIGHT] = right
        
        self.stop_map = {}
        self.stop_map["walking south"] = "standing south"
        self.stop_map["walking north"] = "standing north"
        self.stop_map["walking west"] = "standing west"
        self.stop_map["walking east"] = "standing east"

    def go(self, field, event_key):
        if event_key in self.animation_state_map:
            self.set_animation_state(self.animation_state_map[event_key])
            self.direction = self.direction_map[event_key]

    def stop(self):
        self.direction = nowhere
        current_animation_state = self.animation_states["current"]
        self.set_animation_state(self.stop_map[current_animation_state])

    def tick(self):
        self.animation_tick()
        if self.direction != nowhere:
            field.move(opposite(self.direction))
            if field.collision_detected(self):
                field.move(self.direction)

pygame.init()
screen = pygame.display.set_mode(screen_size)

player = Player(screen, game_data["player"])
field = Field(game_data["field"])

clock = pygame.time.Clock()

while 1:
    clock.tick(frame_rate)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            else:
                player.go(field, event.key)
        elif event.type == pygame.KEYUP:
            player.stop()

    screen.fill(background_color)
    #field.tick()
    field.blit(screen)
    player.tick()
    player.blit(screen)
    pygame.display.update()
