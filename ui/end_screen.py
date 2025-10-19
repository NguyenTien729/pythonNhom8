import pygame
import sys

def end_screen(screen, clock, title, color, caption, settings):

    pygame.display.set_caption(caption)

    # Font Undertale
    title_font = pygame.font.Font("font/MonsterFriendBack.otf", 80)
    press_font = pygame.font.Font("font/MonsterFriendBack.otf", 20)

    esc_sound = pygame.mixer.Sound("sound/sand_battle/snd_select.wav")

    BLACK = (0, 0, 0)

    while True:
        esc_sound.set_volume(settings.sfx_volume)
        screen.fill(BLACK)

        title_text = title_font.render(title, True, color)
        title_rect = title_text.get_rect(center=(500, 250))
        screen.blit(title_text, title_rect)

        press_text = press_font.render("PRESS ANY KEY TO CONTINUE", True, (200, 200, 200))
        press_rect = press_text.get_rect(bottomright=(980, 580))
        screen.blit(press_text, press_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                esc_sound.play()
                return "LEADERBOARD"

        clock.tick(60)