import sys

import pygame

def run_menu(screen, clock, game_context, settings):
    background = pygame.image.load("graphics/sprites/bones/background3.jpg")

    font = pygame.font.Font("font/MonsterFriendBack.otf", 36)
    small_font = pygame.font.Font("font/MonsterFriendBack.otf", 18)

    player_name = game_context["player_name"]
    pygame.display.set_caption("Undertale Menu")

    select_sound = pygame.mixer.Sound("sound/sand_battle/snd_select.wav")
    start_sound = pygame.mixer.Sound("sound/sand_battle/Sound-Effect-Battle-Start.wav")

    # Màu sắc
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)

    options = ["START", "LEADERBOARD", "SETTINGS", "EXIT"]
    selected = 0
    pre_choice = -1

    pygame.key.set_repeat(500, 75)

    while True:
        select_sound.set_volume(settings.sfx_volume)
        start_sound.set_volume(settings.sfx_volume)

        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BLACK)
        screen.blit(background, (0, 0))

        # Tiêu đề
        title = font.render("UNDERTAIL", True, WHITE)
        title_rect = title.get_rect(center=(screen.get_width() // 2, 150))
        screen.blit(title, title_rect)

        # Hiển thị player_name
        name_text = small_font.render(f"PLAYER: {player_name}", True, YELLOW)
        screen.blit(name_text, (20, 20))

        mouse_cursor = False
        for i, opt in enumerate(options):
            buttons_rect = pygame.Rect(screen.get_width() // 2 - 150, 300 + i * 80 - 30, 300, 60)
            if buttons_rect.collidepoint(mouse_pos):
                if selected != i:
                    select_sound.play()
                selected = i
                mouse_cursor = True
                break

        if pre_choice != selected and pre_choice != -1:
            if not mouse_cursor:
                select_sound.play()
        pre_choice = selected

        # Nút bấm
        buttons_rect = []
        for i, opt in enumerate(options):
            text_color = RED if i == selected else WHITE
            text = font.render(opt, True, text_color)
            text_rect = text.get_rect(center=(screen.get_width() // 2, 300 + i * 80))

            screen.blit(text, text_rect)
            buttons_rect.append((opt, text_rect))

        pygame.display.flip()

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
                    pygame.key.set_repeat(0)
                    if selected == 0:
                        start_sound.play()
                    else:
                        select_sound.play()
                    return options[selected]

            if event.type == pygame.MOUSEBUTTONDOWN:
                for opt, rect in buttons_rect:
                    if rect.collidepoint(mouse_pos):
                        pygame.key.set_repeat(0)
                        if opt == "START":
                            start_sound.play()
                        else:
                            select_sound.play()
                        return opt

        clock.tick(30)
