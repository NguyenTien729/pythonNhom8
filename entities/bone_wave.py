import pygame

class BoneWave:
    def __init__(self, screen_width, screen_height, arena_rect):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.arena_rect = arena_rect

        # Load ảnh xương
        self.bone_img = pygame.image.load("graphics/Sprites/bones/bone.png").convert_alpha()
        self.bone_width = self.bone_img.get_width()
        self.bone_height = self.bone_img.get_height()

        # 3 hàng y khác nhau trong arena
        arena_top = arena_rect.top
        arena_bottom = arena_rect.bottom
        spacing = (arena_bottom - arena_top) // 4
        self.rows_y = [
            arena_top + spacing,
            arena_top + spacing * 2,
            arena_top + spacing * 3
        ]

        # Danh sách xương
        self.bones = []
        self.speed = 8

    def spawn_bones(self):
        """Sinh thêm xương ở ngoài màn hình bên phải"""
        for y in self.rows_y:
            bone_rect = self.bone_img.get_rect(topleft=(self.screen_width + 50, y))
            self.bones.append(bone_rect)

    def update(self, box_rect):
        """Cập nhật vị trí xương & chỉ hiển thị khi đi vào trong box"""
        for bone in self.bones:
            bone.x -= self.speed

        # Xóa xương đi ra khỏi màn hình
        self.bones = [b for b in self.bones if b.right > 0]

    def draw(self, screen, box_rect):
        """Vẽ xương chỉ khi nằm trong box"""
        for bone in self.bones:
            if box_rect.left < bone.centerx < box_rect.right:
                screen.blit(self.bone_img, bone)
