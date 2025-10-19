import pygame
import sys
from game.db.database import Database

if len(sys.argv) > 1:
    user_id = int(sys.argv[1])
else:
    user_id = 1

from ui.login_ui import login_ui
from ui.enter_name import get_player_name
from ui.menu_screen import run_menu
from ui.leaderboard import leaderboard_main
from ui.end_screen import end_screen
from ui.pause_menu import pause_menu

from pygame import Vector2
from entities.blaster import MultiBlaster
from entities.stand_floor import MultiFloor
from game.level_3.Sand import CallBoss
from game.player.player import Player
from ui.setting_screen import setting_screen

class SettingsManager:
    def __init__(self):
        self.music_volume = 0.5
        self.sfx_volume = 0.5

def game_run(screen, clock, db, game_context, settings):
    pygame.display.set_caption("Game Run")
    g_font = pygame.font.Font("font/MonsterFriendBack.otf", 22)

    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)

    player = Player(500, 470)
    floors = MultiFloor()
    blasters = MultiBlaster(settings)
    boss_lv_3 = CallBoss(screen, player, player.rect, blasters, floors, settings)
    is_active = True
    survival_timer = 0
    win_score = 1000
    game_paused = False

    arena_x, arena_y = 300, 285
    arena_width, arena_height = 400, 200

    saved_frame = None
    box_rect = pygame.Rect(arena_x, arena_y, arena_width, arena_height)

    def lerp(a: float, b: float, t: float) -> float:
        return a + (b - a) * t

    def draw_background(box_rect: pygame.Rect):
        screen.fill(BLACK)
        wbox = pygame.Surface((box_rect.width + 10, box_rect.height + 10))
        wbox.fill(WHITE)

        bbox = pygame.Surface((box_rect.width, box_rect.height))
        bbox.fill(BLACK)

        screen.blit(wbox, (box_rect.x - 5, box_rect.y - 5))
        screen.blit(bbox, (box_rect.x, box_rect.y))

    def draw_health_bar(surface, x, y, current_hp, max_hp, width=40, height=25):
        ratio = max(0, current_hp / max_hp)

        pygame.draw.rect(surface, YELLOW, (x, y, width, height))
        pygame.draw.rect(surface, RED, (x, y, width * ratio, height))

        hp_text = g_font.render("HP", True, WHITE)
        hp_rect = hp_text.get_rect(midright=(x - 5, y + height // 2))
        surface.blit(hp_text, hp_rect)

        hp_val = g_font.render(f"{current_hp}/{max_hp}", True, WHITE)
        hp_val_rect = hp_val.get_rect(midleft=(x + width + 30, y + height // 2))
        surface.blit(hp_val, hp_val_rect)

    while True:
        if not game_paused:
            dt = clock.tick(60) * 0.001
            survival_timer += dt * 10
        else:
            clock.tick(60)
            dt = 0

        print(dt)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # pause menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if not game_paused:
                    game_paused = True
                    saved_frame = screen.copy()

                choice = pause_menu(screen, settings)
                if choice == "MAIN MENU":
                    boss_lv_3.sound.stop()
                    return "MENU"
                elif choice == "EXIT":
                    pygame.quit()
                    sys.exit()
                elif choice == "RESUME":
                    game_paused = False
                    saved_frame = None

        if game_paused:
            if saved_frame:
                screen.blit(saved_frame, (0, 0))
            pygame.display.update()
            continue

        if is_active:


            target_w, target_h, target_x, target_y = boss_lv_3.arena_state()
            arena_width = lerp(arena_width, target_w, 0.09)
            arena_height = lerp(arena_height, target_h, 0.09)
            arena_x = lerp(arena_x, target_x, 0.09)
            arena_y = lerp(arena_y, target_y, 0.09)
            box_rect = pygame.Rect(arena_x, arena_y, arena_width, arena_height)
            draw_background(box_rect)

            # player
            player.update(floors.floors, box_rect)

            # giới hạn di chuyển trong arena
            player.rect.clamp_ip(box_rect)

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

            # player + hpbar
            player.draw(screen)
            draw_health_bar(screen, 435, 500, player.player_hp, player.max_hp)

            boss_name = g_font.render("SAND", True, WHITE)
            boss_name_rect = boss_name.get_rect(midtop=(500, 50))
            screen.blit(boss_name, boss_name_rect)

            if player.player_hp <= 0 or boss_lv_3.is_win:
                boss_lv_3.sound.stop()
                is_active = False

        else:
            score = survival_timer
            db.save_score(game_context["user_id"], score)
            return "GAME_OVER"

        if boss_lv_3.is_win:
            hp_factor = 1.0 + (player.player_hp / player.max_hp)
            score = (survival_timer + win_score) * hp_factor
            db.save_score(game_context["user_id"], score)
            return "GAME_CLEAR"

        pygame.display.update()

def main():
    pygame.init()
    screen_width, screen_height = 1000, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Undertail")
    clock = pygame.time.Clock()
    db = Database()
    settings = SettingsManager()

    game_over_sound = pygame.mixer.Sound("sound/sand_battle/Sound-Effect-Laugh.wav")
    game_clear_sound = pygame.mixer.Sound("sound/sand_battle/Sound-Effect-You-Win_.wav")

    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    game_context = {
        "user_id": None,
        "player_name": None
    }

    current_state = "LOGIN"

    while True:
        game_over_sound.set_volume(settings.sfx_volume)
        game_clear_sound.set_volume(settings.sfx_volume)

        if current_state == "LOGIN":
            login_result = login_ui(screen, clock, settings)
            if login_result:
                game_context["user_id"], game_context["player_name"] = login_result
                if game_context["player_name"]:
                    current_state = "MENU"
                else:
                    current_state = "ENTER_NAME"

        elif current_state == "ENTER_NAME":
            player_name = get_player_name(screen, db, game_context["user_id"])
            if player_name:
                game_context["player_name"] = player_name
                current_state = "MENU"

        elif current_state == "MENU":
            choice = run_menu(screen, clock, game_context, settings)
            if choice == "START":
                current_state = "GAMEPLAY"
            elif choice == "LEADERBOARD":
                current_state = "LEADERBOARD"
            elif choice == "SETTINGS":
                current_state = "SETTINGS"
            elif choice == "EXIT":
                break

        elif current_state == "GAMEPLAY":
            current_state = game_run(screen, clock, db, game_context, settings)

        elif current_state == "LEADERBOARD":
            current_state = leaderboard_main(screen, clock, settings)

        elif current_state == "SETTINGS":
            current_state = setting_screen(screen, clock, settings)


        elif current_state == "GAME_OVER":
            game_over_sound.play()
            current_state = end_screen(screen, clock, "GAME OVER", RED, "Game Over", settings)


        elif current_state == "GAME_CLEAR":
            game_clear_sound.play()
            current_state = end_screen(screen, clock, "YOU WIN!", YELLOW, "Game Clear", settings)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()