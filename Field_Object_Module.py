import sys, pygame, re, json

class Field_Object(object):
    def __init__(self, image_path, position_offset, obstacle_rect_points = 0):
        self.set_image(image_path)
        self.rect = self.image.get_rect()
        if obstacle_rect_points:
            self.obstacle_rect = pygame.Rect(obstacle_rect_points[0], obstacle_rect_points[1],
                                             obstacle_rect_points[2], obstacle_rect_points[3])
        else:
            self.obstacle_rect = False
        self.reposition(position_offset)
    def blit(self, screen):
        screen.blit(self.image, self.rect)
    def reposition(self, position_offset):
        self.rect = self.rect.move(position_offset)
        if(self.obstacle_rect):
            self.obstacle_rect = self.obstacle_rect.move(position_offset)
    def collision_detected(self, field_object):
        return self.obstacle_rect.colliderect(field_object.obstacle_rect)
    def set_image(self, image_path):
        match_groups = re.match(r'^flip (.*)', image_path)
        if match_groups:
            self.image = pygame.image.load(match_groups.group(1))
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = pygame.image.load(image_path)
