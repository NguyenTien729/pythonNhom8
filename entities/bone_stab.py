import pygame
from pygame import Vector2


class BoneStab(pygame.sprite.Sprite):
    def __init__(self, screen, box_rect, side: str, height, speed, player):
        super().__init__()
        self.screen = screen
        self.box_rect = box_rect
        self.side = side
        self.height = height
        self.speed = speed
        self.player = player

        self.image_wide = pygame.image.load('graphics/sprites/bones/spr_s_bonestab_v_wide_0.png')
        self.image_tall = pygame.image.load('graphics/sprites/bones/spr_s_bonestab_h_tall_0.png')

        if self.side in ('left', 'right'):
            self.image = self.image_tall
        elif self.side in ('top', 'bottom'):
            self.image = self.image_wide

        self.rect = self.image.get_rect()

        self.bone_sound = pygame.mixer.Sound('sound/sans_battle/bone-undertale-sound-effect.mp3')
        self.warning_sound = pygame.mixer.Sound('sound/sans_battle/warning_undertale_sound.wav')

        self.movement = Vector2(0, 0)
        self.pos = Vector2(0, 0)
        self.target_pos = Vector2(0, 0)
        self.initial_pos = Vector2(0, 0)

        self.warning_rect = pygame.Rect(0, 0, 0, 0)
        self.state = 0
        self.warning_duration = 0.5
        self.warning_timer = self.warning_duration
        self.delay =0.35
        self.delay_timer = self.delay

        self.have_played_bone = False
        self.have_played_warning = False

        self.pos_cal()

    def pos_cal(self):
        if self.side == 'left':
            #khai báo ví trí gọi và đích của xương
            self.initial_pos.x = self.box_rect.left - self.rect.width / 2
            self.initial_pos.y = self.box_rect.centery
            self.target_pos = (self.box_rect.left - 30 + self.height / 2, self.box_rect.centery)
            #vị trí vẽ cảnh báo
            self.warning_rect.height = self.box_rect.height
            self.warning_rect.width = self.height
            self.warning_rect.topleft = self.box_rect.topleft
            self.movement = Vector2(1, 0)
        elif self.side == 'right':
            self.initial_pos.x = self.box_rect.right + self.rect.width / 2
            self.initial_pos.y = self.box_rect.centery
            self.target_pos = (self.box_rect.right + 30 - self.height / 2, self.box_rect.centery)

            self.warning_rect.height = self.box_rect.height
            self.warning_rect.width = self.height
            self.warning_rect.topright = self.box_rect.topright
            self.movement = Vector2(-1, 0)
        elif self.side == 'top':
            self.initial_pos.x = self.box_rect.centerx
            self.initial_pos.y = self.box_rect.top - self.rect.height / 2
            self.target_pos = (self.box_rect.centerx, self.box_rect.top - 30 + self.height / 2)

            self.warning_rect.width = self.box_rect.width
            self.warning_rect.height = self.height
            self.warning_rect.topleft = self.box_rect.topleft
            self.movement = Vector2(0, 1)
        elif self.side == 'bottom':
            self.initial_pos.x = self.box_rect.centerx
            self.initial_pos.y = self.box_rect.bottom + self.rect.height / 2
            self.target_pos = (self.box_rect.centerx, self.box_rect.bottom + 30 - self.height / 2)

            self.warning_rect.width = self.box_rect.width
            self.warning_rect.height = self.height
            self.warning_rect.bottomleft = self.box_rect.bottomleft
            self.movement = Vector2(0, -1)

        self.initial_pos = Vector2(self.initial_pos)
        self.target_pos = Vector2(self.target_pos)
        self.pos = Vector2(self.initial_pos.copy())
        self.rect.center = self.pos

    def update(self, dt: float):
        #vẽ cảnh báo ban đầu và chuẩn bị tấn công
        if self.state == 0:
            if not self.have_played_warning:
                self.warning_sound.play()
                self.have_played_warning = True
            self.warning_timer -= dt
            if self.warning_timer <= 0:
                self.state = 1
        #bắt đầu đâm xương lên
        elif self.state == 1:
            next_pos = self.pos + self.movement * self.speed * dt
            #lấy vị trí dừng cuối của xương
            if self.movement.x > 0:
                self.pos.x = min(next_pos.x, self.target_pos.x)
            elif self.movement.x < 0:
                self.pos.x = max(next_pos.x, self.target_pos.x)
            elif self.movement.y > 0:
                self.pos.y = min(next_pos.y, self.target_pos.y)
            elif self.movement.y < 0:
                self.pos.y = max(next_pos.y, self.target_pos.y)
            #delay chờ rút xương về
            if self.pos == self.target_pos:
                if not self.have_played_bone:
                    self.bone_sound.play()
                    self.have_played_bone = True
                self.delay_timer -= dt
                if self.delay_timer <= 0:
                    self.state = 2
            self.rect.center = self.pos
        #rút xương
        elif self.state == 2:
            next_pos = self.pos - self.movement * self.speed * dt

            if self.movement.x > 0:
                self.pos.x = max(next_pos.x, self.initial_pos.x)
            elif self.movement.x < 0:
                self.pos.x = min(next_pos.x, self.initial_pos.x)
            elif self.movement.y > 0:
                self.pos.y = max(next_pos.y, self.initial_pos.y)
            elif self.movement.y < 0:
                self.pos.y = min(next_pos.y, self.initial_pos.y)

            if self.pos == self.initial_pos:
                self.kill()
            self.rect.center = self.pos
            self.have_played_bone = False
            self.have_played_warning = False

        if self.state in (1, 2):
            bone_stab_mask = pygame.mask.from_surface(self.image)
            player_mask = pygame.mask.from_surface(self.player.image)
            offset = (self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y)
            if bone_stab_mask.overlap(player_mask, offset):
                self.player.damaged(5)

    def draw(self):
        if self.state == 0:
            pygame.draw.rect(
                surface = self.screen,
                color = (255, 0, 0),
                rect = self.warning_rect,
                width = 2
            )
        else:
            self.screen.blit(self.image, self.rect)