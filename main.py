import pygame
from sys import exit

from pygame import Vector2

from entities.blaster import MultiBlaster
from entities.stand_floor import MultiFloor
from game.level_3.Sand import CallBoss
from game.player.player import Player

pygame.init()
screen_width, screen_height = 1000, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Undertail')
clock = pygame.time.Clock()
is_active = True

# font
g_font = pygame.font.Font("font/MonsterFriendBack.otf", 22)

def lerp (a: float, b: float, t: float) -> float:
    return a + (b - a) * t

# Background

def draw_background(boxl, boxw):
    wbox = pygame.Surface((boxl, boxw))
    wbox.fill('White')

    box_x = ((1000 - boxl) // 2) + 5
    box_y = 485 - boxw
    box_width = boxl - 10
    box_height = boxw - 10

    bbox = pygame.Surface((box_width, box_height))
    bbox.fill('Black')
    mainbackground = pygame.Surface((1000, 600))
    mainbackground.fill('Black')

    box_rect = pygame.Rect(box_x, box_y, box_width, box_height)

    screen.blit(mainbackground, (0, 0))
    screen.blit(wbox, (box_x - 5,box_y - 5))
    screen.blit(bbox, (box_x, box_y))

    return box_rect


# Player
player = Player(500, 470)

# enermy
skull_surf = pygame.image.load('graphics/Sprites/blasters/beam.png').convert_alpha()
skull_rect = skull_surf.get_rect(topleft=(100, 100))

bone_surf = pygame.image.load('graphics/Sprites/bones/wavy_bone_down.png').convert_alpha()
bone_rect = bone_surf.get_rect(topleft=(1000, 285))
bone_surf2 = pygame.image.load('graphics/Sprites/bones/wavy_bone_up.png').convert_alpha()
bone_rect2 = bone_surf2.get_rect(topleft=(1000, 360))

bone_speed = 10

floors = MultiFloor()
blasters = MultiBlaster()
boss_lv_3 = CallBoss(screen, player.rect, blasters, floors)

arena_width = 400
arena_height = 200
final_box_width = 400
final_box_height = 200

def draw_health_bar(surface, x, y, current_hp, max_hp, width=40, height=25):
    ratio = current_hp / max_hp
    if ratio < 0: ratio = 0
    # box_rect = pygame.Rect(0, 0, 1000, 600)
    # pygame.draw.rect(surface, (0,0,0), box_rect)
    pygame.draw.rect(surface, (255, 255, 0), (x, y, width, height))
    pygame.draw.rect(surface, (255, 0, 0), (x, y, width * ratio, height))
    # HP text
    hp_text = g_font.render("HP", True, (255, 255, 255))
    hp_rect = hp_text.get_rect(midright=(x - 5, y + height // 2))
    surface.blit(hp_text, hp_rect)
    # HP value
    hp_val = g_font.render(f"{current_hp}/{max_hp}", True, (255, 255, 255))
    hp_val_rect = hp_val.get_rect(midleft=(x + width + 30, y + height // 2))
    surface.blit(hp_val, hp_val_rect)


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            print(mouse_pos)

        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_UP:
        #        blaster = blasters.create_blaster(-100, -100, 250, 380, -90, start_angle = 0)
    clock = pygame.time.Clock()


    dt = min(clock.tick(60) * 0.001, 1 / 30)
    # input
    if is_active:

        # background
        final_box_width, final_box_height = boss_lv_3.arena_state()

        arena_width = lerp(arena_width, final_box_width, 0.05)
        arena_height = lerp(arena_height, final_box_height, 0.05)

        box_rect = draw_background(arena_width, arena_height)

        player.update(floors.floors, box_rect)

        if player.rect.left < box_rect.left: player.rect.left = box_rect.left
        if player.rect.right > box_rect.right: player.rect.right = box_rect.right
        if player.rect.top < box_rect.top: player.rect.top = box_rect.top
        if player.rect.bottom > box_rect.bottom: player.rect.bottom = box_rect.bottom

        # Vẽ thanh máu

        # Enemy
        screen.blit(skull_surf, skull_rect)
        screen.blit(bone_surf, bone_rect)
        screen.blit(bone_surf2, bone_rect2)
        bone_rect.x -= bone_speed
        bone_rect2.x -= bone_speed

        if bone_rect.right < 0:
            bone_rect.left = 1000
            bone_rect.y = 300

        # Player
        center = Vector2(player.rect.center)
        # blaster_spawner.pivot = center

        boss_lv_3.update(dt, box_rect, player)

        if bone_rect.colliderect(player.rect):
            player.damaged(5)

        # Va chạm với beam
        player_mask = pygame.mask.from_surface(player.image)
        for blaster in blasters.blasters:
            if blaster.beam and blaster.beam.is_active:
                beam_img = blaster.beam.sprite.image
                beam_rect = beam_img.get_rect(center=(blaster.beam.abs_x, blaster.beam.abs_y))
                beam_mask = pygame.mask.from_surface(beam_img)
                offset = (player.rect.x - beam_rect.x, player.rect.y - beam_rect.y)
                if beam_mask.overlap(player_mask, offset):
                    player.damaged(10)

        # VẼ MỌI THỨ
        screen.blit(bone_surf, bone_rect)
        player.draw(screen)
        draw_health_bar(screen, 435, 500, player.player_hp, player.max_hp)

    else:
        screen.fill("Red")

    pygame.display.update()
    clock.tick(60)