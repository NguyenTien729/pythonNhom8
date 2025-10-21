import pygame
import sys
from entities.utils import resource_path

def pause_menu(screen, settings, saved_frame):
    pygame.mixer.pause()

    # Font
    title_font = pygame.font.Font(resource_path("font/MonsterFriendBack.otf"), 48)
    option_font = pygame.font.Font(resource_path("font/MonsterFriendBack.otf"), 28)

    # Danh sách lựa chọn phải TRÙNG với main.py
    options = ["RESUME", "SETTINGS" ,"LEADERBOARD", "MAIN MENU", "EXIT"]
    selected = 0
    pre_choice = -1

    select_sound = pygame.mixer.Sound(resource_path("sound/sand_battle/snd_select.wav"))

    clock = pygame.time.Clock()

    pygame.key.set_repeat(500, 75)

    while True:
        select_sound.set_volume(settings.sfx_volume)
        mouse_pos = pygame.mouse.get_pos()

        if saved_frame:
            screen.blit(saved_frame, (0, 0))

        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Vẽ tiêu đề
        title_surf = title_font.render("PAUSED", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(500, 180))
        screen.blit(title_surf, title_rect)

        mouse_cursor = False
        button_rects = []

        for i, text in enumerate(options):
            rect = pygame.Rect(500 - 150, 300 + i * 60 - 20, 300, 50)
            if rect.collidepoint(mouse_pos):
                if selected != i:
                    select_sound.play()
                selected = i
                mouse_cursor = True
            button_rects.append((text, rect))

        if pre_choice != selected and pre_choice != -1:
            if not mouse_cursor:
                select_sound.play()
        pre_choice = selected

        for i, text in enumerate(options):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            surf = option_font.render(text, True, color)
            rect = surf.get_rect(center=(500, 300 + i * 60))
            screen.blit(surf, rect)

        pygame.display.update()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.key.set_repeat(0)
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    text = options[selected]
                    select_sound.play()
                    if text == "SETTINGS":
                        from ui.setting_screen import setting_screen
                        setting_screen(screen, clock, settings)
                    elif text == "LEADERBOARD":
                        from ui.leaderboard import leaderboard_main
                        leaderboard_main(screen, clock, settings)
                    else:
                        pygame.key.set_repeat(0)
                        pygame.mixer.unpause()
                        return text

                elif event.key == pygame.K_ESCAPE:
                    select_sound.play()
                    pygame.key.set_repeat(0)
                    pygame.mixer.unpause()
                    return "RESUME"

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for text, rect in button_rects:
                    if rect.collidepoint(mouse_pos):
                        select_sound.play()
                        if text == "SETTINGS":
                            from ui.setting_screen import setting_screen
                            setting_screen(screen, clock, settings)
                        elif text == "LEADERBOARD":
                            from ui.leaderboard import leaderboard_main
                            leaderboard_main(screen, clock, settings)
                        else:
                            pygame.mixer.unpause()
                            pygame.key.set_repeat(0)
                            return text
                        break
