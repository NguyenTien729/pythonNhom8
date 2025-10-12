import pygame

from entities.blaster import MultiBlaster
from entities.bone_wave import BoneWave
from entities.increasing_bone import IncreasingBone
from entities.triple_bone import TripleBone
from game.level_3.blaster_round import BlasterCircle
from game.level_3.gravity_bone import GravityBone, MultiBoneStab
from game.level_3.bone_pattern_sideway import BonePatternSideway


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


class SpecialAttack:
    def __init__(self, screen, box_rect, player, player_rect, blasters: MultiBlaster):
        self.end_box_rect = None
        self.current_box_rect = None
        self.screen = screen
        self.box_rect = box_rect
        self.phase3_original_x = self.box_rect.x

        self.player = player
        self.player_rect = player_rect
        self.blasters = blasters

        self.is_active = False
        self.timer = 0.0
        self.phase = 0

        self.side = None
        self.gravity_bone = GravityBone(self.screen, 100, 1, self.player, self.player_rect, self.box_rect, 50, 0.6,
                                        self.side)
        self.bone_parten_sideway = BonePatternSideway(self.screen, self.box_rect, self.player)
        self.bone_wave = BoneWave(self.screen, self.box_rect, self.player, 15)
        self.blaster_circle = BlasterCircle((500, 380), self.blasters, beam_width=1)
        self.triple_bone = TripleBone(self.screen, self.box_rect, self.player)
        self.increasing_bone = IncreasingBone(self.screen, self.box_rect, self.player)
        self.bone_stabs = pygame.sprite.Group()
        self.last_side = [['left', 'top'], ['top', 'bottom'], ['bottom', 'right']]

        self.gravity_bones_multi = []
        self.multi_bone_stab = MultiBoneStab()
        self.phase4_attacks_created = False
        self.phase_4_pair_index = 0
        self.phase4_stage = None
        self.phase3_stage = None

        self.flash_active = False
        self.flash_timer = 0.0
        self.flash_duration = 0.5

        # ✅ Thêm flag để theo dõi trạng thái spawn
        self.bone_wave_spawning = False
        self.triple_bone_spawning = False
        self.increasing_bone_spawning = False

    def start(self):
        self.is_active = True
        self.timer = 0.0
        self.phase = 1
        self.player.set_gravity(True)
        self.end_box_rect = self.box_rect.copy()
        self.current_box_rect = self.box_rect.copy()

    def stop(self):
        self.is_active = False
        self.timer = 0.0
        self.player.set_gravity(False)
        self.player.change_gravity_direction('bottom')

        if hasattr(self.gravity_bone, 'reset'): self.gravity_bone.reset()
        if hasattr(self.bone_parten_sideway, 'reset'): self.bone_parten_sideway.bones.empty()
        if hasattr(self.bone_wave, 'reset'): self.bone_wave.reset()
        if hasattr(self.triple_bone, 'reset'): self.triple_bone.reset()
        if hasattr(self.increasing_bone, 'reset'): self.increasing_bone.reset()

    def cleanup_offscreen_bones(self, bone_group):
        for bone in list(bone_group):
            if bone.rect.left < -50:
                bone.kill()

    def update(self, dt, box_rect):
        if not self.is_active:
            return

        self.timer += dt

        # Căn giữa tự động theo chiều Y, X sẽ được lerp xử lý
        self.gravity_bone.rect_box(box_rect)
        self.bone_parten_sideway.rect_box(box_rect)
        self.bone_wave.rect_box(box_rect)
        self.triple_bone.rect_box(box_rect)
        self.increasing_bone.rect_box(box_rect)

        if self.phase == 1:
            self.end_box_rect.width = 200
            self.end_box_rect.height = 200
            self.end_box_rect.x = (1000 - 200) / 2

            if self.timer >= 1:
                self.gravity_bone.update(dt)

                #reset bone
                if self.gravity_bone.done():
                    self.gravity_bone.reset()

            if self.timer >= 3:
                self.phase = 2
                self.player.set_gravity(False)

        elif self.phase == 2:
            self.end_box_rect.width = 200
            self.end_box_rect.height = 200
            self.end_box_rect.x = (1000 - 200) / 2

            if self.bone_parten_sideway:
                self.bone_parten_sideway.update(dt)

            if self.timer >= 6:
                if self.bone_parten_sideway:
                    self.bone_parten_sideway.stop()
                self.player.set_gravity(True)
                self.player.change_gravity_direction('left')
                self.player.gravity = 500
            if self.timer >= 6.2:
                self.phase = 3

        elif self.phase == 3:
            if self.phase3_stage is None:
                self.phase3_stage = 'expanding'
                self.end_box_rect.width = self.screen.get_width() + 100
                self.end_box_rect.height = 150
                self.end_box_rect.x = (1000 - 200) / 2
                self.player.set_gravity(True)
                self.player.gravity = 1.25
                self.player.change_gravity_direction('right')

            if self.phase3_stage == 'expanding':
                self.box_rect.x = (1000 - 200) / 2

                if abs(box_rect.width - self.end_box_rect.width) < 200:
                    self.phase3_stage = 'moving'
                    self.end_box_rect.x = -100

            self.player.change_gravity_direction('right')
            if self.phase3_stage == 'moving':
                if self.player.rect.left < 30:
                    self.player.rect.left = 30
                    self.player.velocity.x = 0
                else:
                    self.player.velocity.x = -20

            if 7.5 <= self.timer < 10.5:
                self.bone_wave_spawning = True
                self.bone_wave.update(dt)
            else:
                self.bone_wave_spawning = False

            if not self.bone_wave_spawning and len(self.bone_wave.bones) > 0:
                self.bone_wave.bones.update(dt)
                self.cleanup_offscreen_bones(self.bone_wave.bones)

            if 10.5 <= self.timer < 13:
                self.triple_bone_spawning = True
                self.triple_bone.update(dt)
            else:
                self.triple_bone_spawning = False

            if not self.triple_bone_spawning and len(self.triple_bone.bones) > 0:
                self.triple_bone.bones.update(dt)
                self.cleanup_offscreen_bones(self.triple_bone.bones)

            if 13.5 <= self.timer < 15:
                self.increasing_bone_spawning = True
                self.increasing_bone.update(dt)
            else:
                self.increasing_bone_spawning = False

            if not self.increasing_bone_spawning and len(self.increasing_bone.bones) > 0:
                self.increasing_bone.bones.update(dt)
                self.cleanup_offscreen_bones(self.increasing_bone.bones)

            if self.timer >= 15:
                all_bones_gone = (
                        len(self.bone_wave.bones) == 0 and
                        len(self.triple_bone.bones) == 0 and
                        len(self.increasing_bone.bones) == 0
                )

                if all_bones_gone:
                    self.phase = 4
                    self.phase4_stage = 'right_shrinking'
                    self.end_box_rect.x = box_rect.x
                    target_width = self.box_rect.right - box_rect.x
                    self.end_box_rect.width = target_width
                    print("Chuyển sang phase 4")

        elif self.phase == 4:
            if self.phase4_stage == 'right_shrinking':
                if self.player.rect.left < 30:
                    self.player.rect.left = 35
                self.player.velocity.x += 25
                if abs(box_rect.right - self.box_rect.right) < 5 and self.player.rect.right >= box_rect.right - 5:
                    self.phase4_stage = 'single_stab'
                    self.gravity_bone.reset()
                    self.gravity_bone.side_options = ['right']
                    self.gravity_bone.current_side = 'right'

            elif self.phase4_stage == 'single_stab' and self.timer >= 15:
                self.gravity_bone.update(dt)

                if self.gravity_bone.timer >= self.gravity_bone.duration:
                    self.phase4_stage = 'left_shrinking'
                    self.end_box_rect.width = 200
                    self.end_box_rect.height = 200
                    self.end_box_rect.x = (1000 - 200) / 2

            elif self.phase4_stage == 'left_shrinking':
                self.phase_4_pair_index = 0
                self.flash_active = True
                self.flash_timer = 0.0
                self.flash_duration = 0.6
                self.phase4_stage = 'multi_stab_flash'

            elif self.phase4_stage == 'multi_stab_flash':
                self.flash_timer += dt

                if self.flash_timer >= 0.3:
                    self.phase4_stage = 'multi_stab'

            elif self.phase4_stage == 'multi_stab':
                if self.flash_active:
                    self.flash_timer += dt
                    if self.flash_timer >= self.flash_duration:
                        self.flash_active = False
                        self.flash_timer = 0.0
                        self.flash_duration = 0.3

                if self.phase_4_pair_index < len(self.last_side):
                    if not self.phase4_attacks_created:
                        current_pair = self.last_side[self.phase_4_pair_index]

                        if self.phase_4_pair_index == 0:
                            self.player.rect.top = self.box_rect.top + 5
                            self.player.rect.left = self.box_rect.left + 5
                        elif self.phase_4_pair_index == 1:
                            self.player.rect.centery = self.box_rect.centery
                            self.player.rect.centerx = self.box_rect.centerx
                        elif self.phase_4_pair_index == 2:
                            self.player.rect.right = self.box_rect.right - 5
                            self.player.rect.bottom = self.box_rect.bottom - 5

                        self.player.velocity = pygame.Vector2(0, 0)

                        self.multi_bone_stab.create_bone_stab(
                            self.screen, 100, 1, self.player, self.player.rect,
                            box_rect, height=50, duration=0.7, side=[current_pair[0]]
                        )

                        self.multi_bone_stab.create_bone_stab(
                            self.screen, 100, 1, self.player, self.player.rect,
                            box_rect, height=50, duration=0.7, side=[current_pair[1]]
                        )

                        self.phase4_attacks_created = True
                        print(f"✅ Created pair {self.phase_4_pair_index}: {current_pair}")

                    self.multi_bone_stab.update(dt)
                    self.multi_bone_stab.rect_box(pygame.Rect((1000 - 200) / 2, 485 - 200, 200, 200))

                    done = self.multi_bone_stab.done()

                    if done and not self.flash_active:
                        self.multi_bone_stab.destroy_all()
                        self.phase_4_pair_index += 1
                        self.phase4_attacks_created = False

                        if self.phase_4_pair_index < len(self.last_side):
                            self.flash_active = True
                            self.flash_timer = 0.0

                else:
                    self.phase = 5
                    self.player.set_gravity(False)

        elif self.phase == 5:
            if self.timer <= 31:
                self.blaster_circle.update(dt)
            else:
                self.stop()

    def draw(self, box_rect):
        if self.is_active:
            if len(self.bone_wave.bones) > 0:
                self.bone_wave.bones.draw(self.screen)

            if len(self.triple_bone.bones) > 0:
                self.triple_bone.bones.draw(self.screen)

            if len(self.increasing_bone.bones) > 0:
                self.increasing_bone.bones.draw(self.screen)

            # Clip chỉ cho gravity bones và stabs
            self.screen.set_clip(box_rect)

            if self.phase == 1:
                self.gravity_bone.draw()
            elif self.phase == 4:
                if self.phase4_stage == 'single_stab':
                    self.gravity_bone.draw()
                elif self.phase4_stage in ['multi_stab', 'multi_stab_flash']:
                    self.multi_bone_stab.draw()

            self.screen.set_clip(None)

    def get_flash(self):
        if self.flash_active:
            return  255
        return 0

    def arena_state(self):
        if not self.is_active:
            return int(self.box_rect.width), int(self.box_rect.height), int(self.box_rect.x), int(
                485 - self.end_box_rect.height)
        return int(self.end_box_rect.width), int(self.end_box_rect.height), int(self.end_box_rect.x), int(
            485 - self.end_box_rect.height)