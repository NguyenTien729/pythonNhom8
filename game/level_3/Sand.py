import math

from pygame import Vector2

from entities.blaster import MultiBlaster
from entities.bone_wave import BoneWave
from entities.stand_floor import MultiFloor
from game.level_3.gravity_bone import GravityBone
from game.level_3.more_bone_floor import MoreBoneFloor
from game.level_3.random_blaster import RandomBlaster
from game.level_3.blaster_round import BlasterCircle
from game.level_3.blaster_floor import BlasterFloor
from game.level_3.bone_pattern_middle import BonePatternMiddle
from game.level_3.bone_pattern_sideway import BonePatternSideway

import pygame

from game.level_3.special_attack import SpecialAttack


class CallBoss(pygame.sprite.Sprite):
    phase_time = 8
    change_phase_time = 2

    def __init__(self, screen, player, player_rect, blasters: MultiBlaster, floors: MultiFloor):
        super().__init__()
        self.screen = screen
        self.box_rect = pygame.Rect(0, 0, 0, 0)
        self.box_center = Vector2(self.box_rect.center)
        self.player_rect = player_rect
        self.center = Vector2(self.player_rect.center)
        self.start_time = pygame.time.get_ticks()


        self.blasters = blasters
        self.floors = floors

        self.beam_width = 3

        self.legs_idle = pygame.image.load('graphics/characters/sans/spr_sansb_legs_0.png')
        self.legs_idle = pygame.transform.scale_by(self.legs_idle, 2.5)
        self.body_idle = pygame.image.load('graphics/characters/sans/spr_sansb_torso_0.png')
        self.body_idle = pygame.transform.scale_by(self.body_idle, 2.5)
        self.face_idle = pygame.image.load('graphics/characters/sans/spr_sansb_face_0.png')
        self.face_idle = pygame.transform.scale_by(self.face_idle, 2.5)

        self.body_image = self.body_idle
        self.offset_x = 0.0
        self.offset_y = 0.0

        self.hand_down_frames = [pygame.image.load('graphics/characters/sans/spr_sansb_handdown_0.png'),
                                 pygame.image.load('graphics/characters/sans/spr_sansb_handdown_1.png'),
                                 pygame.image.load('graphics/characters/sans/spr_sansb_handdown_2.png'),
                                 pygame.image.load('graphics/characters/sans/spr_sansb_handdown_3.png'),
                                 pygame.image.load('graphics/characters/sans/spr_sansb_handdown_4.png')]
        self.hand_right_frames = [pygame.image.load('graphics/characters/sans/spr_sansb_rightstrike_0.png'),
                                  pygame.image.load('graphics/characters/sans/spr_sansb_rightstrike_1.png'),
                                  pygame.image.load('graphics/characters/sans/spr_sansb_rightstrike_2.png'),
                                  pygame.image.load('graphics/characters/sans/spr_sansb_rightstrike_3.png'),
                                  pygame.image.load('graphics/characters/sans/spr_sansb_rightstrike_4.png')]

        self.animation_index = 0
        self.animation_index_reverse = 4
        self.animation_timer = 0.0
        self.animation_time = 0.1
        self.animation_paused = False
        self.timer = 0
        self.duration = 1.1

        self.leg_rect = self.legs_idle.get_rect()
        self.body_rect = self.body_idle.get_rect()
        self.face_rect = self.face_idle.get_rect()

        self.wiggle_time = 0.0
        self.wiggle_amplitude_head = 1.1
        self.wiggle_amplitude_body = 1.5
        self.wiggle_speed_x = 8
        self.wiggle_speed_y = 16
        self.body_x = 0
        self.face_x = 0
        self.body_y = 0
        self.face_y = 0

        self.special_attack_active = False

        #khai gọi dạng tấn công
        self.blaster_floor = BlasterFloor(self.screen, self.player_rect, self.blasters, self.floors, 2)

        self.blaster_circle = BlasterCircle((500, 380), self.blasters, beam_width = self.beam_width)

        self.blaster_random = RandomBlaster(self.center,  750, 250, 230, 530, self.blasters)

        self.gravity_bone = GravityBone(self.screen, 100, 1, player, player_rect,self.box_rect)

        self.bone_parten_middle = BonePatternMiddle(self.screen,self.box_rect,player, self.floors)

        self.bone_parten_sideway = BonePatternSideway(self.screen,self.box_rect,player)

        self.more_bone_floor = MoreBoneFloor(self.screen, self.blasters, player, self.floors)

        self.bone_wave = BoneWave(self.screen, self.box_rect, player, 45)

        initial_box_rect = pygame.Rect(300, 285, 400, 200)
        self.special_attack = SpecialAttack(screen, initial_box_rect, player, self.player_rect, self.blasters)

        # self.attack_patterns = [self.blaster_floor, self.bone_parten_middle, self.blaster_random, self.blaster_circle, self.gravity_bone, self.bone_parten_sideway]
        self.attack_patterns = [self.special_attack]
        self.attack_index = 0
        self.mod = self.attack_patterns[self.attack_index]
        self.change_mod = False
        self.is_win = False

        self.attack_time = 8
        self.swap_time = 0

        self.sound = pygame.mixer.Sound('sound/sans_battle/MEGALOVANIA.wav')
        self.has_played = False

    #dao động đầu và thân boss
    def wiggle_animation(self, dt: float):
        self.wiggle_time += dt

        offset_x = math.sin(self.wiggle_time * self.wiggle_speed_x)
        offset_y = math.cos(self.wiggle_time * self.wiggle_speed_y)

        self.face_rect.centerx = int(self.face_x + offset_x * self.wiggle_amplitude_head)
        self.face_rect.centery = int(self.face_y + offset_y * self.wiggle_amplitude_head)
        if not isinstance(self.mod, GravityBone):
            self.body_rect.centerx = int(self.body_x + offset_x * self.wiggle_amplitude_body)
            self.body_rect.centery = int(self.body_y + offset_y * self.wiggle_amplitude_body)

    # đổi dạng tấn công
    def attack_mod(self):
        self.floors.destroy_all()
        self.blasters.destroy_all()
        self.attack_index = (self.attack_index + 1) % len(self.attack_patterns)
        self.mod = self.attack_patterns[self.attack_index]

        if hasattr(self.mod, 'start'):
            self.mod.start()

        #reset bone_pattern_middle
        if hasattr(self.mod, 'reset'):
            self.mod.reset()

        self.animation_index = 0
        self.animation_timer = 0.0

    def animation(self, dt: float, player):

        #animation cho gravitybone
        if isinstance(self.mod, GravityBone):
            current_time = self.mod.timer
            self.animation_timer += dt

            #chỉ chạy 1 lần mỗi lần đổi gravity
            if self.mod.pull_start_time < current_time < self.mod.float_time:
                if not self.animation_paused:
                    self.animation_timer = 0.0
                    self.animation_index += 1
                    self.animation_index_reverse -= 1
                    if self.animation_index == 4 or self.animation_index_reverse == 0:
                        self.animation_paused = True
            elif current_time <= self.mod.pull_start_time:
                self.animation_paused = False
                self.animation_index = 0
                self.animation_index_reverse = 0

            if player.gravity_direction in ['top', 'bottom']:
                previous_mask = pygame.mask.from_surface(self.body_image)
                previous_y = previous_mask.centroid()[1]

                if player.gravity_direction == 'top':
                    self.body_image = self.hand_down_frames[self.animation_index_reverse]
                elif player.gravity_direction == 'bottom':
                    self.body_image = self.hand_down_frames[self.animation_index]

                self.body_image = pygame.transform.scale_by(self.body_image, 2.5)
                self.body_rect = self.body_image.get_rect(bottomleft = (self.box_rect.midtop[0] - 77, self.box_rect.midtop[1] - 25))

                current_mask = pygame.mask.from_surface(self.body_image)
                current_y = current_mask.centroid()[1]
                #tính vị trí cổ dựa trên khoảng cách khác nhau của 2 ảnh gần nhất
                if current_y != previous_y and player.gravity_direction == 'top':
                    self.offset_y = current_y - previous_y - 12
                elif current_y != previous_y and player.gravity_direction == 'bottom':
                    self.offset_y = previous_y - current_y - 8

                self.face_rect = self.face_idle.get_rect(midbottom=(self.body_rect.midtop[0] - 2, self.body_rect.centery + self.offset_y))

            elif player.gravity_direction in ['left', 'right']:
                previous_mask = pygame.mask.from_surface(self.body_image)
                previous_x = previous_mask.centroid()[0]

                if player.gravity_direction == 'left':
                    self.body_image = self.hand_right_frames[self.animation_index_reverse]
                elif player.gravity_direction == 'right':
                    self.body_image = self.hand_right_frames[self.animation_index]

                self.body_image = pygame.transform.scale_by(self.body_image, 2.5)
                self.body_rect = self.body_image.get_rect(bottomleft = (self.box_rect.midtop[0] - 77, self.box_rect.midtop[1] - 20))

                current_mask = pygame.mask.from_surface(self.body_image)
                current_x = current_mask.centroid()[0]
                #tính vị trí cổ dựa trên khoảng cách khác nhau của 2 ảnh gần nhất
                if current_x != previous_x and player.gravity_direction == 'left':
                    self.offset_x = current_x - previous_x + 3
                elif current_x != previous_x and player.gravity_direction == 'right':
                    self.offset_x = previous_x - current_x - 15
                self.face_rect = self.face_idle.get_rect(bottomleft = (self.body_rect.bottomleft[0] + 47.5 + self.offset_x, self.body_rect.centery - 40))

        elif not isinstance(self.mod, GravityBone) or self.change_mod:
            self.leg_rect = self.legs_idle.get_rect(midbottom = (self.box_rect.midtop[0], self.box_rect.midtop[1] - 20))
            self.body_image = self.body_idle
            self.body_rect = self.body_image.get_rect(midbottom = (self.leg_rect.midtop[0], self.leg_rect.midtop[1] + 25))
            self.face_rect = self.face_idle.get_rect(midbottom=(self.body_rect.midtop[0], self.body_rect.midtop[1] + 20))

        self.body_x = self.body_rect.centerx
        self.face_x = self.face_rect.centerx

        self.body_y = self.body_rect.centery
        self.face_y = self.face_rect.centery

    #vẽ boss
    def draw(self):
        if not isinstance(self.mod, GravityBone):
            self.screen.blit(self.legs_idle, self.leg_rect)
        self.screen.blit(self.body_image, self.body_rect)
        self.screen.blit(self.face_idle, self.face_rect)

    def update(self, dt: float, box_rect: pygame.Rect, player):
        if not self.has_played:
            self.sound.play(loops=-1)
            self.has_played = True

        if self.is_win:
            self.sound.fadeout(1000)
            self.has_played = False
            return

        if isinstance(self.mod, BonePatternMiddle):
            if self.mod.box_rect != box_rect:
                self.mod.rect_box(box_rect)

        if isinstance(self.mod, BonePatternSideway) or isinstance(self.mod, MoreBoneFloor) or isinstance(self.mod, BoneWave):
            self.mod.rect_box(box_rect)


        #cắt ảnh ngoài arena
        if isinstance(self.mod, GravityBone):
            self.mod.rect_box(box_rect)
            self.mod.bone_stab.update(dt)
            self.screen.set_clip(box_rect)

            for stab in self.mod.bone_stab:
                stab.draw()

            self.screen.set_clip(None)

        self.special_attack.draw(self.box_rect)

        #gọi gravity
        if not isinstance(self.mod, SpecialAttack):
            if isinstance(self.mod, GravityBone) or isinstance(self.mod, BlasterFloor) or isinstance(self.mod, BonePatternMiddle) or isinstance(self.mod, MoreBoneFloor):
                player.set_gravity(True)
            else:
                player.set_gravity(False)

            if not isinstance(self.mod, GravityBone):
                player.change_gravity_direction('bottom')
                player.gravity = 1.25
                player.hold_jump_force = 2.25

        self.box_rect = box_rect
        self.center = Vector2(self.box_rect.center)

        self.animation(dt, player)
        self.wiggle_animation(dt)
        self.draw()

        # ✅ Vẽ flash effect SAU khi vẽ Sans (che toàn bộ màn hình)
        if isinstance(self.mod, SpecialAttack):
            flash_alpha = self.mod.get_flash()
            if flash_alpha > 0:
                flash_surface = pygame.Surface(self.screen.get_size())
                flash_surface.fill((0, 0, 0))
                flash_surface.set_alpha(flash_alpha)
                self.screen.blit(flash_surface, (0, 0))

        self.blaster_random.pivot = Vector2(self.player_rect.center)

        if isinstance(self.mod, SpecialAttack):
            self.special_attack_active = self.mod.is_active

        #đổi dạng attack
        if self.change_mod:
            self.swap_time += dt
            #time delay trước khi đổi
            if self.swap_time >= self.change_phase_time:
                self.swap_time = 0
                self.change_mod = False
                self.attack_mod()

        else:
            if isinstance(self.mod, SpecialAttack):
                self.mod.update(dt, box_rect)

                # QUAN TRỌNG: Không đếm thời gian khi SpecialAttack đang chạy
                # Chỉ chuyển khi SpecialAttack kết thúc
                if not self.mod.is_active:
                    self.attack_time += dt
                    if self.attack_time >= 1.0:  # Delay nhỏ sau khi kết thúc
                        self.attack_time = 0
                        self.change_mod = True
                # Nếu vẫn đang active, không làm gì cả

            else:
                self.mod.update(dt)
                # Thời gian cho các attack khác
                self.attack_time += dt
                if self.attack_time >= self.phase_time:
                    self.attack_time = 0
                    self.change_mod = True

        change_floor_direction = isinstance(self.mod, BonePatternMiddle)

        #hàm cập nhật vật thể
        self.floors.update(change_floor_direction)
        self.floors.draw(self.screen)

        self.blasters.update()
        self.blasters.draw(self.screen)

    def arena_state(self):
        if isinstance(self.mod, SpecialAttack) and self.mod.is_active:
            # Lấy thẳng mục tiêu từ SpecialAttack
            final_box_width, final_box_height, final_box_x, final_box_y = self.mod.arena_state()
            return final_box_width, final_box_height, final_box_x, final_box_y
        else:
            if isinstance(self.mod, BlasterFloor):
                final_box_width = 400
                final_box_height = 200
            elif isinstance(self.mod, RandomBlaster):
                final_box_width = 400
                final_box_height = 200
            elif isinstance(self.mod, BonePatternSideway):
                final_box_width = 200
                final_box_height = 200
            elif isinstance(self.mod, BlasterCircle):
                final_box_width = 200
                final_box_height = 200
            elif isinstance(self.mod, GravityBone):
                final_box_width = 200
                final_box_height = 200
            elif isinstance(self.mod, BonePatternMiddle):
                final_box_width = 500
                final_box_height = 200
            elif isinstance(self.mod, MoreBoneFloor):
                final_box_width = 500
                final_box_height = 175
            else:
                final_box_width = 400
                final_box_height = 200

            final_box_x = (1000 - final_box_width) // 2
            final_box_y = 485 - final_box_height

        return final_box_width, final_box_height, final_box_x, final_box_y