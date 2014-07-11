#silly rpg game

import sys, pygame, json, common
#TODO make editor
#TODO make some more game content, at least a few rooms and hallways in a space ship
#TODO   as well as a new set of animations for player
#TODO consolidate code between game and editor
#TODO save game to json file in folder specified by a config.json file in assets/json (for now just save player position)
#TODO interactibles
#TODO npc's that walk around
#TODO dialog with npc's, just like some of the later mspaint games, not just a little avatar
#TODO   but a whole person closeup
#
#TODO the camera can be another surface, smaller than the field, then the player would be in the field...
#TODO can become another npc/person
#TODO more than one person in your party
#TODO dynamic buffering, perhaps in blocks
#TODO cutscenes! move the camera according to a target, which can be "scripted"
#TODO special effects like earth quakes!
#TODO do battle map?


def change_speed(new_speed, velocity):
    def change_velocity_component(new_speed, velocity_component):
        if velocity_component == 0:
            return 0
        if velocity_component < 0:
            return -1 * new_speed
        return new_speed
    return map(lambda velocity_component: change_velocity_component(new_speed, velocity_component), velocity)

def opposite_velocity(velocity):
    return [-1 * component for component in velocity]

class Field(object):

    def __init__(self, field_data):
        self.field_elements = []
        for field_element_data in field_data["field elements"]:
                self.field_elements.append(Field_Element(field_element_data))

    def move(self, xy_offset):
        for field_element in self.field_elements:
            field_element.reposition(xy_offset)

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

    def reposition(self, xy_offset):
        self.rect = self.rect.move(xy_offset)
        if(self.obstacle_rect):
            self.obstacle_rect = self.obstacle_rect.move(xy_offset)

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
        self.speed = int(player_data["walking speed"])

        #put player in center of screen
        screen_rect = screen.get_rect()
        self.rect.centerx = screen_rect.centerx
        self.rect.centery = screen_rect.centery
        self.obstacle_rect = self.obstacle_rect.move([self.rect.left, self.rect.top])

        #set velocity to stopped
        self.velocity = common.stopped

        #TODO replace event keys with command enum and call key stack a command stack
        #initialize maps used to DRY up player code
        #begin maps
        self.animation_state_map = {}
        self.animation_state_map[pygame.K_DOWN] = "walking south"
        self.animation_state_map[pygame.K_UP] = "walking north"
        self.animation_state_map[pygame.K_LEFT] = "walking west"
        self.animation_state_map[pygame.K_RIGHT] = "walking east"
        
        self.velocity_map = {}
        self.velocity_map[pygame.K_DOWN] = change_speed(self.speed, common.down)
        self.velocity_map[pygame.K_UP] = change_speed(self.speed, common.up)
        self.velocity_map[pygame.K_LEFT] = change_speed(self.speed, common.left)
        self.velocity_map[pygame.K_RIGHT] = change_speed(self.speed, common.right)

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
            self.velocity = common.stopped
            self.set_animation_state(self.stop_map[self.animation_states["current"]])

    def tick(self):
        self.animation_tick()
        if self.velocity != common.stopped:
            field.move(opposite_velocity(self.velocity))
            if field.collision_detected(self):
                field.move(self.velocity)

pygame.init()
game_data = json.loads(open('assets/json/sillyRPG.json', 'r').read())
screen = pygame.display.set_mode(game_data["screen size"])
background_color = 0, 0, 0
frame_rate = 60
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

    screen.fill(background_color)
    #TODO field.tick()
    field.blit(screen)
    player.tick()
    player.blit(screen)
    pygame.display.update()
