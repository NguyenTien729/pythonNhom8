import pygame
from entities.utils import resource_path

class Bone(pygame.sprite.Sprite):
    def __init__(self, image, start_pos, speed, direction, arena_rect):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=start_pos)
        self.speed = speed
        self.direction = direction  # 1 = phải, -1 = trái
        self.arena_rect = arena_rect
        self.mask = pygame.mask.from_surface(self.image)
    # Xóa khi ngoài khung cho đỡ lag
    def update(self, dt):
        self.rect.x += self.speed * self.direction * dt * 60
        if self.rect.right < self.arena_rect.left - 50 or self.rect.left > self.arena_rect.right + 50:
            self.kill()


class BonePatternColumn:
    bone_delay = 1.2  # Delay giữa spawn

    def __init__(self, screen, box_rect, player):
        self.screen = screen
        self.box_rect = box_rect
        self.player = player

        #image
        self.bone_top_img = pygame.image.load(resource_path("graphics/Sprites/bones/bone_gap_below2.png")).convert_alpha()
        self.bone_bottom_img = pygame.image.load(resource_path("graphics/Sprites/bones/bone_gap_upper2.png")).convert_alpha()
        self.bones = pygame.sprite.Group()

        # Vị trí sinh so vs y=0 của arena
        self.column_y_offsets = [-50, 65]
        self.columns = [
            {"direction": 1, "timer": 0},   # Trái phải
            {"direction": -1, "timer": 0}   # Phải trái
        ]

        self.speed = 3.5  # tốc độ di chuyển

    def spawn_column(self, direction):
        if direction == 1:  
            x = self.box_rect.left - 30
        else:  
            x = self.box_rect.right + 30

        center_y = self.box_rect.centery
        bone_top = Bone(self.bone_top_img, (x, center_y + self.column_y_offsets[0]), self.speed, direction, self.box_rect)
        bone_bottom = Bone(self.bone_bottom_img, (x, center_y + self.column_y_offsets[1]), self.speed, direction, self.box_rect)

        self.bones.add(bone_top, bone_bottom)

    def update(self, dt):
        for col in self.columns:
            col["timer"] += dt
            if col["timer"] >= self.bone_delay:
                self.spawn_column(col["direction"])
                col["timer"] = 0

        # Chỉ vẽ khi vào box
        self.bones.update(dt)
        for bone in self.bones:
            if self.box_rect.colliderect(bone.rect):
                self.screen.blit(bone.image, bone.rect)

        # hitbox
        player_mask = pygame.mask.from_surface(self.player.image)
        for bone in self.bones:
            offset = (bone.rect.x - self.player.rect.x, bone.rect.y - self.player.rect.y)
            if player_mask.overlap(bone.mask, offset):
                self.player.damaged(5)
                break
    # Cập nhật arena nếu đổi
    def rect_box(self, rect):
        self.box_rect = rect
