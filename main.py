import pygame
from sys import exit
from pygame import Vector2
from entities.blaster import MultiBlaster
from entities.stand_floor import MultiFloor
from game.level_3.Sand import CallBoss
from game.player.player import Player
from game.player.player_turn import PlayerTurnManager


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

def draw_background(box_rect: pygame.Rect):
    wbox = pygame.Surface((box_rect.width + 10, box_rect.height + 10))
    wbox.fill('White')

    bbox = pygame.Surface((box_rect.width, box_rect.height))
    bbox.fill('Black')
    mainbackground = pygame.Surface((1000, 600))
    mainbackground.fill('Black')

    screen.blit(mainbackground, (0, 0))
    screen.blit(wbox, (box_rect.x - 5, box_rect.y - 5))
    screen.blit(bbox, (box_rect.x, box_rect.y))


    return box_rect


# Player
player = Player(500, 470)

# Enemy
floors = MultiFloor()
blasters = MultiBlaster()
boss_lv_3 = CallBoss(screen, player, player.rect, blasters, floors)
player_turn_manager = PlayerTurnManager(screen, player, boss_lv_3) # <-- TẠO INSTANCE

game_state = 'BOSS_ATTACK'
boss_hp = 1000
#base arena
arena_x, arena_y = 300, 285
arena_width, arena_height = 400, 200
target_w, target_h, target_x, target_y = arena_width, arena_height, arena_x, arena_y

def draw_health_bar(surface, x, y, current_hp, max_hp, width=40, height=25):
    ratio = current_hp / max_hp
    if ratio < 0: ratio = 0
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
        if game_state == 'PLAYER_TURN':
            player_turn_manager.handle_input(event)

    dt = min(clock.tick(60) * 0.001, 1 / 30)

    if is_active:
        # --- PHẦN 1: CẬP NHẬT LOGIC GAME ---
        if game_state == 'BOSS_ATTACK':

            player.update(floors.floors, pygame.Rect(arena_x, arena_y, arena_width, arena_height))
            if not boss_lv_3.is_attacking:
                game_state = 'PLAYER_TURN'
                player_turn_manager.start_turn()
        elif game_state == 'PLAYER_TURN':
            target_w, target_h, target_x, target_y = 600, 150, (1000 - 600) / 2, (485 - 150)
            is_player_turn_continuing = player_turn_manager.update(dt)
            if not is_player_turn_continuing:
                game_state = 'BOSS_ATTACK'
                boss_lv_3.start_next_attack()

        # --- PHẦN 2: CẬP NHẬT VISUAL (ARENA) ---
        arena_width = lerp(arena_width, target_w, 0.1)
        arena_height = lerp(arena_height, target_h, 0.1)
        arena_x = lerp(arena_x, target_x, 0.1)
        arena_y = lerp(arena_y, target_y, 0.1)
        box_rect = pygame.Rect(arena_x, arena_y, arena_width, arena_height)

        # --- PHẦN 3: VẼ MỌI THỨ LÊN MÀN HÌNH ---
        draw_background(box_rect)

        target_w, target_h, target_x, target_y = boss_lv_3.arena_state()
        boss_lv_3.update(dt, pygame.Rect(arena_x, arena_y, arena_width, arena_height), player)

        if game_state == 'BOSS_ATTACK':
            # Ràng buộc và vẽ player trong arena
            if player.rect.left < box_rect.left: player.rect.left = box_rect.left
            if player.rect.right > box_rect.right: player.rect.right = box_rect.right
            if player.rect.top < box_rect.top: player.rect.top = box_rect.top
            if player.rect.bottom > box_rect.bottom: player.rect.bottom = box_rect.bottom
            player.draw(screen)

            # Xử lý va chạm blaster
            player_mask = pygame.mask.from_surface(player.image)
            for blaster in blasters.blasters:
                if blaster.beam and blaster.beam.is_active:
                    beam_img = blaster.beam.sprite.image
                    beam_rect = beam_img.get_rect(center=(blaster.beam.abs_x, blaster.beam.abs_y))
                    beam_mask = pygame.mask.from_surface(beam_img)
                    offset = (player.rect.x - beam_rect.x, player.rect.y - beam_rect.y)
                    if beam_mask.overlap(player_mask, offset):
                        player.damaged(10)

        elif game_state == 'PLAYER_TURN':
            # Vẽ UI của lượt người chơi
            player_turn_manager.draw(box_rect)

        # Vẽ thanh máu (luôn hiển thị)
        draw_health_bar(screen, 435, 500, player.player_hp, player.max_hp)

    else:
        screen.fill("Red")

    pygame.display.update()
    clock.tick(60)