import random

import pygame

from entities.bone_stab import BoneStab


class GravityBone:
    def __init__(self, screen, strong_gravity, default_gravity, player, player_rect, box_rect):
        self.screen = screen
        self.strong_gravity = strong_gravity
        self.default_gravity = default_gravity
        self.player = player
        self.player_rect = player_rect
        self.box_rect = box_rect

        self.bone_stab= pygame.sprite.GroupSingle()

        self.side = ['left', 'right', 'top', 'bottom']
        self.current_side = random.choice(self.side)
        self.timer = 0
        self.duration = 1.0

        self.pull_start_time = 0.0
        self.attack_time = 0.25
        self.float_time = 0.6

        self.is_attack = False

        self.player.gravity = self.strong_gravity

    def update(self, dt):
        self.timer += dt

        if self.pull_start_time <= self.timer <= self.attack_time:
            self.player.gravity = self.strong_gravity
            self.player.gravity_direction = self.current_side
            self.player.hold_jump_force = 0
        elif self.attack_time <= self.timer < self.float_time:
            if not self.is_attack:
                self.is_attack = True
                self.player.gravity = self.default_gravity
                self.player.hold_jump_force = 2.5
                bone_stab = BoneStab(self.screen, self.box_rect, self.current_side, 30, 250)
                self.bone_stab.add(bone_stab)
        elif self.float_time <= self.timer:
            self.player.gravity = 0
            self.player.velocity.x = 0
            self.player.velocity.y = 0
            self.player.hold_jump_force = 0

        if self.timer >= self.duration:
            self.timer = 0
            self.bone_stab.empty()
            self.is_attack = False
            self.current_side = random.choice(self.side)

            self.player.gravity = self.strong_gravity
            self.player.gravity_direction = self.current_side

    def rect_box(self, rect):
        self.box_rect = rect