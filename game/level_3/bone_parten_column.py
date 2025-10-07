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
        """Di chuyển ngang và tự xóa khi ra khỏi arena."""
        self.rect.x += self.speed * self.direction * dt * 60
        if self.rect.right < self.arena_rect.left - 50 or self.rect.left > self.arena_rect.right + 50:
            self.kill()


class BonePatternColumn:
    """Hai cột xương di chuyển ngược chiều nhau, mỗi cột có 2 xương dọc."""
    bone_delay = 0.6  # Thời gian giữa mỗi lần spawn

    def __init__(self, screen, box_rect, player):
        self.screen = screen
        self.box_rect = box_rect
        self.player = player

        # Load ảnh xương trên và dưới
        self.bone_top_img = pygame.image.load("graphics/Sprites/bones/bone_gap_upper2.png").convert_alpha()
        self.bone_bottom_img = pygame.image.load("graphics/Sprites/bones/bone_gap_below2.png").convert_alpha()

        self.bones = pygame.sprite.Group()

        # Mỗi cột có 2 xương dọc cách nhau
        self.column_y_offsets = [-65, 50]

        # Cấu hình 2 cột
        self.columns = [
            {"direction": 1, "timer": 0},   # Cột trái → phải
            {"direction": -1, "timer": 0}   # Cột phải → trái
        ]

        self.speed = 7  # tốc độ di chuyển

    def spawn_column(self, direction):
        """Sinh 1 cột xương (2 xương dọc) theo hướng cho sẵn."""
        if direction == 1:  # Trái → Phải
            x = self.box_rect.left - 30
        else:  # Phải → Trái
            x = self.box_rect.right + 30

        center_y = self.box_rect.centery

        # Xương trên: bone1, Xương dưới: bone2
        bone_top = Bone(self.bone_top_img, (x, center_y + self.column_y_offsets[0]), self.speed, direction, self.box_rect)
        bone_bottom = Bone(self.bone_bottom_img, (x, center_y + self.column_y_offsets[1]), self.speed, direction, self.box_rect)

        self.bones.add(bone_top, bone_bottom)

    def update(self, dt):
        """Cập nhật logic sinh và di chuyển xương."""
        for col in self.columns:
            col["timer"] += dt
            if col["timer"] >= self.bone_delay:
                self.spawn_column(col["direction"])
                col["timer"] = 0

        # Cập nhật vị trí và vẽ xương
        self.bones.update(dt)
        for bone in self.bones:
            if self.box_rect.colliderect(bone.rect):
                self.screen.blit(bone.image, bone.rect)

        # Kiểm tra va chạm với player
        player_mask = pygame.mask.from_surface(self.player.image)
        for bone in self.bones:
            offset = (bone.rect.x - self.player.rect.x, bone.rect.y - self.player.rect.y)
            if player_mask.overlap(bone.mask, offset):
                self.player.damaged(5)
                break

    def rect_box(self, rect):
        """Cập nhật lại vùng box khi thay đổi."""
        self.box_rect = rect
