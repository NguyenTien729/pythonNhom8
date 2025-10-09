import pygame

class Bone(pygame.sprite.Sprite):
    def __init__(self, image, start_pos, speed, direction, arena_rect):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=start_pos)
        self.speed = speed
        self.direction = direction  # 1 = xuống, -1 = lên
        self.arena_rect = arena_rect
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.rect.y += self.speed * self.direction * dt * 60
        if self.rect.top > 700 or self.rect.bottom < -100:
            self.kill()


class BonePatternSideway:
    bone_delay = 0.4

    def __init__(self, screen, box_rect, player):
        self.screen = screen
        self.box_rect = box_rect
        self.player = player

        self.bone_image = pygame.image.load("graphics/sprites/bones/bone_sideway_2.png").convert_alpha()

        self.bone_mask = pygame.mask.from_surface(self.bone_image)
        self.bones = pygame.sprite.Group()

        #vị trí spawn
        self.spawn_x_positions = [400,600]
        self.directions = [1, -1]
        self.column_timers = [0, 0]

        self.floor_spawned = False  

    def spawn_bone(self, x, direction):
        if direction == 1: 
            y = -10
        else: 
            y = 610
        speed = 10
        bone = Bone(self.bone_image, (x, y), speed, direction, self.box_rect)
        self.bones.add(bone)

    def update(self, dt):
        #update timer cho xương
        for i in range(2):
            self.column_timers[i] += dt
            if self.column_timers[i] >= self.bone_delay:
                self.spawn_bone(self.spawn_x_positions[i], self.directions[i])
                self.column_timers[i] = 0

        self.bones.update(dt)
        for bone in self.bones:
            self.screen.blit(bone.image, bone.rect)

        #hitbox
        player_mask = pygame.mask.from_surface(self.player.image)
        for bone in self.bones:
            offset = (bone.rect.x - self.player.rect.x, bone.rect.y - self.player.rect.y)
            if player_mask.overlap(bone.mask, offset):
                self.player.damaged(5)
                break

    def rect_box(self, rect):
        self.box_rect = rect
        self.floor_spawned = False 