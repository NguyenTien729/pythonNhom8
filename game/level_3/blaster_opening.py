import math
from pygame import Vector2
from typing import Optional



class BlasterOpen:
    time_delay = 0.9

    def __init__(self, pivot: Vector2, blaster,beam_alpha_speed: Optional[int] = 0.125):
        self.pivot = pivot
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
    
    def spawn_pattern_left(self):
        #--
        blaster = self.blaster.create_blaster(0, 250, 300, 350, -90, start_angle=-45)
        blaster = self.blaster.create_blaster(0, 250, 300, 405, -90, start_angle=-45)
        blaster = self.blaster.create_blaster(0, 250, 300, 460, -90, start_angle=-45)
        blaster.beam_alpha_speed = self.beam_alpha_speed

    def spawn_pattern_right(self):
        #--
        blaster = self.blaster.create_blaster(1000, 250, 700, 310, 90, start_angle=45)
        blaster = self.blaster.create_blaster(1000, 250, 700, 365, 90, start_angle=45)
        blaster = self.blaster.create_blaster(1000, 250, 700, 420, 90, start_angle=45)
        blaster.beam_alpha_speed = self.beam_alpha_speed

    def spawn_pattern_final(self):
        #--
        blaster = self.blaster.create_blaster(1000, 250, 700, 320, 90, start_angle=0)        
        blaster = self.blaster.create_blaster(0, 250, 300, 450, -90, start_angle=0)
        blaster = self.blaster.create_blaster(500, -100, 440, 200,  0, start_angle=90)
        blaster = self.blaster.create_blaster(500, 600, 560, 560,  180, start_angle=90)

        blaster.beam_alpha_speed = self.beam_alpha_speed


    def spawn_blaster(self):
        """Gọi lượt bắn tương ứng"""
        if self.round == 1:
            self.spawn_pattern_plus()
        elif self.round == 2:
            self.spawn_pattern_x()
        elif self.round == 3:
            self.spawn_pattern_down()
        elif self.round == 4:
            self.spawn_pattern_right()
        elif self.round == 5:
            self.spawn_pattern_left()
        elif self.round == 6:
            self.spawn_pattern_final()

        # sang lượt tiếp theo
        self.round += 1
        # if self.round > 3:
        #     self.round = 1  # nếu muốn lặp lại 3 lượt thì giữ dòng này
            # nếu muốn chỉ bắn 3 lượt rồi dừng, thì có thể bỏ dòng này

    def update(self, dt: float):
        self.spawn_timer += dt

        if self.spawn_timer >= self.time_delay:
            self.spawn_blaster()
            self.spawn_timer -= self.time_delay
