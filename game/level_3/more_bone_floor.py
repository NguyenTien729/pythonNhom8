import pygame
from entities.bone import Bone

class MoreBoneFloor(pygame.sprite.Sprite):
    floor_delay = 1
    def __init__(self, screen, box_rect, players, floors):
        super().__init__()
        self.screen = screen
        self.box_rect = box_rect
        self.player = players

        self.bone_images = [
            pygame.image.load("graphics/sprites/bones/spr_s_boneloop_in_0.png").convert_alpha(),
            pygame.image.load("graphics/sprites/bones/spr_s_boneloop_out_0.png").convert_alpha(),
            pygame.image.load("graphics/sprites/bones/spr_s_bonewall_0.png").convert_alpha(),
        ]

        self.bones = pygame.sprite.Group()

        self.floor = floors

        self.floor_1 = "graphics/sprites/bones/floor4.png"
        self.floor_2 = "graphics/sprites/bones/floor3.png"

        self.floor_pos_1 = 360
        self.floor_pos_2 = 415

        self.floor_timer = 0

        self.spawn_y_positions = [330, 380, 450]

        #hướng
        self.directions = [-1, 1, -1]

        self.normal_delay = 1
        # khoảng trống sau mỗi 2 xương
        self.gap_delay = 0.4
        self.column_timers = [0, 0, 0]
        self.pair_count = [0, 0, 0]

    def spawn_bone(self, y, direction, image, speed):
        if direction == -1:
            x = self.box_rect.right + 20
        else:
            x = self.box_rect.left - 20
        bone = Bone(image, (x, y), speed, direction, self.box_rect)
        self.bones.add(bone)

    def spawn_floor(self):
        floor_left = self.floor.create_floor(1, 1, self.screen, (200, self.floor_pos_1), "right", speed=5, sprite_prefix=self.floor_1)
        floor_right = self.floor.create_floor(1, 1, self.screen, (800, self.floor_pos_2), "left", speed=5, sprite_prefix=self.floor_2)

    def update(self, dt):
        self.floor_timer += dt
        self.screen.set_clip(self.box_rect)

        if self.floor_timer >= self.floor_delay:
            self.spawn_floor()
            self.floor_timer = 0

        for i in range (3):
            self.column_timers[i] += dt

            if i == 1:
                if self.column_timers[i] > self.normal_delay:
                    self.spawn_bone(self.spawn_y_positions[i], self.directions[i], self.bone_images[i], 1.3)
                    self.column_timers[i] = 0

            else:
                speed = (2 if i == 0 else 1.56)
                delay = self.normal_delay if self.pair_count[i] < 2 else self.gap_delay
                if self.column_timers[i] >= delay:
                    self.spawn_bone(self.spawn_y_positions[i], self.directions[i], self.bone_images[i], speed)
                    self.pair_count[i] += 1
                    self.column_timers[i] = 0

                    if self.pair_count[i] >= 1 and delay == self.normal_delay:
                        self.pair_count[i] = 2
                    elif self.pair_count[i] >= 2:
                        self.pair_count[i] = 0

            self.bones.update(dt)
            for bone in self.bones:
                if self.box_rect.colliderect(bone.rect):
                    self.screen.blit(bone.image, bone.rect)

        player_mask = pygame.mask.from_surface(self.player.image)
        for bone in self.bones:
            offset = (bone.rect.x - self.player.rect.x, bone.rect.y - self.player.rect.y)
            if player_mask.overlap(bone.mask, offset):
                self.player.damaged(5)

        self.screen.set_clip(None)

    def reset(self):
        self.floor_timer = 0
        self.bones.empty()
        self.column_timers = [0, 0, 0]

    def rect_box(self, rect):
        self.box_rect = rect

class MovingFloorBone(pygame.sprite.Sprite):
    def __init__(self, image, start_pos, speed, box_rect, group):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(midtop=start_pos)
        self.speed = speed
        self.box_rect = box_rect
        self.mask = pygame.mask.from_surface(self.image)

        self.y = start_pos[1]
        self.group = group
        self.bone_width = image.get_width()

    def update(self, dt):
        #speed floor bone
        self.rect.x += self.speed * dt * 60
        self.rect.centery = self.y

        # Nếu bone ra ngoài hoàn toàn
        if self.rect.left >= self.box_rect.right + 50:
            # tìm bone ngoài cùng bên trái
            leftmost = min(self.group, key=lambda b: b.rect.left)
            # đặt bone này ngay sau bone bên trái (liền mạch)
            self.rect.left = leftmost.rect.left - self.bone_width - 8