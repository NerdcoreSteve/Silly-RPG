#silly rpg editor

import sys, pygame, json, common
def render(screen):
    screen.fill(background_color)
    field.blit(screen)
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
field = common.Field(game_data["field"])
clock = pygame.time.Clock()
render(screen)

clicked_field_element = False
while True:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        sys.exit()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            sys.exit()
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.dict['button'] == 1:
            clicked_field_element = get_clicked_field_element(field, event.dict['pos'])
    elif event.type == pygame.MOUSEBUTTONUP:
        if event.dict['button'] == 1:
            clicked_field_element == False
    elif event.type == pygame.MOUSEMOTION:
        if event.dict['buttons'] == (1, 0, 0):
            if clicked_field_element:
                clicked_field_element.reposition(event.dict['rel'])
                render(screen)
