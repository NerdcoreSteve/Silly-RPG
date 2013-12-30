import sys, pygame, re, json
from Player_Module import Player
from Field_Module import Field
from Field_Object_Module import Field_Object
from Animated_Field_Object_Module import Animated_Field_Object

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
