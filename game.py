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

pygame.init()
game_data = json.loads(open('assets/json/sillyRPG.json', 'r').read())
screen = pygame.display.set_mode(game_data["screen size"])
background_color = 0, 0, 0
frame_rate = 60
player = common.Player(screen, game_data["player"])
field = common.Field(game_data["field"])
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
    player.tick(field)
    player.blit(screen)
    pygame.display.update()
