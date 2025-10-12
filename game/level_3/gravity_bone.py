# Mọi thứ trong class GravityBone giữ nguyên, chỉ sửa hàm draw()

import random
from typing import Optional, List  # Thêm List
import pygame
from entities.bone_stab import BoneStab


class GravityBone(pygame.sprite.Sprite):
    # ... (toàn bộ code __init__ và các hàm khác của bạn giữ nguyên) ...
    def __init__(self, screen, strong_gravity, default_gravity, player, player_rect, box_rect, height: Optional[int] = 30,
                 duration: Optional[float] = 0.75, side: Optional[List[str]] = None):
        super().__init__()
        self.screen = screen
        self.strong_gravity = strong_gravity
        self.default_gravity = default_gravity
        self.player = player
        self.player_rect = player_rect
        self.box_rect = box_rect
        self.height = height

        self.slam_sound = pygame.mixer.Sound('sound/sans_battle/undertale-impact-slam.mp3')

        self.bone_stab = pygame.sprite.GroupSingle()

        if side is None:
            self.side_options = ['left', 'right', 'top', 'bottom']
        else:
            self.side_options = side

        self.current_side = random.choice(self.side_options)
        self.timer = 0
        self.duration = duration

        self.pull_start_time = 0.0
        self.attack_time = 0.175
        self.float_time = 0.6

        self.is_attack = False
        self.have_played = False
        # Dòng này không cần thiết vì nó được xử lý trong update rồi
        # self.player.gravity = self.strong_gravity

    def update(self, dt, on: Optional[bool] = True):
        # ... (code hàm update của bạn giữ nguyên) ...
        self.timer += dt

        if self.pull_start_time <= self.timer < self.attack_time:
            self.player.gravity = self.strong_gravity
            self.player.change_gravity_direction(self.current_side)
            self.player.hold_jump_force = 0
            is_colliding_wall = (self.current_side == 'bottom' and self.player.rect.bottom >= self.box_rect.bottom) or \
                                (self.current_side == 'top' and self.player.rect.top <= self.box_rect.top) or \
                                (self.current_side == 'left' and self.player.rect.left <= self.box_rect.left) or \
                                (self.current_side == 'right' and self.player.rect.right >= self.box_rect.right)

            if is_colliding_wall and not self.have_played:
                self.slam_sound.play()
                self.have_played = True

        elif self.attack_time <= self.timer < self.float_time and on:
            if not self.is_attack:
                self.is_attack = True
                self.player.gravity = self.default_gravity
                self.player.hold_jump_force = 2.15
                # Ở đây bạn có thể truyền self.screen, hoặc không vì BoneStab đã giữ nó rồi
                bone_stab = BoneStab(self.screen, self.box_rect, self.current_side, self.height, 250, self.player)
                self.bone_stab.add(bone_stab)

        elif self.float_time <= self.timer < self.duration and on:
            self.player.gravity = 0
            self.player.velocity.x = 0
            self.player.velocity.y = 0
            self.player.hold_jump_force = 0
        #
        # if self.timer >= self.duration:
        #     self.reset()

        # Ta cần phải update cả sprite bên trong group nữa
        self.bone_stab.update(dt)

    def draw(self):
        if self.bone_stab.sprite:
            self.bone_stab.sprite.draw()

    def rect_box(self, rect):
        self.box_rect = rect

    def reset(self):
        self.timer = 0
        if self.bone_stab.sprite:
            self.bone_stab.sprite.kill()
        self.is_attack = False
        self.current_side = random.choice(self.side_options)
        self.have_played = False

    def done(self):
        return self.timer >= self.duration

class MultiBoneStab:
    def __init__(self, reset = False):
        self.bone_stabs = pygame.sprite.Group()
        self.reset = reset


    def create_bone_stab(self, screen, strong_gravity, default_gravity, player, player_rect, box_rect, height,
                 duration: Optional[float] = 0.75, side: Optional[List[str]] = None):
        bone_stab = GravityBone(screen, strong_gravity, default_gravity, player, player_rect, box_rect, height, duration, side)
        self.bone_stabs.add(bone_stab)
        return bone_stab

    def update(self, dt, on: Optional[bool] = True):
        for bone_stab in self.bone_stabs:
            bone_stab.update(dt, on)

        if self.reset:
            remove = [bs for bs in self.bone_stabs if bs.timer > bs.duration]
            for bs in remove:
                bs.bone_stab.sprite.kill() if bs.bone_stab.sprite else None
                bs.kill()

    def done(self):
        if len(self.bone_stabs) == 0:
            return False
        return all(bs.timer >= bs.duration for bs in self.bone_stabs)

    def destroy_all(self):
        for bone_stab in self.bone_stabs:
            bone_stab.reset()
        self.bone_stabs.empty()

    def draw(self):
        for bone_stab in self.bone_stabs:
            bone_stab.draw()

    def rect_box(self, rect):
        for bone_stab in self.bone_stabs:
            bone_stab.rect_box(rect)