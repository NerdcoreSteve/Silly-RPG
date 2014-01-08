import sys, pygame, re, json
from Field_Object_Module import Field_Object

class Field(object):
    def __init__(self, field_data):
        self.field_objects = []
        for object_dict in field_data["objects"]:
            if "collision rectagle" in object_dict:
                self.field_objects.append(Field_Object(object_dict["image"], object_dict["position"], object_dict["collision rectangle"]))
            else:
                self.field_objects.append(Field_Object(object_dict["image"], object_dict["position"]))
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


