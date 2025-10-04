import random
from typing import Optional

y2 = [305, 380, 455]

class BlasterFloor:
    blaster_delay = 1.5
    floor_delay = 0.5

    def __init__(self, screen, player_rect, blasters, floors, beam_alpha_speed: Optional[int] = 0.125):
        self.screen = screen
        self.player_rect = player_rect
        self.blaster = blasters
        self.blaster_is_left = True

        self.beam_alpha_speed = beam_alpha_speed

        self.blaster_timer = 0
        self.floor_timer = 0

        self.floor = floors
        self.floor_pos_1 = 340
        self.floor_pos_2 = 415

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
        floor_up = self.floor.create_floor(1, 1, self.screen, self.player_rect, (-50, self.floor_pos_1), "right", speed = 5, sprite_prefix = self.image)
        floor_down = self.floor.create_floor(1, 1, self.screen, self.player_rect, (1050, self.floor_pos_2), "left", speed = 5, sprite_prefix = self.image)


    def update(self, dt):
        self.blaster_timer += dt
        self.floor_timer += dt

        if self.blaster_timer >= self.blaster_delay:
            self.spawn_blaster()
            self.blaster_timer = 0.5

        if self.floor_timer >= self.floor_delay:
            self.spawn_floor()
            self.floor_timer = 0