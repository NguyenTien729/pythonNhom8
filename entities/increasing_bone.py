import pygame
from entities.bone import Bone

class IncreasingBone:
    def __init__(self, screen, box_rect, player, speed = 15):
        self.screen = screen
        self.box_rect = box_rect
        self.player = player
        self.speed = speed

        self.image = pygame.image.load("graphics/sprites/bones/bone_wave.png").convert_alpha()
        self.bones = pygame.sprite.Group()

        self.timer = 0
        self.delay = 0.02
        self.current_scale = 0
        self.max_scale = 0.65
        self.scale_increase = 0.04

    def spawn_bone(self):
        height = int(self.image.get_height() * self.current_scale)

        scale_image = pygame.transform.smoothscale(self.image, (self.image.get_width() - 5, height))

        bone_top = Bone(scale_image, (self.box_rect.right + 20, self.box_rect.top), self.speed, -1, self.box_rect)
        bone_top.rect.top = self.box_rect.top
        bone_top.rect = bone_top.image.get_rect(center=bone_top.rect.center)
        self.bones.add(bone_top)

        bone_bottom = Bone(scale_image, (self.box_rect.right + 20, self.box_rect.bottom), self.speed, -1, self.box_rect)
        bone_bottom.rect.bottom = self.box_rect.bottom
        bone_bottom.image = pygame.transform.rotate(bone_bottom.image, 180)
        bone_bottom.rect = bone_bottom.image.get_rect(center=bone_bottom.rect.center)
        self.bones.add(bone_bottom)

        self.current_scale += self.scale_increase

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.delay and self.current_scale <= self.max_scale:
            self.timer = 0
            self.spawn_bone()

        self.bones.update(dt)

        player_mask = pygame.mask.from_surface(self.player.image)
        for bone in self.bones:
            offset = (bone.rect.x - self.player.rect.x, bone.rect.y - self.player.rect.y)
            if player_mask.overlap(bone.mask, offset):
                self.player.damaged(5)
                break

    def reset(self):
        self.bones.empty()
        self.timer = 0.0
        self.current_scale = 0.0

    def rect_box(self, rect):
        self.box_rect = rect
