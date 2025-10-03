import math
import random

from pygame import Vector2

def fire_vector(pivot: Vector2, pos: Vector2) -> float:
    vector = pivot - pos
    angle = math.degrees(math.atan2(vector.x, -vector.y)) + 180

    while angle >= 180:
        angle -= 360
    while angle < -180:
        angle += 360

    return angle


class RandomBlaster:
    time_delay = 0.5

    def __init__(self, pivot: Vector2, x_right, x_left, y_top, y_bottom, blaster):
        self.pivot = pivot
        self.x_right = x_right
        self.x_left = x_left
        self.y_top = y_top
        self.y_bottom = y_bottom

        self.spawn_timer = 0

        self.blaster = blaster

    def spawn_blaster(self):

        x1 = random.randint(self.x_left, self.x_right)
        y1 = random.randint(self.y_top, self.y_bottom)
        if x1 < (self.x_right - self.x_left) / 2 + self.x_left:
            x2 = x1 - 500
        else:
            x2 = x1 + 500

        if y1 < (self.y_bottom - self.y_top) / 2 + self.y_top:
            y2 = y1 - 300
        else:
            y2 = y1 + 300
        
        start_angle = random.randint(-180, 180)
        
        vector = Vector2(x1, y1)
        angle = fire_vector(self.pivot ,vector)

        blaster = self.blaster.create_blaster(x2, y2, x1, y1, angle = angle, start_angle = start_angle)


    def update(self, dt: float):
        self.spawn_timer += dt

        if self.spawn_timer >= self.time_delay:
            self.spawn_blaster()
            self.spawn_timer -= self.time_delay

