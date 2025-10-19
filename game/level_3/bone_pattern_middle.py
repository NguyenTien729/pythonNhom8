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
        if self.rect.top > self.arena_rect.bottom + 10 or self.rect.bottom < self.arena_rect.top - 10:
            self.kill()


class BonePatternMiddle:
    bone_delay = 0.8

    def __init__(self, screen, box_rect, players, floors):
        self.screen = screen
        self.box_rect = box_rect
        self.player = players
        self.floor = floors

        # Load sprite xương
        self.bone_image = pygame.image.load("graphics/Sprites/bones/spr_s_boneloop_0.png").convert_alpha()
        self.bone_mask = pygame.mask.from_surface(self.bone_image)
        self.bones = pygame.sprite.Group()
        #bonefloor
        self.floor_bones = pygame.sprite.Group()
        self.floor_bone_image = pygame.image.load("graphics/sprites/bones/spr_s_boneloop_0.png").convert_alpha()

        # Hướng di chuyển + vị trí
        self.spawn_x_positions = [500, 600, 700]
        self.directions = [1, -1, 1]
        self.column_timers = [0, 0, 0]

        # Floor
        self.floor_bone_spawned = False
        self.floor_image = "graphics/sprites/bones/floor1.png"
        self.has_spawned_floor = False
        self.floor_direction = "left"
        self.floor_timer = 0
        self.floor_delay = 0.4

    def spawn_bone(self, x, direction):
        if direction == 1:
            y = self.box_rect.top - 20
        else:
            y = self.box_rect.bottom + 20
        speed = 2
        bone = Bone(self.bone_image, (x, y), speed, direction, self.box_rect)
        self.bones.add(bone)

    def spawn_floor(self):
        self.floor.create_floor(1, 1, self.screen, (290, 435), self.floor_direction, speed=125, sprite_prefix=self.floor_image)

    def spawn_floor_bones(self):
        if self.floor_bone_spawned:
            return

        start_y = self.box_rect.bottom
        image = self.floor_bone_image
        x = self.box_rect.left - 200

        #lấp đầy box bằng bone tạo thành floor
        while x < self.box_rect.right + 100:
            bone = MovingFloorBone(image, (x + 20, start_y), 2, self.box_rect, self.floor_bones)
            self.floor_bones.add(bone)
            x += 20
        self.floor_bone_spawned = True

    def update(self, dt):
        self.floor_timer += dt

        self.screen.set_clip(self.box_rect)

        self.spawn_floor_bones()
        if self.floor_timer >= self.floor_delay:
            self.floor_bones.update(dt)

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

        #vẽ floor
        if not self.has_spawned_floor:
            if self.floor_timer >= self.floor_delay:
                self.spawn_floor()
                #vị trí player khi vào màn
                self.player.rect.centerx = 290
                self.player.rect.centery = 410
                self.player.is_on_ground = True
                self.has_spawned_floor = True

        # Vẽ
        for floor in self.floor_bones:
            self.screen.blit(floor.image, floor.rect)
        #hitbox
        player_mask = pygame.mask.from_surface(self.player.image)
        for bone in self.bones:
            offset = (bone.rect.x - self.player.rect.x, bone.rect.y - self.player.rect.y)
            if player_mask.overlap(bone.mask, offset):
                self.player.damaged(5)
                # self.spawn_sound.play()
                break
        for floor in self.floor_bones:
            offset = (floor.rect.x - self.player.rect.x, floor.rect.y - self.player.rect.y)
            if player_mask.overlap(floor.mask, offset):
                self.player.damaged(5)
                break

        self.screen.set_clip(None)

    #reset nếu có gọi lại
    def reset(self):
        self.has_spawned_floor = False
        self.floor_timer = 0
        self.bones.empty()
        self.column_timers = [0, 0, 0]

    def rect_box(self, rect, reset_spawn=False):
        # chỉ reset khi thực sự muốn
        self.box_rect = rect
        if reset_spawn:
            self.floor_bone_spawned = False
            self.has_spawned_floor = False

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
        if self.rect.left >= self.box_rect.right + 150:
            # tìm bone ngoài cùng bên trái
            leftmost = min(self.group, key=lambda b: b.rect.left)
            # đặt bone này ngay sau bone bên trái (liền mạch)
            self.rect.left = leftmost.rect.left - self.bone_width - 8