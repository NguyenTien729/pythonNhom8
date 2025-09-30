import pygame
import random

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
            self.sprite.update()

            # Calculate position based on pivot
            rect = self.sprite.image.get_rect()
            rect.x = int(self.abs_x - (rect.width * self.sprite.pivot_x))
            rect.y = int(self.abs_y - (rect.height * self.sprite.pivot_y))

            surf.blit(self.sprite.image, rect)

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