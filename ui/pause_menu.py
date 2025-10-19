import pygame
import sys

def pause_menu(screen, settings):
    pygame.mixer.pause()
    paused = True

    # Font
    title_font = pygame.font.Font("font/MonsterFriendBack.otf", 48)
    option_font = pygame.font.Font("font/MonsterFriendBack.otf", 28)

    # Danh sách lựa chọn phải TRÙNG với main.py
    options = ["RESUME", "MAIN MENU", "LEADERBOARD", "EXIT"]
    selected = 0

    select_sound = pygame.mixer.Sound("sound/sans_battle/snd_select.wav")
    select_sound.set_volume(settings.sfx_volume)

    clock = pygame.time.Clock()

    while paused:
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Vẽ tiêu đề
        title_surf = title_font.render("PAUSED", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(500, 180))
        screen.blit(title_surf, title_rect)

        button_rects = []
        for i, text in enumerate(options):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            surf = option_font.render(text, True, color)
            rect = surf.get_rect(center=(500, 300 + i * 60))
            screen.blit(surf, rect)
            button_rects.append((text, rect))

        pygame.display.update()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    pygame.mixer.unpause()
                    return options[selected]  # trả về đúng chuỗi main.py dùng

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for i, (text, rect) in enumerate(button_rects):
                    if rect.collidepoint(mouse_pos):
                        selected = i

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for text, rect in button_rects:
                    if rect.collidepoint(mouse_pos):
                        pygame.mixer.unpause()
                        return text  # trả về đúng tên nút
