from typing import Optional

import pygame

class CallFloor(pygame.sprite.Sprite):
    def __init__(self, height, width, screen ,player_rect, pos, direction: str, speed = 5, sprite_prefix: Optional[str] = None):
        super().__init__()

        self.screen = screen
        self.height = height
        self.width = width
        self.pos = pos
        self.speed = speed

        self.sprite_prefix = sprite_prefix or "graphics/sprites/bones/floor1.png"
        self.sprite = pygame.image.load(self.sprite_prefix).convert_alpha()
        self.sprite = pygame.transform.scale_by(self.sprite,(self.width,self.height))
        self.image = self.sprite

        self.rect = self.sprite.get_rect(center = pos)
        self.old_rect = self.rect.copy()
        self.player_rect = player_rect

        self.direction = direction

    def move(self):

        if self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed
        elif self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed

    def draw(self):
        self.screen.blit(self.sprite, self.rect)

    def destroy(self):
        if self.rect.right > 1100 or self.rect.left < -100:
            self.kill()


    def collision(self):

        if self.rect.colliderect(self.player_rect):
            over_lap_x = min(self.rect.right, self.player_rect.right) - max(self.rect.left, self.player_rect.left)
            over_lap_y = min(self.rect.bottom, self.player_rect.bottom) - max(self.rect.top, self.player_rect.top)

            if over_lap_x < over_lap_y:
                if self.rect.centerx > self.player_rect.centerx:
                    self.player_rect.right = self.rect.left
                else:
                    self.player_rect.left = self.rect.right
            else:
                if self.rect.centery > self.player_rect.centery:
                    self.player_rect.bottom = self.rect.top

                    offset_x = self.rect.x - self.old_rect.x
                    offset_y = self.rect.y - self.old_rect.y

                    self.player_rect.x += offset_x
                    self.player_rect.y += offset_y
                else:
                    self.player_rect.top = self.rect.bottom

            return self.player_rect
        return None

    def update(self):
        self.old_rect = self.rect.copy()

        self.move()
        self.collision()
        self.draw()

class MultiFloor:
    def __init__(self):
        self.floors = pygame.sprite.Group()

    def create_floor(self, height, width, screen ,player_rect, pos, direction: str, speed = 5, sprite_prefix: Optional[str] = None):
        floor = CallFloor(height, width, screen, player_rect, pos, direction, speed, sprite_prefix)
        self.floors.add(floor)
        return floor

    def update(self):
        self.floors.update()


    def destroy_all(self):
        for floor in self.floors:
            floor.destroy()
        self.floors.empty()

    def draw(self, surface: pygame.Surface):
        self.floors.draw(surface)

