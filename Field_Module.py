import sys, pygame, re, json
from Field_Object_Module import Field_Object

class Field(object):
    def __init__(self, field_data):
        self.field_objects = [Field_Object(field_data["objects"][0]["image"], [0, 0], [0, 0, 218, 145]),
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
