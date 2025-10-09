import pygame

class Bone(pygame.sprite.Sprite):
    def __init__(self, image, start_pos, speed, direction, arena_rect):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=start_pos)
        self.speed = speed
        self.direction = direction  # 1 = phải, -1 = trái
        self.arena_rect = arena_rect
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.rect.x += self.speed * self.direction * dt * 60
        if self.rect.right < self.arena_rect.left - 50 or self.rect.left > self.arena_rect.right + 50:
            self.kill()