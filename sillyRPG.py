import sys, pygame, json

class Field(object):
    def __init__(self, field_data):
        self.field_elements = []
        for object_dict in field_data["elements"]:
            if "collision rectagle" in object_dict:
                self.field_elements.append(Field_Element(object_dict["image"], object_dict["position"], object_dict["collision rectangle"]))
            else:
                self.field_elements.append(Field_Element(object_dict["image"], object_dict["position"]))
    def move(self, direction):
        for field_object in self.field_elements:
            field_object.reposition(direction)
    def collision_detected(self, player):
        for field_object in self.field_elements:
            if field_object.obstacle_rect:
                if field_object.collision_detected(player):
                    return True
        return False
    def blit(self, screen):
        for field_object in self.field_elements:
            field_object.blit(screen)

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
    def collision_detected(self, field_object):
        return self.obstacle_rect.colliderect(field_object.obstacle_rect)
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
        self.change_state(state_data["current animation state"])
    def change_state(self, animation_state):
        if animation_state in self.state_data["animation states"] and \
           self.state_data["current animation state"] is not animation_state:
            self.state_data["current animation state"] = animation_state
            current_state = self.get_state_data()
            self.current_frame = 0
            self.counter = 0
            if "frames" in current_state:
                self.set_animation_frame()
            else:
                self.set_image(current_state["image"])
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
        flip = False
        if "transform" in current_state["frames"][self.current_frame]:
            flip = True;
        self.set_image(frames_directory + image, flip)

class Player(Animated_Field_Element):
    def __init__(self, screen, game_data, player_data):
        Animated_Field_Element.__init__(self, [0, 0], player_data)
        screen_rect = screen.get_rect()
        self.rect.centerx = screen_rect.centerx
        self.rect.centery = screen_rect.centery
        self.obstacle_rect = self.obstacle_rect.move([self.rect.left, self.rect.top])
    def move(self, direction, field):
        field.move(direction)
        if field.collision_detected(self):
            field.move([-1 * direction[0], -1 * direction[1]])

class NPC(Animated_Field_Element):
    def __init__(self, screen, npc_data):
        #TODO hard-code for now, use json
        Animated_Field_Element.__init__(self, [0, 0], player_data)
            
game_data = json.loads(open('sillyRPG.json', 'r').read())
game_data2 = json.loads(open('sillyRPGj2.json', 'r').read())

speed = 3
right = [speed, 0]
left = [-1 * speed, 0]
up = [0, -1 * speed]
down = [0, speed]

pygame.init()
screen_size = width, height = 800, 600
screen = pygame.display.set_mode(screen_size)
black = 0, 0, 0

player = Player(screen, game_data, game_data2["player"])
field = Field(game_data2["field"])

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

    #can I put how states transition in the json? maybe lock them to keys?
    #put them as actual keys for now but perhaps as intermediary map ids later?
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(right, field)
        player.change_state("walking east")
    elif keys[pygame.K_RIGHT]:
        player.move(left, field)
        player.change_state("walking west")
    elif keys[pygame.K_DOWN]:
        player.move(up, field)
        player.change_state("walking south")
    elif keys[pygame.K_UP]:
        player.move(down, field)
        player.change_state("walking north")
    else:
        if(player.get_state() is "walking south"):
            player.change_state("standing south")
        elif(player.get_state() is "walking north"):
            player.change_state("standing north")
        elif(player.get_state() is "walking west"):
            player.change_state("standing west")
        elif(player.get_state() is "walking east"):
            player.change_state("standing east")

    screen.fill(black)
    field.blit(screen)
    player.blit(screen)
    pygame.display.update()
