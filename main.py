import pygame
import sys
import os
import subprocess
from database import Database

if len(sys.argv) > 1:
    user_id = int(sys.argv[1])
else:
    user_id = 1 

def open_game_over():
    pygame.quit()
    over_path = os.path.join(os.path.dirname(__file__), "game_over.py")
    subprocess.Popen([sys.executable, over_path])
    sys.exit()

def open_game_clear():
    pygame.quit()
    clear_path = os.path.join(os.path.dirname(__file__), "game_clear.py")
    subprocess.Popen([sys.executable, clear_path])
    sys.exit()
from pygame import Vector2


from entities.blaster import MultiBlaster
from entities.stand_floor import MultiFloor
from game.level_3.Sand import CallBoss
from game.player.player import Player
from pause_menu import pause_menu  


pygame.init()
screen_width, screen_height = 1000, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Undertale")
clock = pygame.time.Clock()
is_active = True

g_font = pygame.font.Font("font/MonsterFriendBack.otf", 22)


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)


db = Database()

def return_to_menu():
    pygame.quit()
    menu_path = os.path.join(os.path.dirname(__file__), "menu1.py")
    subprocess.Popen([sys.executable, menu_path])
    sys.exit()

def open_leaderboard():
    pygame.quit()
    lb_path = os.path.join(os.path.dirname(__file__), "leaderboard.py")
    subprocess.Popen([sys.executable, lb_path])
    sys.exit()


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

def draw_background(box_rect: pygame.Rect):
    wbox = pygame.Surface((box_rect.width + 10, box_rect.height + 10))
    wbox.fill(WHITE)

    bbox = pygame.Surface((box_rect.width, box_rect.height))
    bbox.fill(BLACK)
    mainbackground = pygame.Surface((screen_width, screen_height))
    mainbackground.fill(BLACK)

    screen.blit(mainbackground, (0, 0))
    screen.blit(wbox, (box_rect.x - 5, box_rect.y - 5))
    screen.blit(bbox, (box_rect.x, box_rect.y))
    return box_rect

def draw_health_bar(surface, x, y, current_hp, max_hp, width=40, height=25):
    ratio = current_hp / max_hp
    if ratio < 0: ratio = 0
    pygame.draw.rect(surface, YELLOW, (x, y, width, height))
    pygame.draw.rect(surface, RED, (x, y, width * ratio, height))
    hp_text = g_font.render("HP", True, WHITE)
    hp_rect = hp_text.get_rect(midright=(x - 5, y + height // 2))
    surface.blit(hp_text, hp_rect)
    hp_val = g_font.render(f"{current_hp}/{max_hp}", True, WHITE)
    hp_val_rect = hp_val.get_rect(midleft=(x + width + 30, y + height // 2))
    surface.blit(hp_val, hp_val_rect)

#player+boss
player = Player(500, 470)
floors = MultiFloor()
blasters = MultiBlaster()
boss_lv_3 = CallBoss(screen, player, player.rect, blasters, floors)

#base arena
arena_x, arena_y = 300, 285
arena_width, arena_height = 400, 200

paused = False

score = 0

while True:
    dt = min(clock.tick(60) * 0.001, 1 / 30)

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #pause menu
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            paused = True
            choice = pause_menu(screen) 
            if choice == "RESUME":
                paused = False
            elif choice == "MAIN MENU":
                return_to_menu()
            elif choice == "LEADERBOARD":
                open_leaderboard()
            elif choice == "EXIT":
                pygame.quit()
                sys.exit()

    if paused:
        continue  

    dt = min(clock.tick(60) * 0.001, 1 / 30)

    if is_active:
        # background
        target_w, target_h, target_x, target_y = boss_lv_3.arena_state()
        arena_width = lerp(arena_width, target_w, 0.1)
        arena_height = lerp(arena_height, target_h, 0.1)
        arena_x = lerp(arena_x, target_x, 0.1)
        arena_y = lerp(arena_y, target_y, 0.1)
        box_rect = pygame.Rect(arena_x, arena_y, arena_width, arena_height)
        draw_background(box_rect)

        #player
        player.update(floors.floors, box_rect)

        #giới hạn di chuyển trong arena
        if player.rect.left < box_rect.left: player.rect.left = box_rect.left
        if player.rect.right > box_rect.right: player.rect.right = box_rect.right
        if player.rect.top < box_rect.top: player.rect.top = box_rect.top
        if player.rect.bottom > box_rect.bottom: player.rect.bottom = box_rect.bottom

        # beamhit
        center = Vector2(player.rect.center)
        boss_lv_3.update(dt, box_rect, player)
        player_mask = pygame.mask.from_surface(player.image)
        for blaster in blasters.blasters:
            if blaster.beam and blaster.beam.is_active:
                beam_img = blaster.beam.sprite.image
                beam_rect = beam_img.get_rect(center=(blaster.beam.abs_x, blaster.beam.abs_y))
                beam_mask = pygame.mask.from_surface(beam_img)
                offset = (player.rect.x - beam_rect.x, player.rect.y - beam_rect.y)
                if beam_mask.overlap(player_mask, offset):
                    player.damaged(10)

        #player + hpbar
        player.draw(screen)
        draw_health_bar(screen, 435, 500, player.player_hp, player.max_hp)
        # 
        boss_name = g_font.render("SANS", True, WHITE)
        boss_name_rect = boss_name.get_rect(midtop=(500, 50))
        screen.blit(boss_name, boss_name_rect)

        #status check
        if player.player_hp <= 0:
            is_active = False
        # thêm elì + t.g vào đây để tính cái win

    else:
        db.save_score(user_id, score)
        
        

    pygame.display.update()
