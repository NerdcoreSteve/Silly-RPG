import sys, pygame, re, json, pprint

#TODO need to figure out why player isn't reading json right

class Field_Object(object):
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
    def set_image(self, image_path):
        match_groups = re.match(r'^flip (.*)', image_path)
        if match_groups:
            self.image = pygame.image.load(match_groups.group(1))
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = pygame.image.load(image_path)


class Animated_Field_Object(Field_Object):
    def __init__(self, image_path, position_offset, states, states2, obstacle_rect_points = 0):
        Field_Object.__init__(self, image_path, position_offset, obstacle_rect_points)
        self.states = states
        self.states2 = states2
        self.change_state(self.states2["player"]["current animation state"])
    def change_state(self, state):
        if state in self.states and self.states["current state"] is not state:
            self.states["current state"] = state
            self.current_frame = 0
            self.counter = 0
            if "array" in self.states[state]:
                self.set_image(self.states[state]["array"][self.current_frame])
            else:
                self.set_image(image_path = self.states[state]["static image"])
    def count_or_next_frame(self):
        current_state = self.states[self.states["current state"]]
        if "dict" in current_state:
            self.counter += 1
            delay = current_state["dict"][current_state["array"][self.current_frame]]
            if self.counter > delay:
                self.counter = 0
                self.current_frame += 1
                if self.current_frame > len(current_state["array"]) - 1:
                    self.current_frame = 0
                self.set_image(current_state["array"][self.current_frame])
    def get_state(self):
        return self.states["current state"]

class Player(Animated_Field_Object):
    def __init__(self, screen, game_data, player_data):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(player_data["current animation state"])
        image_path = player_data["animation states"][player_data["current animation state"]]["static image"];
        Animated_Field_Object.__init__(self, image_path, [0, 0], game_data, game_data2, [29, 75, 25, 15])
        screen_rect = screen.get_rect()
        self.rect.centerx = screen_rect.centerx
        self.rect.centery = screen_rect.centery
        self.obstacle_rect = self.obstacle_rect.move([self.rect.left, self.rect.top])
    def move(self, direction, field):
        field.move(direction)
        if field.collision_detected(self):
            field.move([-1 * direction[0], -1 * direction[1]])

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

    player.count_or_next_frame()

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
