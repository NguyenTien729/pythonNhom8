import pygame
from entities.bone import Bone

class TripleBone:
    def __init__(self, screen, box_rect, player, speed = 30):
        self.screen = screen
        self.box_rect = box_rect
        self.player = player
        self.speed = speed

        self.image = pygame.image.load("graphics/sprites/bones/bone_wave_2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.bones = pygame.sprite.Group()

        self.row_timer = [0.35, 0]
        self.delay = 0.7
        self.count = 0


    def spawn_bone(self, y, direction, image, speed):
        if direction == -1:
            x = self.box_rect.right + speed
        else:
            x = self.box_rect.left - speed
        bone = Bone(image, (x, y), speed, direction, self.box_rect)
        self.bones.add(bone)

    def update(self, dt):
        for i in range(2):
            self.row_timer[i] += dt
            if self.row_timer[i] >= self.delay:
                if i == 0:
                    y = self.box_rect.top + self.rect.height / 2
                else:
                    y = self.box_rect.bottom - self.rect.height / 2

                self.spawn_bone(y, -1, self.image, self.speed)
                self.row_timer[i] = 0

        self.bones.update(dt)

        player_mask = pygame.mask.from_surface(self.player.image)
        for bone in self.bones:
            offset = (bone.rect.x - self.player.rect.x, bone.rect.y - self.player.rect.y)
            if player_mask.overlap(bone.mask, offset):
                self.player.damaged(5)
                break

    def reset(self):
        self.bones.empty()
        self.row_timer = [0, 0]

    def rect_box(self, rect):
        self.box_rect = rect