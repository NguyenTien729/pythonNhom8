import random
from typing import Optional

import pygame

from entities.bone_stab import BoneStab


class GravityBone:
    def __init__(self, screen, strong_gravity, default_gravity, player, player_rect, box_rect, duration: Optional[float] = 0.75):
        self.screen = screen
        self.strong_gravity = strong_gravity
        self.default_gravity = default_gravity
        self.player = player
        self.player_rect = player_rect
        self.box_rect = box_rect

        self.slam_sound = pygame.mixer.Sound('sound/sans_battle/undertale-impact-slam.mp3')

        self.bone_stab= pygame.sprite.GroupSingle()

        self.side = ['left', 'right', 'top', 'bottom']
        self.current_side = random.choice(self.side)
        self.timer = 0
        self.duration = duration

        self.pull_start_time = 0.0
        self.attack_time = 0.175
        self.float_time = 0.6

        self.is_attack = False
        self.have_played = False
        self.player.gravity = self.strong_gravity

    def update(self, dt, on: Optional[bool] = True):
        self.timer += dt

        #hút mạnh khi mới vào đòn đánh
        if self.pull_start_time <= self.timer <= self.attack_time:
            self.player.gravity = self.strong_gravity
            self.player.gravity_direction = self.current_side
            self.player.hold_jump_force = 0
            if self.player.rect.bottom <= self.box_rect.bottom or self.player.rect.top >= self.box_rect.top or self.player.rect.left <= self.box_rect.left or self.player.rect.right >= self.box_rect.right:
                if not self.have_played:
                    self.slam_sound.play()
                    self.have_played = True
        #cho phép player nhảy né
        elif self.attack_time <= self.timer < self.float_time and on:
            if not self.is_attack:
                self.is_attack = True
                self.player.gravity = self.default_gravity
                self.player.hold_jump_force = 2.15
                bone_stab = BoneStab(self.screen, self.box_rect, self.current_side, 30, 250, self.player)
                self.bone_stab.add(bone_stab)
        elif self.float_time <= self.timer and on:
            self.player.gravity = 0
            self.player.velocity.x = 0
            self.player.velocity.y = 0
            self.player.hold_jump_force = 0

        #reset đòn
        if self.timer >= self.duration:
            self.timer = 0
            self.bone_stab.empty()
            self.is_attack = False
            self.current_side = random.choice(self.side)

            self.player.gravity = self.strong_gravity
            self.player.gravity_direction = self.current_side
            self.have_played = False

    def rect_box(self, rect):
        self.box_rect = rect