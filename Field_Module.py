import sys, pygame, re, json
from Field_Object_Module import Field_Object

class Field(object):
    def __init__(self, field_data):
        self.field_objects = [Field_Object(field_data["objects"][0]["image"], field_data["objects"][0]["position"], field_data["objects"][0]["collision rectangle"]), Field_Object(field_data["objects"][1]["image"], field_data["objects"][1]["position"])]
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


