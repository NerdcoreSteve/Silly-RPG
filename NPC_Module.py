import sys, pygame, re, json
from Animated_Field_Object_Module import Animated_Field_Object

class NPC(Animated_Field_Object):
    def __init__(self, screen, npc_data):
        #TODO hard-code for now, use json
        Animated_Field_Object.__init__(self, [0, 0], player_data)
