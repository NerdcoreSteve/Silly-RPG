import sys, pygame, json
#Remember you are on a branch for the top TODO!
#TODO finish making player speed part of player object 
#TODO finish todo's sprinkled within code
#TODO save game to json file in folder specified by a config.json file in assets/json (for now just save player position)
#TODO
#TODO do other todos below, npc's, objects and maybe a few other things before tackling the camera
#TODO the camera can be another surface, smaller than the field, then the player would be in the field...
#TODO once camera is done, do dynamic buffering, perhaps in blocks
#TODO special effects like earth quakes!
#TODO cutscenes! move the camera according to a target, which can be "scripted"

game_data = json.loads(open('assets/json/sillyRPG.json', 'r').read())

frame_rate = 60
#TODO This should be part of the player object
player_walking_speed = int(game_data["player"]["walking speed"])
screen_size = 400, 300
background_color = 0, 0, 0

#TODO it should be 1 instead of player_walking_speed, then when the player moves it will be
#TODO [i*self.speed for i in direction] make function for this generalized purpose? number_times_array(number, array)
#TODO a lot of this stuff 
right   = [ 1,  0]
left    = [-1,  0]
up      = [ 0, -1]
down    = [ 0,  1]
stopped = [ 0,  0]

def velocity(speed, direction):
    return [speed * component for component in direction]

def opposite(direction):
    if direction == down:
        return up
    if direction == up:
        return down
    if direction == left:
        return right
    if direction == right:
        return left
    return stopped

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

        #put player in center of screen
        screen_rect = screen.get_rect()
        self.rect.centerx = screen_rect.centerx
        self.rect.centery = screen_rect.centery
        self.obstacle_rect = self.obstacle_rect.move([self.rect.left, self.rect.top])

        #set velocity to stopped
        self.velocity = stopped

        #TODO replace event keys with command enum and call key stack a command stack
        #initialize maps used to DRY up player code
        #begin maps
        self.animation_state_map = {}
        self.animation_state_map[pygame.K_DOWN] = "walking south"
        self.animation_state_map[pygame.K_UP] = "walking north"
        self.animation_state_map[pygame.K_LEFT] = "walking west"
        self.animation_state_map[pygame.K_RIGHT] = "walking east"
        
        self.velocity_map = {}
        self.velocity_map[pygame.K_DOWN] = down
        self.velocity_map[pygame.K_UP] = up
        self.velocity_map[pygame.K_LEFT] = left
        self.velocity_map[pygame.K_RIGHT] = right

        self.stop_map = {}
        self.stop_map["walking south"] = "standing south"
        self.stop_map["walking north"] = "standing north"
        self.stop_map["walking west"] = "standing west"
        self.stop_map["walking east"] = "standing east"
        #end maps

        #stack used so that player controls feel natural
        self.key_stack = []

    #TODO change from key down/up to add_command, remove_command
    def key_down(self, field, event_key):
        self.key_stack.append(event_key)
        self.set_movement_appropriate_animation_state()

    def key_up(self, field, event_key):
        self.key_stack.remove(event_key)
        self.set_movement_appropriate_animation_state()

    def set_movement_appropriate_animation_state(self):
        #The very last command sets player motion
        if self.key_stack: #if stack not empty
            self.velocity = self.velocity_map[self.key_stack[-1]] #peek
            self.set_animation_state(self.animation_state_map[self.key_stack[-1]])
        else:
            self.velocity = stopped
            self.set_animation_state(self.stop_map[self.animation_states["current"]])

    def tick(self):
        self.animation_tick()
        if self.velocity != stopped:
            field.move(opposite(self.velocity))
            if field.collision_detected(self):
                field.move(self.velocity)

pygame.init()
screen = pygame.display.set_mode(screen_size)

#TODO use screen size from game_data here?
player = Player(screen, game_data["player"])
field = Field(game_data["field"])

clock = pygame.time.Clock()

while True:
    clock.tick(frame_rate)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            else:
                player.key_down(field, event.key)
        elif event.type == pygame.KEYUP:
            player.key_up(field, event.key)

    #TODO ticks should only happen on clock ticks!
    screen.fill(background_color)
    #TODO field.tick()
    field.blit(screen)
    player.tick()
    player.blit(screen)
    pygame.display.update()
