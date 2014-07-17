#silly rpg game

import sys, pygame, json, common

clock = pygame.time.Clock()

while True:
    clock.tick(common.frame_rate)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            else:
                common.player.key_down(common.field, event.key)
        elif event.type == pygame.KEYUP:
            common.player.key_up(common.field, event.key)

    common.screen.fill(common.background_color)
    common.field.blit(common.screen)
    common.player.tick(common.field)
    common.player.blit(common.screen)
    pygame.display.update()
