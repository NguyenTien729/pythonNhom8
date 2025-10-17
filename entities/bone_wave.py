import math
from typing import Optional

import pygame
from entities.bone import Bone

class BoneWave(pygame.sprite.Sprite):
    normal_delay = 0.05

    def __init__(self, screen, box_rect, player, gap, speed: Optional[float] = 15, scale: Optional[float] = 1.1):
        super().__init__()
        self.screen = screen
        self.box_rect = box_rect
        self.player = player
        self.speed = speed

        self.image = pygame.image.load("graphics/sprites/bones/bone_wave.png").convert_alpha()


        self.max_height = self.image.get_height()
        self.min_height = 5
        self.rect = self.image.get_rect()

        self.wave_timer = 0.0
        self.scale = scale
        self.frequency = 6

        self.bones = pygame.sprite.Group()

        self.spawn_timer = 0
        self.period = 2.0

        self.gap = gap

    def spawn_bone(self, y, direction, image, speed, anchor):
        if direction == -1:
            x = self.box_rect.right + 20
        else:
            x = self.box_rect.left - 20
        bone = Bone(image, (x, y), speed, direction, self.box_rect)

        if anchor == 'top':
            bone.rect.top = y
        elif anchor == 'bottom':
            bone.rect.bottom = y

        self.bones.add(bone)

    def update(self, dt):
        self.spawn_timer += dt
        self.wave_timer += dt

        while self.spawn_timer >= self.normal_delay:
            self.spawn_timer -= self.normal_delay

            scale_factor = (math.sin(self.wave_timer * self.frequency) + 1) / 2
            opposite_scale_factor = 1 - scale_factor

            height_1 = self.max_height * scale_factor * self.scale
            if height_1 < self.min_height: height_1 = self.min_height
            image_1 = pygame.transform.smoothscale(self.image, (self.image.get_width(), int(height_1)))
            self.spawn_bone(self.box_rect.top, -1, image_1, self.speed, 'top')

            height_2 = self.max_height * opposite_scale_factor * self.scale
            if height_2 < self.min_height: height_2 = self.min_height
            image_2 = pygame.transform.smoothscale(self.image, (self.image.get_width(), int(height_2)))
            self.spawn_bone(self.box_rect.bottom, -1, image_2, self.speed, 'bottom')

        self.bones.update(dt)

        player_mask = pygame.mask.from_surface(self.player.image)
        for bone in self.bones:
            offset = (bone.rect.x - self.player.rect.x, bone.rect.y - self.player.rect.y)
            if player_mask.overlap(bone.mask, offset):
                self.player.damaged(5)
                break

    def reset(self):
        self.bones.empty()

    def rect_box(self, rect):
        self.box_rect = rect