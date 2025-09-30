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

    def get_pivot_offset(self):
        # Pivot trong image space (trước khi rotate)
        pivot_x = self.rect.width * self.pivot_x
        pivot_y = self.rect.height * self.pivot_y

        # Offset từ center của image gốc đến pivot
        offset = Vector2(
            pivot_x - self.rect.width / 2,
            pivot_y - self.rect.height / 2
        )
        return offset

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
            self.sprite.update()

            # Pivot trong image CHƯA rotate (image gốc)
            original_width = self.sprite.original_image.get_width() * self.sprite.scale_x * self.sprite.y_scale
            original_height = self.sprite.original_image.get_height() * self.sprite.scale_y

            pivot_x = original_width * self.sprite.pivot_x
            pivot_y = original_height * self.sprite.pivot_y

            # Center của image gốc
            center_x = original_width / 2
            center_y = original_height / 2

            # Offset từ center đến pivot (TRONG image space gốc)
            offset = Vector2(pivot_x - center_x, pivot_y - center_y)

            # Rotate offset vector CÙNG góc với image
            rotated_offset = offset.rotate(self.sprite.rotation)

            # World position của center = pivot world position - rotated offset
            if self.abs_x <= 400:
                rotated_image_center = Vector2(self.abs_x, self.abs_y) + rotated_offset
            else:
                rotated_image_center = Vector2(self.abs_x, self.abs_y) - rotated_offset

            # Blit
            final_rect = self.sprite.image.get_rect(center=rotated_image_center)
            surf.blit(self.sprite.image, final_rect)

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