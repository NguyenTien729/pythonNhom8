import pygame
import random
from pygame.math import Vector2

class Beam:
    def __init__(self, image: pygame.Surface):
        self.original_image = image
        self.image = image.copy()
        self.rect = self.image.get_rect()

        #Properties
        self.rotation = 0
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.y_scale = 1.0 #beam width
        self.alpha = 255

        self.pivot_x = 0.5
        self.pivot_y = 0.5

        self.center = pygame.Vector2(self.rect.center)

    def scale(self, x: float, y: float):
        self.scale_x = x
        self.scale_y = y
        self.update()

    def set_pivot(self, px: float, py: float):
        self.pivot_x = px
        self.pivot_y = py

    def update(self):
        #Scale
        width = int(self.original_image.get_width() * self.scale_x * self.y_scale)
        height = int(self.original_image.get_height() * self.scale_y)
        scaled_image = pygame.transform.scale(self.original_image, (width, height))

        #Rotate
        self.image = pygame.transform.rotate(scaled_image, -self.rotation)
        self.image.set_alpha(int(self.alpha))

class Projectile:
    def __init__(self, sprite_path: str, x: float, y: float):
        image = pygame.image.load(sprite_path + ".png").convert_alpha()
        self.sprite = Beam(image)

        #Position
        self.x = x
        self.y = y

        self.abs_x = x
        self.abs_y = y

        self.p_collision = False

        self.is_active = True

        self.layer = ""

    def move(self, dx: float, dy: float):
        self.x += dx
        self.y += dy
        self.abs_x += dx
        self.abs_y += dy

    def move_to(self, x: float, y: float):
        self.x = x
        self.y = y

    def move_to_absolute(self, x: float, y: float):
        self.abs_x = x
        self.abs_y = y

        self.x = x
        self.y = y

    def remove(self):
        self.is_active = False

    def animation(self, surf: pygame.Surface):
        if self.is_active:
            self.sprite.update()  # Tạo ra ảnh self.sprite.image đã được xoay

            # 1. Lấy ảnh đã xoay và vị trí mục tiêu của điểm pivot
            rotated_image = self.sprite.image
            target_pivot_pos = Vector2(self.abs_x, self.abs_y)

            # 2. Vector từ tâm của ảnh gốc tới điểm pivot của nó
            original_rect = self.sprite.original_image.get_rect()
            pivot_in_image = Vector2(self.sprite.pivot_x * original_rect.width,
                                     self.sprite.pivot_y * original_rect.height)
            image_center = Vector2(original_rect.center)
            pivot_offset_vector = pivot_in_image - image_center

            # 3. Xoay vector offset này cùng chiều và cùng góc với ảnh
            # Ảnh được xoay bởi -self.sprite.rotation, nên vector cũng phải xoay như vậy
            rotated_offset_vector = pivot_offset_vector.rotate(-self.sprite.rotation)

            # 4. Tìm vị trí tâm của ảnh đã xoay để điểm pivot khớp với vị trí mục tiêu
            rotated_image_center = target_pivot_pos

            # 5. Lấy hình chữ nhật cuối cùng và vẽ nó ra
            final_rect = rotated_image.get_rect(center=rotated_image_center)

            surf.blit(rotated_image, final_rect)


def create_projectile_abs(sprite_path: str, x: float, y: float):
    return Projectile(sprite_path, x, y)

class ScreenShaker:
    def __init__(self):
        self.timer = 0
        self.magnitude = 0

    def shake(self, duration, magnitude):
        self.magnitude = magnitude
        self.timer = duration

    def get_offset(self):
        if self.timer > 0:
            self.timer -= 1
            offset_x = random.randint(-self.magnitude, self.magnitude)
            offset_y = random.randint(-self.magnitude, self.magnitude)
            return offset_x, offset_y

        return 0, 0