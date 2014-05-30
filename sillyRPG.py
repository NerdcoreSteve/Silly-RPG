import sys, pygame, json

class Field(object):

    def __init__(self, field_data):
        self.field_elements = []
        for object_dict in field_data["elements"]:
            if "collision rectangle" in object_dict:
                self.field_elements.append(Field_Element(object_dict["image"], \
                                           object_dict["position"], \
                                           object_dict["collision rectangle"]))
            else:
                self.field_elements.append(Field_Element(object_dict["image"], \
                                           object_dict["position"]))
    def move(self, direction):
        for field_element in self.field_elements:
            field_element.reposition(direction)

    def collision_detected(self, player):
        for field_element in self.field_elements:
            if field_element.obstacle_rect:
                if field_element.collision_detected(player):
                    return True
        return False

    def blit(self, screen):
        for field_element in self.field_elements:
            field_element.blit(screen)

class Field_Element(object):

    def __init__(self, image_path, position_offset, obstacle_rect_points = 0):
        self.set_image(image_path)
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

    def collision_detected(self, field_element):
        return self.obstacle_rect.colliderect(field_element.obstacle_rect)

    def set_image(self, image_path, flip = False):
        self.image = pygame.image.load(image_path)
        if flip:
            self.image = pygame.transform.flip(self.image, True, False)

class Animated_Field_Element(Field_Element):

    def __init__(self, position_offset, state_data):
        if "collision rectangle" in state_data:
            obstacle_rect_points = state_data["collision rectangle"]
        else:
            obstacle_rect_points = 0
        Field_Element.__init__(self, 
            state_data["animation states"][state_data["current animation state"]]["image"],
            position_offset,
            obstacle_rect_points)
        self.state_data = state_data
        self.change_animation_state(state_data["current animation state"])

    def change_animation_state(self, animation_state):
        if animation_state in self.state_data["animation states"] and \
                self.state_data["current animation state"] is not animation_state:
            self.state_data["current animation state"] = animation_state
            current_state = self.get_state_data()
            self.current_frame = 0
            self.counter = 0
            if "frames" in current_state:
                self.set_animation_frame()
            else:
                flip = False
                if "transform" in current_state and current_state["transform"] == "flip":
                    flip = True
                self.set_image(current_state["image"], flip)

    def tick(self):
        current_state = self.get_state_data()
        if "frames" in current_state:
            self.counter += 1
            if self.counter > current_state["frames"][self.current_frame]["delay"]:
                self.counter = 0
                self.current_frame += 1
                if self.current_frame > len(current_state["frames"]) - 1:
                    self.current_frame = 0
                self.set_animation_frame()

    def get_state(self):
        return self.state_data["current animation state"]

    def get_state_data(self):
        return self.state_data["animation states"][self.get_state()]

    def set_animation_frame(self):
        current_state = self.get_state_data()
        frames_directory = current_state["frames directory"]
        image = current_state["frames"][self.current_frame]["image"]
        #TODO I'm checking for flip in two places, is bad
        flip = False
        if "transform" in current_state["frames"][self.current_frame] \
           and current_state["frames"][self.current_frame]:
            flip = True;
        self.set_image(frames_directory + image, flip)

class Player(Animated_Field_Element):

    def __init__(self, screen, player_data):
        Animated_Field_Element.__init__(self, [0, 0], player_data)
        screen_rect = screen.get_rect()
        #TODO this should be part of the Field_Element class code
        self.rect.centerx = screen_rect.centerx
        self.rect.centery = screen_rect.centery
        self.obstacle_rect = self.obstacle_rect.move([self.rect.left, self.rect.top])
            
game_data = json.loads(open('assets/game_json/sillyRPG.json', 'r').read())

#TODO speed, screen size, and frame rate should be in the json
speed = 3
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
        player.change_animation_state("walking west")
        #TODO maybe the player should detect collisions?
        if field.collision_detected(player):
            field.move(left)
    elif keys[pygame.K_RIGHT]:
        field.move(left)
        player.change_animation_state("walking east")
        if field.collision_detected(player):
            field.move(right)
    elif keys[pygame.K_DOWN]:
        field.move(up)
        player.change_animation_state("walking south")
        if field.collision_detected(player):
            field.move(down)
    elif keys[pygame.K_UP]:
        field.move(down)
        player.change_animation_state("walking north")
        if field.collision_detected(player):
            field.move(up)
    else:
        if(player.get_state() is "walking south"):
            player.change_animation_state("standing south")
        elif(player.get_state() is "walking north"):
            player.change_animation_state("standing north")
        elif(player.get_state() is "walking west"):
            player.change_animation_state("standing west")
        elif(player.get_state() is "walking east"):
            player.change_animation_state("standing east")

    screen.fill(black)
    field.blit(screen)
    player.blit(screen)
    pygame.display.update()
