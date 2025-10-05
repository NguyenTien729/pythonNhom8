import math

from pygame import Vector2

from entities.blaster import MultiBlaster
from entities.stand_floor import MultiFloor
from game.level_3.random_blaster import RandomBlaster
from game.level_3.blaster_round import BlasterCircle
from game.level_3.blaster_floor import BlasterFloor

import pygame


class CallBoss(pygame.sprite.Sprite):
    phase_time = 8
    change_phase_time = 2

    def __init__(self, screen, player_rect, blasters: MultiBlaster, floors: MultiFloor):
        super().__init__()
        self.screen = screen
        self.box_rect = pygame.Rect(0, 0, 0, 0)
        self.box_center = Vector2(self.box_rect.center)
        self.player_rect = player_rect
        self.center = Vector2(self.player_rect.center)
        self.start_time = pygame.time.get_ticks()

        self.blasters = blasters
        self.floors = floors

        self.beam_width = 1

        self.legs_idle = pygame.image.load('graphics/characters/sans/spr_sansb_legs_0.png')
        self.legs_idle = pygame.transform.scale_by(self.legs_idle, 2.5)
        self.body_idle = pygame.image.load('graphics/characters/sans/spr_sansb_torso_0.png')
        self.body_idle = pygame.transform.scale_by(self.body_idle, 2.5)
        self.face_idle = pygame.image.load('graphics/characters/sans/spr_sansb_face_0.png')
        self.face_idle = pygame.transform.scale_by(self.face_idle, 2.5)

        self.hand_down_frames = [pygame.image.load('graphics/characters/sans/spr_sansb_handdown_0.png'),
                                 pygame.image.load('graphics/characters/sans/spr_sansb_handdown_1.png'),
                                 pygame.image.load('graphics/characters/sans/spr_sansb_handdown_2.png'),
                                 pygame.image.load('graphics/characters/sans/spr_sansb_handdown_3.png'),
                                 pygame.image.load('graphics/characters/sans/spr_sansb_handdown_4.png'),]

        self.hand_right_frames = [pygame.image.load('graphics/characters/sans/spr_sansb_rightstrike_0.png'),
                                  pygame.image.load('graphics/characters/sans/spr_sansb_rightstrike_1.png'),
                                  pygame.image.load('graphics/characters/sans/spr_sansb_rightstrike_2.png'),
                                  pygame.image.load('graphics/characters/sans/spr_sansb_rightstrike_3.png'),
                                  pygame.image.load('graphics/characters/sans/spr_sansb_rightstrike_4.png')]

        self.leg_rect = self.legs_idle.get_rect()
        self.body_rect = self.body_idle.get_rect()
        self.face_rect = self.face_idle.get_rect()

        self.wiggle_time = 0.0
        self.wiggle_amplitude_head = 1.2
        self.wiggle_amplitude_body = 1.5
        self.wiggle_speed_x = 8
        self.wiggle_speed_y = 16
        self.body_x = 0
        self.face_x = 0
        self.body_y = 0
        self.face_y = 0


        self.blaster_floor = BlasterFloor(self.screen, self.player_rect, self.blasters, self.floors, 2)

        self.blaster_circle = BlasterCircle((500, 380), self.blasters, beam_width = self.beam_width)

        self.blaster_random = RandomBlaster(self.center,  750, 250, 230, 530, self.blasters)

        self.attack_patterns = [self.blaster_floor, self.blaster_random, self.blaster_circle]
        self.index = -1
        self.mod = self.attack_patterns[self.index]
        self.change_mod = False
        self.is_win = False

        self.attack_time = 8
        self.swap_time = 0

    def wiggle_animation(self, dt: float):
        self.wiggle_time += dt

        offset_x = math.sin(self.wiggle_time * self.wiggle_speed_x)
        offset_y = math.cos(self.wiggle_time * self.wiggle_speed_y)

        self.body_rect.centerx = int(self.body_x + offset_x * self.wiggle_amplitude_body)
        self.face_rect.centerx = int(self.face_x + offset_x * self.wiggle_amplitude_head)

        self.body_rect.centery = int(self.body_y + offset_y * self.wiggle_amplitude_body)
        self.face_rect.centery = int(self.face_y + offset_y * self.wiggle_amplitude_head)

    def attack_mod(self):
        self.floors.destroy_all()
        self.blasters.destroy_all()
        self.index = (self.index + 1) % len(self.attack_patterns)
        self.mod = self.attack_patterns[self.index]

    def animation(self):
        self.leg_rect = self.legs_idle.get_rect(midbottom = (self.box_rect.midtop[0], self.box_rect.midtop[1] - 20))
        self.body_rect = self.body_idle.get_rect(midbottom = (self.leg_rect.midtop[0], self.leg_rect.midtop[1] + 25))
        self.face_rect = self.face_idle.get_rect(midbottom = (self.body_rect.midtop[0], self.body_rect.midtop[1] + 20))

        self.body_x = self.body_rect.centerx
        self.face_x = self.face_rect.centerx

        self.body_y = self.body_rect.centery
        self.face_y = self.face_rect.centery

    def draw(self):
        self.screen.blit(self.legs_idle, self.leg_rect)
        self.screen.blit(self.body_idle, self.body_rect)
        self.screen.blit(self.face_idle, self.face_rect)

    def update(self, dt: float, box_rect: pygame.Rect, player):
        if self.is_win:
            return

        if self.index == 0:
            player.set_gravity(True)
        else:
            player.set_gravity(False)

        self.box_rect = box_rect
        self.center = Vector2(self.box_rect.center)

        self.animation()
        self.wiggle_animation(dt)
        self.draw()

        self.blaster_random.pivot = Vector2(self.player_rect.center)

        if self.change_mod:
            self.swap_time += dt
            if self.swap_time >= self.change_phase_time:
                self.swap_time = 0
                self.change_mod = False
                self.attack_mod()
        else:
            self.mod.update(dt)

            self.attack_time += dt
            if self.attack_time >= self.phase_time:
                self.attack_time = 0
                self.change_mod = True


        self.floors.update()
        self.floors.draw(self.screen)

        self.blasters.update()
        self.blasters.draw(self.screen)


    def arena_state(self):
        #floor
        if self.index == -1:
            final_box_width = 400
            final_box_height = 200
        #random
        elif self.index == 1:
            final_box_width = 400
            final_box_height = 200
        #circle
        elif self.index == 2:
            final_box_width = 200
            final_box_height = 200
        else:
            final_box_width = 400
            final_box_height = 200
        return final_box_width, final_box_height