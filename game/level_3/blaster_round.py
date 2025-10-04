import math

import pygame
from pygame import Vector2

def rotate_on_pivot(pivot, angle, origin):
    offset = pivot + (origin - pivot).rotate(-angle)

    return offset

def fire_vector(pivot: Vector2, pos: Vector2) -> float:
    vector = pivot - pos
    angle = math.degrees(math.atan2(vector.x, -vector.y)) + 180

    while angle >= 180:
        angle -= 360
    while angle < -180:
        angle += 360

    return angle

class BlasterCircle:
    fire_radius = 250
    spawn_radius = 700
    spawn_delay = 0.225

    def __init__(self, pivot, blaster, start_angle = 0, beam_alpha_speed = 7, beam_width = 0.7):
        self.pivot = pivot
        self.angle = -15

        spawn_offset = Vector2()
        spawn_offset.from_polar((self.spawn_radius, -start_angle - 30))

        fire_offset = Vector2()
        fire_offset.from_polar((self.fire_radius, -start_angle))

        self.pos_1 = pivot + spawn_offset
        self.pos_2 = pivot + fire_offset

        self.blaster = blaster
        self.spawn_timer = 0

        self.beam_alpha_speed = beam_alpha_speed
        self.beam_width = beam_width

        self.sound = pygame.mixer.Sound("sound/sans_battle/gaster_round_call.wav")
        self.fire_sound = pygame.mixer.Sound("sound/sans_battle/gaster_round_fire.wav")

    def spawn_blaster(self):
        spawn_pos = rotate_on_pivot(self.pivot, self.angle, self.pos_1)

        fire_pos = rotate_on_pivot(self.pivot, self.angle, self.pos_2)
        angle = fire_vector(self.pivot, fire_pos)

        blaster = self.blaster.create_blaster(spawn_pos.x, spawn_pos.y, fire_pos.x, fire_pos.y, angle = angle, start_angle = angle - 270,
                                              sound = self.sound ,fire_sound = self.fire_sound)

        blaster.beam_alpha_speed = self.beam_alpha_speed
        blaster.beam_width = self.beam_width

    def update(self, dt: float):
        self.angle += 180 * dt

        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_blaster()
            self.spawn_timer -= self.spawn_delay
