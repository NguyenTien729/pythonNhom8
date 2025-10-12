import pygame
from pygame import Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image_normal = pygame.image.load('graphics/sprites/player/heart.png').convert_alpha()
        self.image_gravity = pygame.image.load('graphics/sprites/player/heart_blue.png').convert_alpha()
        self.image_hit = pygame.image.load('graphics/Sprites/player/heart_hit1.png').convert_alpha()

        self.max_hp = 50
        self.player_hp = 50
        self.immunity_dur = 1000
        self.last_hit_time = 0
        self.is_invulnerable = False

        self.image = self.image_normal
        self.rect = self.image.get_rect(center = (x, y))
        self.center = Vector2(self.rect.center)

        self.speed = 5
        self.gravity = 1.25
        self.gravity_direction = 'bottom'
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.max_velocity = 18

        self.initial_jump = -5
        self.hold_jump_force = 2.15
        self.jump_time_max = 5
        self.jump_timer = 0

        self.is_gravity = False
        self.is_on_ground = False
        self.avatar_face_right = False

    def input(self):
        keys = pygame.key.get_pressed()

        if self.is_gravity:
            if self.gravity_direction in ['top', 'bottom']:
                if keys[pygame.K_LEFT]:
                    self.velocity.x = -self.speed
                elif keys[pygame.K_RIGHT]:
                    self.velocity.x = self.speed
                else:
                    self.velocity.x = 0

            elif self.gravity_direction in ['left', 'right']:
                if keys[pygame.K_LEFT]:
                    self.velocity.y = -self.speed
                elif keys[pygame.K_RIGHT]:
                    self.velocity.y = self.speed
                else:
                    self.velocity.y = 0

            if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.is_on_ground:
                self.jump()

        else:
            position = Vector2(0, 0)

            if keys[pygame.K_LEFT]:
                position.x -= 1
            if keys[pygame.K_RIGHT]:
                position.x += 1
            if keys[pygame.K_UP]:
                position.y -= 1
            if keys[pygame.K_DOWN]:
                position.y += 1

            if position.magnitude() != 0:
                position = position.normalize()

            self.velocity = position * self.speed

    def change_gravity_direction(self, direction: str):
        if self.gravity_direction != direction:
            self.gravity_direction = direction
            self.velocity = Vector2(0, 0)

    def apply_gravity(self):
        if self.is_gravity:
            if self.gravity_direction == 'bottom':
                self.velocity.y += self.gravity
            elif self.gravity_direction == 'top':
                self.velocity.y -= self.gravity
            elif self.gravity_direction == 'left':
                self.velocity.x -= self.gravity
            elif self.gravity_direction == 'right':
                self.velocity.x += self.gravity

            if self.gravity_direction == 'bottom':
                if self.velocity.y > self.max_velocity:
                    self.velocity.y = self.max_velocity
            elif self.gravity_direction == 'top':
                if self.velocity.y < -self.max_velocity:
                    self.velocity.y = -self.max_velocity
            elif self.gravity_direction == 'left':
                if self.velocity.x < -self.max_velocity:
                    self.velocity.x = -self.max_velocity
            elif self.gravity_direction == 'right':
                if self.velocity.x > self.max_velocity:
                    self.velocity.x = self.max_velocity


    def jump(self):
        if self.is_on_ground:
            if self.gravity_direction == 'bottom':
                self.velocity.y = self.initial_jump
            elif self.gravity_direction == 'top':
                self.velocity.y = -self.initial_jump
            elif self.gravity_direction == 'left':
                self.velocity.x = -self.initial_jump
            elif self.gravity_direction == 'right':
                self.velocity.x = self.initial_jump

            self.is_on_ground = False
            self.jump_timer = 0

    def set_gravity(self, on: bool):
        self.is_gravity = on

        if self.is_gravity:
            self.image = self.image_gravity
        else:
            self.image = self.image_normal
            self.velocity = Vector2(0, 0)
            self.change_gravity_direction('bottom')

    def damaged(self, amount):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time > self.immunity_dur:
            self.player_hp -= amount
            self.last_hit_time = current_time
            self.is_invulnerable = True

    def collision(self, floors):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        self.is_on_ground = False

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

        if self.is_on_ground:
            self.jump_timer = 0

    def update(self, floors, box_rect):
        self.input()

        if self.is_invulnerable and pygame.time.get_ticks() - self.last_hit_time > self.immunity_dur:
            self.is_invulnerable = False

        if self.is_gravity:
            self.apply_gravity()

        if self.velocity.x > 0:
            self.avatar_face_right = True
        elif self.velocity.x < 0:
            self.avatar_face_right = False

        keys = pygame.key.get_pressed()

        if self.is_gravity and self.jump_timer < self.jump_time_max:
            if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
                if self.gravity_direction == 'bottom':
                    self.velocity.y -= self.hold_jump_force
                elif self.gravity_direction == 'top':
                    self.velocity.y += self.hold_jump_force
                elif self.gravity_direction == 'left':
                    self.velocity.x += self.hold_jump_force
                elif self.gravity_direction == 'right':
                    self.velocity.x -= self.hold_jump_force
                self.jump_timer += 1

        self.collision(floors)

        if self.rect.bottom >= box_rect.bottom:
            self.rect.bottom = box_rect.bottom
            if self.is_gravity and self.gravity_direction == 'bottom':
                self.velocity.y = 0
                self.is_on_ground = True
                self.jump_timer = 0
        if self.rect.top <= box_rect.top:
            self.rect.top = box_rect.top
            if self.is_gravity and self.gravity_direction == 'top':
                self.velocity.y = 0
                self.is_on_ground = True
                self.jump_timer = 0
        if self.rect.right >= box_rect.right:
            self.rect.right = box_rect.right
            if self.is_gravity and self.gravity_direction == 'right':
                self.velocity.x = 0
                self.is_on_ground = True
                self.jump_timer = 0
        if self.rect.left <= box_rect.left:
            self.rect.left = box_rect.left
            if self.is_gravity and self.gravity_direction == 'left':
                self.velocity.x = 0
                self.is_on_ground = True
                self.jump_timer = 0

    def draw(self, surface):
        original_image = self.image_normal
        if self.is_gravity:
            original_image = self.image_gravity

        if self.is_invulnerable and (pygame.time.get_ticks() // 200) % 2 == 0:
            original_image = self.image_hit

        rotated_image = original_image
        if self.gravity_direction == 'top':
            rotated_image = pygame.transform.flip(original_image, False, True)
        elif self.gravity_direction == 'left':
            rotated_image = pygame.transform.rotate(original_image, -90)
        elif self.gravity_direction == 'right':
            rotated_image = pygame.transform.rotate(original_image, 90)

        if self.gravity_direction in ['top', 'bottom'] and not self.avatar_face_right:
            final_image = pygame.transform.flip(rotated_image, True, False)
        else:
            final_image = rotated_image

        surface.blit(final_image, self.rect)