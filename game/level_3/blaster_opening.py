import math
from pygame import Vector2
from typing import Optional



class BlasterOpen:
    time_delay = 0.7

    def __init__(self, pivot: Vector2, x_right, x_left, y_top, y_bottom, blaster,beam_alpha_speed: Optional[int] = 0.125):
        self.pivot = pivot
        self.x_right = x_right
        self.x_left = x_left
        self.y_top = y_top
        self.y_bottom = y_bottom
        self.beam_alpha_speed = beam_alpha_speed

        self.spawn_timer = 0
        self.round = 1  # lượt bắn hiện tại (1, 2, 3)
        self.blaster = blaster

    def spawn_pattern_plus(self):
        #+
        blaster = self.blaster.create_blaster(1000, 250, 700, 380, 90, start_angle=45)
        blaster = self.blaster.create_blaster(500, -100, 500, 200,  0, start_angle=45)
        blaster.beam_alpha_speed = self.beam_alpha_speed

    def spawn_pattern_x(self):
        #x
        blaster = self.blaster.create_blaster(1000, -100, 633, 250, 45, start_angle=0)
        blaster = self.blaster.create_blaster(0, -100, 366, 250, -45, start_angle=0)
        blaster.beam_alpha_speed = self.beam_alpha_speed

    def spawn_pattern_down(self):
        #||
        blaster = self.blaster.create_blaster(800, 600, 460, 530, 180, start_angle=90)
        blaster = self.blaster.create_blaster(200, 600, 540, 530, 180, start_angle=90)
        blaster.beam_alpha_speed = self.beam_alpha_speed

    def spawn_blaster(self):
        """Gọi lượt bắn tương ứng"""
        if self.round == 1:
            self.spawn_pattern_plus()
        elif self.round == 2:
            self.spawn_pattern_x()
        elif self.round == 3:
            self.spawn_pattern_down()

        # sang lượt tiếp theo
        self.round += 1
        if self.round > 3:
            self.round = 1  # nếu muốn lặp lại 3 lượt thì giữ dòng này
            # nếu muốn chỉ bắn 3 lượt rồi dừng, thì có thể bỏ dòng này

    def update(self, dt: float):
        self.spawn_timer += dt

        if self.spawn_timer >= self.time_delay:
            self.spawn_blaster()
            self.spawn_timer -= self.time_delay
