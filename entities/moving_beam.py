import random

import pygame, math
from beams import *
from main import player_rect


class MovingBeam:
    def __init__(self, start_pos, end_pos, angle, config:Beam = Beam()):
        self.x, self.y = start_pos
        self.end_pos = end_pos
        self.angle = angle

        self.speed = config.speed
        self.delay = config.delay
        self.duration = config.duration
        self.width = config.width

        self.state = 0
        self.timer = 0
        self.active = True

        skull_small = pygame.image.load('char_python/skull.png')
        self.image = skull_small
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def draw(self, surf):
        if self.state == 0:
            surf.blit(self.image, self.rect)
        elif self.state == 1:
            end = (self.x + math.cos(math.radians(self.angle)) * 100,
                   self.y + math.sin(math.radians(self.angle)) * 100)
            pygame.draw.line(surf, 'yellow', (self.x, self.y), end, 4)
        elif self.state == 2:
            half = self.duration / 2.0
            if self.timer < half:
                fade = self.timer / half

            else:
                fade = 1 - (self.timer - half) / half
            alpha = max(0, min(255, int(fade * 255)))

            temp_surface = pygame.Surface(self.get_size(), pygame.SRCALPHA)

            end = (self.x + math.cos(math.radians(self.angle)) * 999,
                   self.y + math.sin(math.radians(self.angle)) * 999)
            pygame.draw.line(temp_surface, (255, 255, 255, alpha), (self.x, self.y), end, self.width)

            surf.blit(temp_surface, (0,0))

    def hit(self):
        if self.state != 2:
            return False
        player_x, player_y = player_rect.center
        vx, vy = math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle))
        dx, dy = player_x - self.x, player_y - self.y
        dist = abs(vx * dx + vy * dy)
        return dist <= self.width / 2

    def update(self):




