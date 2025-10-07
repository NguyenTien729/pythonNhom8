import pygame
import random


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
        if self.rect.top > self.arena_rect.bottom + 10 or self.rect.bottom < self.arena_rect.top - 10:
            self.kill()


class BonePatternMiddle:
    bone_delay = 0.4  

    def __init__(self, screen, box_rect, player):
        self.screen = screen
        self.box_rect = box_rect
        self.player = player

        self.bone_image = pygame.image.load("graphics/Sprites/bones/bone.png").convert_alpha()
        self.bone_mask = pygame.mask.from_surface(self.bone_image)
        self.bones = pygame.sprite.Group()
        #bonefloor
        self.floor_bones = pygame.sprite.Group()
        self.floor_image = pygame.image.load("graphics/Sprites/bones/bone_floor.png").convert_alpha()

        #vị trí spawn
        self.spawn_x_positions = [400, 500, 600]
        self.directions = [1, -1, 1]
        self.column_timers = [0, 0, 0]

        self.floor_spawned = False  

    def spawn_bone(self, x, direction):
        if direction == 1: 
            y = self.box_rect.top - 20
        else: 
            y = self.box_rect.bottom + 20
        speed = 4
        bone = Bone(self.bone_image, (x, y), speed, direction, self.box_rect)
        self.bones.add(bone)


    def spawn_floor_bones(self):
        if self.floor_spawned:
            return  
        floor_rect = self.floor_image.get_rect()
        floor_rect.midtop = (self.box_rect.centerx, self.box_rect.bottom-35)  
        floor = pygame.sprite.Sprite()
        floor.image = self.floor_image
        floor.rect = floor_rect
        floor.mask = pygame.mask.from_surface(self.floor_image)
        self.floor_bones.add(floor)
        self.floor_spawned = True

    def update(self, dt):
        #bone floor
        self.spawn_floor_bones()
        #update timer cho xương
        for i in range(3):
            self.column_timers[i] += dt
            if self.column_timers[i] >= self.bone_delay:
                self.spawn_bone(self.spawn_x_positions[i], self.directions[i])
                self.column_timers[i] = 0
        self.bones.update(dt)
        for bone in self.bones:
            if self.box_rect.colliderect(bone.rect):
                self.screen.blit(bone.image, bone.rect)

        for floor in self.floor_bones:
            self.screen.blit(floor.image, floor.rect)
        #hitbox
        player_mask = pygame.mask.from_surface(self.player.image)
        for bone in self.bones:
            offset = (bone.rect.x - self.player.rect.x, bone.rect.y - self.player.rect.y)
            if player_mask.overlap(bone.mask, offset):
                self.player.damaged(5)
                break
        for floor in self.floor_bones:
            offset = (floor.rect.x - self.player.rect.x, floor.rect.y - self.player.rect.y)
            if player_mask.overlap(floor.mask, offset):
                self.player.damaged(5)
                break

    def rect_box(self, rect):
        self.box_rect = rect
        self.floor_spawned = False 
