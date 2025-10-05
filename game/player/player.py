import pygame
from pygame import Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image_normal = pygame.image.load('graphics/sprites/player/heart.png').convert_alpha()
        self.image_gravity = pygame.image.load('graphics/sprites/player/heart_blue-export.png').convert_alpha()
        self.image_hit = pygame.image.load('graphics/Sprites/player/heart_hit1.png').convert_alpha()

        self.max_hp = 50
        self.player_hp = 50
        self.immunity_dur = 1000
        self.last_hit_time = 0
        self.is_invulnerable = False

        self.image = self.image_normal
        self.rect = self.image.get_rect(center = (x, y))
        self.center = Vector2(self.rect.center)

        self.speed = 7
        self.gravity = 1.1
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)

        self.initial_jump = -5
        self.hold_jump_force = 1.5
        self.jump_time_max = 9
        self.jump_timer = 0

        self.is_gravity = False
        self.is_on_ground = False

    def input(self):
        keys = pygame.key.get_pressed()
        position = Vector2(0, 0)

        if keys[pygame.K_LEFT]:
            position.x -= 1
        if keys[pygame.K_RIGHT]:
            position.x += 1

        if not self.is_gravity:
            if keys[pygame.K_UP]:
                position.y -= 1
            if keys[pygame.K_DOWN]:
                position.y += 1
        else:
            if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.is_on_ground:
                self.jump()

        if position.magnitude() != 0:
            position = position.normalize()

        self.rect.x += position.x * self.speed

        if not self.is_gravity:
            self.rect.y += position.y * self.speed

    def apply_gravity(self):
        if self.is_gravity:
            self.velocity.y += self.gravity
            self.rect.y += self.velocity.y

    def jump(self):
        if self.is_on_ground:
            self.velocity.y = self.initial_jump
            self.is_on_ground = False
            self.jump_timer = 0

    def set_gravity(self, on: bool):
        self.is_gravity = on

        if self.is_gravity:
            self.image = self.image_gravity
        else:
            self.image = self.image_normal

        if not self.is_gravity:
            self.velocity.y = 0

    def damaged(self, amount):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time > self.immunity_dur:
            self.player_hp -= amount
            self.last_hit_time = current_time

    def update(self, floors, box_rect):
        self.input()

        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time > self.immunity_dur:
            self.is_invulnerable = False
        else:
            self.is_invulnerable = True

        keys = pygame.key.get_pressed()

        if self.is_gravity and (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.jump_timer < self.jump_time_max:
            self.velocity.y -= self.hold_jump_force
            self.jump_timer += 1

        self.apply_gravity()

        self.is_on_ground = False
        if self.is_gravity:
            for floor in floors:
                if self.rect.colliderect(floor.rect):
                    over_lap_x = min(self.rect.right, floor.rect.right) - max(self.rect.left, floor.rect.left)
                    over_lap_y = min(self.rect.bottom, floor.rect.bottom) - max(self.rect.top, floor.rect.top)
                    if over_lap_x < over_lap_y:
                        if self.velocity.y >= 0:
                            if self.rect.centerx < floor.rect.centerx:
                                self.rect.right = floor.rect.left
                            else:
                                self.rect.left = floor.rect.right
                    else:
                        if self.velocity.y >= 0:
                            self.rect.bottom = floor.rect.top
                            self.velocity.y = 0
                            self.is_on_ground = True
                            self.jump_timer = 0
                            offset_x = floor.rect.x - floor.old_rect.x
                            self.rect.x += offset_x
                        elif self.velocity.y < 0:
                            self.rect.top = floor.rect.bottom
                            self.velocity.y = 0
        if self.rect.top <= box_rect.top:
            if self.is_gravity:
                self.velocity.y = 0

        if self.rect.bottom >= box_rect.bottom:
            if self.is_gravity:
                self.velocity.y = 0
                self.is_on_ground = True
                self.jump_timer = 0

    def draw(self, surface):
        if not self.is_invulnerable:
            current_image = self.image_gravity if self.is_gravity else self.image_normal
            surface.blit(current_image, self.rect)
        else:
            cur_time = pygame.time.get_ticks()
            if (cur_time - self.last_hit_time) < self.immunity_dur:
                if (cur_time // 200) % 2 == 0:
                 surface.blit(self.image_hit, self.rect)
                else:
                    current_image = self.image_gravity if self.is_gravity else self.image_normal
                    surface.blit(current_image, self.rect)



