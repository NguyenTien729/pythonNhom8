import pygame
import random


class Bone(pygame.sprite.Sprite):
    """Một xương di chuyển dọc trong arena."""
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

        # Nếu ra khỏi box, xóa xương để tránh quá tải
        if self.rect.top > self.arena_rect.bottom + 10 or self.rect.bottom < self.arena_rect.top - 10:
            self.kill()


class BonePatternMiddle:
    """3 cột xương chạy dọc (giữa lên, hai bên xuống)."""
    bone_delay = 0.4  # delay giữa các xương trong cùng 1 cột

    def __init__(self, screen, box_rect, players, floors):
        self.screen = screen
        self.box_rect = box_rect
        self.player = players
        self.floor = floors

        # Load sprite xương
        self.bone_image = pygame.image.load("graphics/Sprites/bones/spr_s_boneloop_0.png").convert_alpha()
        self.bone_mask = pygame.mask.from_surface(self.bone_image)

        # Nhóm sprite chứa tất cả xương
        self.bones = pygame.sprite.Group()

        # Vị trí x cho 3 cột
        self.spawn_x_positions = [500, 600, 700]

        # Hướng di chuyển tương ứng: ngoài ↓, giữa ↑, ngoài ↓
        self.directions = [1, -1, 1]

        # Bộ đếm thời gian riêng cho từng cột
        self.column_timers = [0, 0, 0]

        # Âm thanh spawn (tùy chọn)
        self.spawn_sound = pygame.mixer.Sound("sound/sans_battle/undertale-impact-slam.mp3")

        self.floor_image = "graphics/sprites/bones/floor1.png"
        self.has_spawned_floor = False
        self.floor_direction = "left"
        self.floor_timer = 0
        self.floor_delay = 0.4

    def spawn_bone(self, x, direction):
        """Sinh 1 xương tại cột cụ thể."""
        if direction == 1:  # đi xuống
            y = self.box_rect.top - 20
        else:  # đi lên
            y = self.box_rect.bottom + 20

        speed = 4
        bone = Bone(self.bone_image, (x, y), speed, direction, self.box_rect)
        self.bones.add(bone)
        # self.spawn_sound.play()

    def spawn_floor(self):
        self.floor.create_floor(1, 1, self.screen, (290, 400), self.floor_direction, speed=2.5, sprite_prefix=self.floor_image)

    def update(self, dt):
        """Cập nhật tất cả logic."""
        # Cập nhật timer cho từng cột và spawn xương
        for i in range(3):
            self.column_timers[i] += dt
            if self.column_timers[i] >= self.bone_delay:
                self.spawn_bone(self.spawn_x_positions[i], self.directions[i])
                self.column_timers[i] = 0

        # Cập nhật vị trí xương
        self.bones.update(dt)

        # Vẽ xương
        for bone in self.bones:
            if self.box_rect.colliderect(bone.rect):
                self.screen.blit(bone.image, bone.rect)

        #vẽ floor
        if not self.has_spawned_floor:
            self.floor_timer += dt
            if self.floor_timer >= self.floor_delay:
                self.spawn_floor()
                self.player.rect.centerx = 290
                self.player.rect.centery = 390
                self.player.is_on_ground = True
                self.has_spawned_floor = True

        # Kiểm tra va chạm pixel-perfect
        player_mask = pygame.mask.from_surface(self.player.image)
        for bone in self.bones:
            offset = (bone.rect.x - self.player.rect.x, bone.rect.y - self.player.rect.y)
            if player_mask.overlap(bone.mask, offset):
                self.player.damaged(5)
                break

    #reset nếu có gọi lại
    def reset(self):
        self.has_spawned_floor = False
        self.floor_timer = 0
        self.bones.empty()
        self.column_timers = [0, 0, 0]

    def rect_box(self, rect):
        """Cập nhật lại vùng box khi thay đổi."""
        self.box_rect = rect
