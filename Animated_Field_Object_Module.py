import sys, pygame, re, json
from Field_Object_Module import Field_Object

class Animated_Field_Object(Field_Object):
    def __init__(self, position_offset, state_data):
        if "collision rectangle" in state_data:
            obstacle_rect_points = state_data["collision rectangle"]
        else:
            obstacle_rect_points = 0
        Field_Object.__init__(self, 
            state_data["animation states"][state_data["current animation state"]]["image"],
            position_offset,
            obstacle_rect_points)
        self.state_data = state_data
        self.change_state(state_data["current animation state"])
    def change_state(self, animation_state):
        if animation_state in self.state_data["animation states"] and \
           self.state_data["current animation state"] is not animation_state:
            self.state_data["current animation state"] = animation_state
            current_state = self.get_state_data()
            self.current_frame = 0
            self.counter = 0
            if "frames" in current_state:
                self.set_animation_frame()
            else:
                self.set_image(current_state["image"])
    def count_or_next_frame(self):
        current_state = self.get_state_data()
        if "frames" in current_state:
            self.counter += 1
            if self.counter > current_state["frames"][self.current_frame]["delay"]:
                self.counter = 0
                self.current_frame += 1
                if self.current_frame > len(current_state["frames"]) - 1:
                    self.current_frame = 0
                self.set_animation_frame()
    def get_state(self):
        return self.state_data["current animation state"]
    def get_state_data(self):
        return self.state_data["animation states"][self.get_state()]
    def set_animation_frame(self):
        current_state = self.get_state_data()
        frames_directory = current_state["frames directory"]
        image = current_state["frames"][self.current_frame]["image"]
        self.set_image(frames_directory + image)
