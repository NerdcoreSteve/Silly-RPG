#silly rpg editor
import sys, pygame, json, common

class Cursor(object):
    def __init__(self):
        self.rect = False
        self.current_field_element = False
        self.line_color = 0, 255, 0
        self.line_thickness = 2

    def draw(self, screen):
        if self.rect:
            pygame.draw.rect(screen, self.line_color, self.rect, self.line_thickness)

    def attach(self, field_element):
        self.current_field_element = field_element
        self.update_position()

    def detach(self):
        self.rect = False

    def update_position(self):
        if self.current_field_element:
            self.rect = self.current_field_element.rect

class Editor_Field(common.Field):
    def __init__(self, field_data):
        common.Field.__init__(self, field_data)

    def move(self, field_element, direction):
        move_map =   {"up": lambda index: index + 1, "down": lambda index: index - 1}
        bounds_map = {"up": lambda index: index >= len(self.field_elements), "down": lambda index: index < 0}
        if direction == "up":
            old_index = self.field_elements.index(field_element)
            new_index = move_map[direction](old_index);
            if bounds_map["up"](new_index):
                new_index = old_index
            self.field_elements.insert(new_index, self.field_elements.pop(old_index))
        elif direction == "down":
            old_index = self.field_elements.index(field_element)
            new_index = move_map[direction](old_index);
            if bounds_map["up"](new_index):
                new_index = old_index
            self.field_elements.insert(new_index, self.field_elements.pop(old_index))

def render(screen, cursor):
    screen.fill(background_color)
    field.blit(screen)
    cursor.draw(screen)
    pygame.display.update()

def get_clicked_field_element(field, click_coordinates):
    clicked_field_element = False
    for field_element in field.field_elements:
        if field_element.rect.collidepoint(click_coordinates):
            clicked_field_element = field_element
    return clicked_field_element

pygame.init()
game_data = json.loads(open('assets/json/sillyRPG.json', 'r').read())
screen = pygame.display.set_mode(game_data["screen size"])
background_color = 0, 0, 0
frame_rate = 60
player = common.Player(game_data["screen size"], game_data["player"])
field = Editor_Field(game_data["field"])
clock = pygame.time.Clock()
cursor = Cursor()
render(screen, cursor)

clicked_field_element = False
while True:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        sys.exit()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_DOWN:
            if(clicked_field_element):
                field.move(clicked_field_element, "down")
        elif event.key == pygame.K_UP:
            if(clicked_field_element):
                field.move(clicked_field_element, "up")
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.dict['button'] == 1:
            clicked_field_element = get_clicked_field_element(field, event.dict['pos'])
            cursor.attach(clicked_field_element)
    elif event.type == pygame.MOUSEBUTTONUP:
        if event.dict['button'] == 1:
            clicked_field_element == False
    elif event.type == pygame.MOUSEMOTION:
        if event.dict['buttons'] == (1, 0, 0):
            if clicked_field_element:
                clicked_field_element.reposition(event.dict['rel'])
                cursor.update_position()
    render(screen, cursor)
