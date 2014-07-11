#silly rpg editor

import sys, pygame, json, common
#TODO consolidate code between editor and game
#TODO hotkeys, from now on any changes need both mouse and hot keys
#TODO undo-redo
#TODO change z depth
    #TODO right click move down, move up, send to front/back
#TODO edit collision rect, drag, edit fields, toggle existence, set to image dimensions
#TODO see list of images, and other assets on side, edit them from there too
#TODO browse assets/images folder for images to create new field elements
#TODO edit player
#TODO save changes to sillyRPG.json
    #TODO maybe take out object methods belonging to game domain and just make them functions
#TODO both game and editor should have a game file and saved-game file pickers
    #TODO create new games

def render():
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
player = common.Player(screen, game_data["player"])
field = common.Field(game_data["field"])
clock = pygame.time.Clock()
render()

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
                render()
