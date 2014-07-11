#silly rpg game

import sys, pygame, json, common

pygame.init()
game_data = json.loads(open('assets/json/sillyRPG.json', 'r').read())
screen = pygame.display.set_mode(game_data["screen size"])
background_color = 0, 0, 0
frame_rate = 60
player = common.Player(game_data["screen size"], game_data["player"])
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
