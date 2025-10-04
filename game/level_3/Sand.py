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
        self.player_rect = player_rect
        self.center = Vector2(self.player_rect.center)
        self.start_time = pygame.time.get_ticks()

        self.blasters = blasters
        self.floors = floors

        # self.idle = pygame.image.load('images/idle.png')
        # self.frames = [pygame.image.load("frame1"),
        #                pygame.image.load("frame2"),
        #               pygame.image.load("frame3")]

        # self.image = self.idle
        # self.rect = self.image.get_rect()

        self.blaster_floor = BlasterFloor(self.screen, self.player_rect, self.blasters, self.floors)

        self.blaster_circle = BlasterCircle((500, 380), self.blasters)

        self.blaster_random = RandomBlaster(self.center,  750, 250, 230, 530, self.blasters)

        self.attack_patterns = [self.blaster_floor, self.blaster_random, self.blaster_circle]
        self.index = 1
        self.mod = self.attack_patterns[self.index]
        self.change_mod = False
        self.is_win = False

        self.attack_time = 8
        self.swap_time = 0

    def attack_mod(self):
        self.floors.destroy_all()
        self.blasters.destroy_all()
        self.index = (self.index + 1) % len(self.attack_patterns)
        self.mod = self.attack_patterns[self.index]

    def update(self, dt: float):
        if self.is_win:
            return

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


