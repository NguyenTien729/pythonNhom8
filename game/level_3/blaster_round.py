import math
from math import radians

import pygame
from pygame import Vector2

from entities.blaster import MultiBlaster

blasters = MultiBlaster()


def rotate_on_pivot(pivot, angle, origin):
    offset = pivot + (origin - pivot).rotate(-angle)

    return offset

def fire_vector(pivot: Vector2, pos: Vector2) -> float:
    vector = pivot - pos
    # Tính góc chuẩn rồi xoay -90° để chuyển từ East sang North
    angle = math.degrees(math.atan2(vector.x, -vector.y)) + 180

    # Chuẩn hóa về [-180, 180) như Blaster
    while angle >= 180:
        angle -= 360
    while angle < -180:
        angle += 360

    return angle

class BlasterCircle:
    fire_radius = 150
    spawn_radius = 700
    spawn_delay = 0.005

    def __init__(self, pivot, blaster, start_angle = 0, beam_alpha_speed = 0.6, beam_width = 0.7):
        self.pivot = pivot
        self.angle = 180

        # offset = Vector2()
        # offset.from_polar((self.spawn_radius, -start_angle - 30))

        offset_2 = Vector2()
        offset_2.from_polar((self.fire_radius, -start_angle))

        # self.pos_1 = pivot + offset
        self.pos_2 = pivot + offset_2

        self.blaster = blaster
        self.spawn_timer = 0

        self.beam_alpha_speed = beam_alpha_speed
        self.beam_width = beam_width


    def spawn_blaster(self):
        # spawn_pos = rotate_on_pivot(self.pivot, self.angle, self.pos_1)

        fire_pos = rotate_on_pivot(self.pivot, self.angle, self.pos_2)
        angle = fire_vector(self.pivot, fire_pos)
        print(fire_pos)
        print(angle)
        blaster = self.blaster.create_blaster(-100, -100, fire_pos.x, fire_pos.y, angle = angle, start_angle = angle - 30)

        blaster.beam_alpha_speed = self.beam_alpha_speed
        blaster.beam_width = self.beam_width

    def update(self, dt: float):
        self.angle += 120 * dt * 20

        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_blaster()
            self.spawn_timer -= self.spawn_delay