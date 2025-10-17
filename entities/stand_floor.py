from typing import Optional

import pygame

class CallFloor(pygame.sprite.Sprite):
    def __init__(self, height, width, screen, pos, direction: str, speed = 20, sprite_prefix: Optional[str] = None):
        super().__init__()

        self.screen = screen
        self.speed = speed

        self.sprite_prefix = sprite_prefix or "graphics/sprites/bones/floor2.png"
        self.sprite = pygame.image.load(self.sprite_prefix).convert_alpha()
        self.sprite = pygame.transform.scale_by(self.sprite,(width, height))
        self.image = self.sprite

        self.rect = self.sprite.get_rect(center = pos)
        self.old_rect = self.rect.copy()

        self.direction = direction

    def move(self, dt: float):

        if self.direction == "left":
            self.rect.x -= self.speed * dt
        elif self.direction == "right":
            self.rect.x += self.speed * dt
        elif self.direction == "up":
            self.rect.y -= self.speed * dt
        elif self.direction == "down":
            self.rect.y += self.speed * dt

    def change_direction(self, on: bool):
        if on:
            if self.direction == "right" and self.rect.right >= 740:
                self.rect.right = 740
                self.direction = "left"
            elif self.direction == "left" and self.rect.left <= 255:
                self.rect.left = 255
                self.direction = "right"

    def draw(self):
        self.screen.blit(self.sprite, self.rect)

    def destroy(self):
        if self.rect.right > 1100 or self.rect.left < -100:
            self.kill()

    def update(self, dt: float):
        self.old_rect = self.rect.copy()

        self.move(dt)
        self.draw()

class MultiFloor:
    def __init__(self):
        self.floors = pygame.sprite.Group()

    def create_floor(self, height, width, screen, pos, direction: str, speed = 500, sprite_prefix: Optional[str] = None):
        floor = CallFloor(height, width, screen, pos, direction, speed, sprite_prefix)
        self.floors.add(floor)
        return floor

    def update(self, dt: float, on: Optional[bool] = False):
        for floor in self.floors:
            floor.change_direction(on)

        self.floors.update(dt)

    def destroy_all(self):
        for floor in self.floors:
            floor.destroy()
        self.floors.empty()

    def draw(self, surface: pygame.Surface):
        self.floors.draw(surface)