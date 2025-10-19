from typing import Optional
from entities.Beams import create_projectile_abs
import pygame
import math


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


class GasterBlaster(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, x2: float, y2: float, angle: float, settings,  start_angle: Optional[float] = None,
                 sound: Optional[pygame.mixer.Sound] = None, fire_sound: Optional[pygame.mixer.Sound] = None,
                 sprite_prefix: Optional[str] = None, beam_sprite: Optional[str] = None):

        super().__init__()
        self.beam = None
        self.sprite_prefix = sprite_prefix or "graphics/Sprites/blasters/spr_gasterblaster_"
        self.beam_sprite = beam_sprite or "graphics/Sprites/blasters/beam1"
        self.sprite = pygame.image.load(self.sprite_prefix + "0.png").convert_alpha()
        self.sprite = pygame.transform.scale_by(self.sprite, 2.0)
        self.image = self.sprite.copy()
        self.rect = self.image.get_rect(center = (x, y))

        self.sprite_rotation = 0
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2
        self.x_scale = 1
        self.y_scale = 1
        self.beam_alpha_speed = 0.025
        self.beam_width = 1.0

        self.shoot_delay = 80
        self.speed = 80
        self.hold_fire = 6
        self.update_timer = 0

        self.do_rotation = 0
        self.builder_spd = 0

        self.beam_frozen = False

        self.angle_check = angle
        self.angle = angle % 360
        if start_angle is not None:
            self.do_rotation = start_angle
            self.sprite_rotation = start_angle
        if self.angle >= 180:
            self.angle -= 360

        self.settings = settings

        self.sound = sound
        self.fire_sound = fire_sound
        self.sound = self.sound or pygame.mixer.Sound("sound/sans_battle/gasterintro.wav")
        self.fire_sound = self.fire_sound or pygame.mixer.Sound("sound/sans_battle/gasterfire.wav")
        self.sound.set_volume(self.settings.sfx_volume)
        self.fire_sound.set_volume(self.settings.sfx_volume)

        if self.sound is not None:
            self.sound.play()

        self.frames = []
        self.animation_frame_time = 0.0
        self.animation_timer = 0
        self.animation_index = 0
        self.current_frame_index = "0"

    def spawn_beam(self):
        self.beam = create_projectile_abs(self.beam_sprite, 0, 0)
        self.beam.sprite.scale(2 * self.x_scale * self.beam_width, self.y_scale)
        self.beam.p_collision = True
        self.beam.sprite.y_scale = 1.5 * self.x_scale
        self.beam.sprite.x_scale = 1.75 * self.x_scale

        if self.fire_sound:
            self.fire_sound.play()

        self.calculate_beam_position()
        self.beam.blasters = True

    def calculate_beam_position(self):

        self.beam.move_to_absolute(self.x, self.y)

        distance = -44 * self.y_scale
        dx = distance * math.sin(math.radians(self.sprite_rotation))
        dy = -distance * math.cos(math.radians(self.sprite_rotation))

        self.beam.move(dx, dy)

        self.beam.sprite.rotation = self.sprite_rotation - 90

        if self.angle_check >= 0:
            self.beam.sprite.set_pivot(1, 0.5)
        else:
            self.beam.sprite.set_pivot(0, 0.5)

    def scale(self, x, y):
        self.x_scale = x
        self.y_scale = y

        current_frame = "0"
        if hasattr(self, 'current_frame_index'):
            current_frame = self.current_frame_index

        original = pygame.image.load(self.sprite_prefix + current_frame + ".png").convert_alpha()
        self.sprite = pygame.transform.scale_by(original, (2 * x, 2 * y))

    def update_position(self, x: float, y: float):
        self.x = x
        self.y = y
        if self.beam and not self.beam_frozen:
            self.calculate_beam_position()

    def set(self, index: str):
        self.current_frame_index = index
        self.sprite = pygame.image.load(self.sprite_prefix + index + ".png").convert_alpha()
        self.sprite = pygame.transform.scale_by(self.sprite, (2.0 * self.x_scale, 2.0 * self.y_scale))

    def start_animation(self, frames: list[str], frame_time: float):
        self.frames = [self.sprite_prefix + f + ".png" for f in frames]
        self.animation_frame_time = frame_time
        self.animation_timer = 0
        self.animation_index = 0


    def update(self):
        self.sound.set_volume(self.settings.sfx_volume)
        self.fire_sound.set_volume(self.settings.sfx_volume)

        self.update_timer += 1
        #blaster move
        if self.update_timer > self.shoot_delay and self.update_timer > (self.shoot_delay + self.hold_fire):
            self.sprite_rotation = self.angle
            self.builder_spd += 0.5
            self.x += (self.builder_spd * math.sin(math.radians(self.sprite_rotation)))
            self.y += (-self.builder_spd * math.cos(math.radians(self.sprite_rotation)))
        else:
            self.x = lerp(self.x, self.x2, 6 / self.speed)
            self.y = lerp(self.y, self.y2, 6 / self.speed)
            self.do_rotation = lerp(self.do_rotation, self.angle, 6 / self.speed)
            self.sprite_rotation = self.do_rotation

        if self.beam:
            #khóa beam
            if not self.beam_frozen and (self.x < -100 or self.x > 1100 or self.y < -100 or self.y > 700):
                self.beam_frozen = True

            if not self.beam_frozen:
                if self.shoot_delay < self.update_timer <= self.shoot_delay + 8:
                    self.beam.sprite.x_scale += 0.06 * self.x_scale
                if self.update_timer > self.shoot_delay + 8 and self.update_timer > self.shoot_delay + 8 + self.hold_fire:
                    self.beam.sprite.x_scale = max(0, self.beam.sprite.x_scale - 0.05 * self.x_scale)
                    self.beam.sprite.alpha = max(0, self.beam.sprite.alpha - 0.15 * (self.beam_alpha_speed / 0.07))
            else:
                # beam ko bay ra khỏi màn
                self.beam.sprite.alpha = max(0, int(self.beam.sprite.alpha - 1.5 * (self.beam_alpha_speed / 0.07)))
                self.beam.sprite.x_scale = max(0, self.beam.sprite.x_scale - 0.06 * self.x_scale)

            #xóa nếu như beam biến mất
            if self.beam.sprite.alpha <= 0 or self.beam.sprite.x_scale <= 0:
                self.destroy()
                return

        self.image = pygame.transform.rotate(self.sprite, -self.sprite_rotation)
        self.rect = self.image.get_rect(center=(self.x, self.y))

        #cập nhật animation theo thời gian
        self.update_position(self.x, self.y)
        if self.update_timer == self.shoot_delay - 12:
            self.set("1")
        elif self.update_timer == self.shoot_delay - 8:
            self.set("2")
        elif self.update_timer == self.shoot_delay - 4:
            self.set("3")
        elif self.update_timer == self.shoot_delay:
            self.start_animation(["4", "5"], 6 / 60)
            self.spawn_beam()

    def destroy(self):
        if self.beam:
            self.beam.remove()
            self.beam = None
        self.sprite = None
        self.image = None

    def kill(self):
        self.destroy()
        super().kill()


class MultiBlaster:
    def __init__(self, settings):
        self.blasters = pygame.sprite.Group()
        self.settings = settings

    def create_blaster(self, x: float, y: float, x2: float, y2: float, angle: float ,start_angle: Optional[float] = None,
                 sound: Optional[pygame.mixer.Sound] = None, fire_sound: Optional[pygame.mixer.Sound] = None,
                 sprite_prefix: Optional[str] = None, beam_sprite: Optional[str] = None):
        blaster = GasterBlaster(x, y, x2, y2, angle, self.settings, start_angle, sound, fire_sound, sprite_prefix, beam_sprite)
        self.blasters.add(blaster)
        return blaster

    def update(self):
        self.blasters.update()

        for blaster in self.blasters:
            if blaster.image is None:
                self.blasters.remove(blaster)

    def destroy_all(self):
        for blaster in self.blasters:
            blaster.destroy()
        self.blasters.empty()

    def draw(self, surface: pygame.Surface):
        self.blasters.draw(surface)

        for blaster in self.blasters:
                if blaster.beam:
                    blaster.beam.animation(surface)