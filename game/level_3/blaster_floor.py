import random
from typing import Optional
from entities.utils import resource_path

y2 = [325, 390, 460]

class BlasterFloor:
    blaster_delay = 3
    floor_delay = 1

    def __init__(self, screen, player_rect, blasters, floors, beam_alpha_speed: Optional[int] = 0.125):
        self.screen = screen
        self.player_rect = player_rect
        self.blaster = blasters
        self.blaster_is_left = True

        self.beam_alpha_speed = beam_alpha_speed

        self.blaster_timer = 0
        self.floor_timer = 0

        self.floor = floors
        self.floor_pos_1 = 360
        self.floor_pos_2 = 425

        self.image = "graphics/sprites/bones/floor2.png"


    def spawn_blaster(self):
        if self.blaster_is_left:
            x = -100
            x2 = 250
            angle = -90
            self.blaster_is_left = False
        else:
            x = 1100
            x2 = 750
            angle = 90
            self.blaster_is_left = True


        blaster = self.blaster.create_blaster(x, -100, x2, random.choice(y2), angle = angle, start_angle = 60)

        blaster.beam_alpha_speed = self.beam_alpha_speed

    def spawn_floor(self):
        floor_left = self.floor.create_floor(1, 1, self.screen, (-50, self.floor_pos_1), "right", speed=150, sprite_prefix=self.image)
        floor_right = self.floor.create_floor(1, 1, self.screen, (1050, self.floor_pos_2), "left", speed = 150, sprite_prefix = self.image)


    def update(self, dt):
        self.blaster_timer += dt
        self.floor_timer += dt

        if self.blaster_timer >= self.blaster_delay:
            self.spawn_blaster()
            self.blaster_timer = 1

        if self.floor_timer >= self.floor_delay:
            self.spawn_floor()
            self.floor_timer = 0