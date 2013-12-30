import sys, pygame, re, json
from Animated_Field_Object_Module import Animated_Field_Object

class Player(Animated_Field_Object):
    def __init__(self, screen, game_data, player_data):
        Animated_Field_Object.__init__(self, [0, 0], player_data)
        screen_rect = screen.get_rect()
        self.rect.centerx = screen_rect.centerx
        self.rect.centery = screen_rect.centery
        self.obstacle_rect = self.obstacle_rect.move([self.rect.left, self.rect.top])
    def move(self, direction, field):
        field.move(direction)
        if field.collision_detected(self):
            field.move([-1 * direction[0], -1 * direction[1]])
