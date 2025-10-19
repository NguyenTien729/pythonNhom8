import sys

import pygame
from entities.setting_slider import Slider

def setting_screen(screen, clock, settings):
    pygame.display.set_caption("Settings")
    title_font = pygame.font.Font("font/MonsterFriendBack.otf", 48)
    option_font = pygame.font.Font("font/MonsterFriendBack.otf", 28)
    font_small = pygame.font.Font("font/MonsterFriendBack.otf", 20)

    esc_sound = pygame.mixer.Sound("sound/sand_battle/snd_select.wav")


    # Màu sắc
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    screen_center = screen.get_rect().center
    music_slider= Slider(screen_center, (500, 40), settings.music_volume, 0, 100)
    sfx_slider = Slider((screen_center[0], screen_center[1] + 150), (500, 40), settings.sfx_volume, 0, 100)
    sliders = [music_slider, sfx_slider]

    current_slider = music_slider

    pygame.key.set_repeat(500, 20)

    while True:
        esc_sound.set_volume(settings.sfx_volume)

        mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()
        print(mouse_pos)

        screen.fill(BLACK)

        title_surf = title_font.render("SETTINGS", True, "yellow")
        title_rect = title_surf.get_rect(center=(500, 120))
        screen.blit(title_surf, title_rect)

        for slider in sliders:
            slider.render(screen)
            if slider == current_slider:
                pygame.draw.rect(screen, "white", slider.container_rect, 5)

        music_label = option_font.render("MUSIC VOLUME", True, WHITE)
        music_rect = music_label.get_rect(center = (screen_center[0], music_slider.pos[1] - 40))
        screen.blit(music_label, music_rect)

        music_value = option_font.render(f"{int(music_slider.get_value())}", True, WHITE)
        music_value_rect = music_value.get_rect(center=(screen_center[0], music_slider.pos[1] + 40))
        screen.blit(music_value, music_value_rect)

        sfx_lable = option_font.render("SOUND VOLUME", True, WHITE)
        sfx_rect = sfx_lable.get_rect(center = (screen_center[0], sfx_slider.pos[1] - 40))
        screen.blit(sfx_lable, sfx_rect)

        sfx_value = option_font.render(f"{int(sfx_slider.get_value())}", True, WHITE)
        sfx_value_rect = sfx_value.get_rect(center = (screen_center[0], sfx_slider.pos[1] + 40))
        screen.blit(sfx_value, sfx_value_rect)

        back_text = font_small.render("Press ESC to go back", True, "gray")
        back_rect = back_text.get_rect(bottomright=(980, 580))
        screen.blit(back_text, back_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.key.set_repeat(0)
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.key.set_repeat(0)
                    esc_sound.play()
                    return "MENU"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for slider in sliders:
                        if slider.container_rect.collidepoint(mouse_pos):
                            current_slider = slider
                            slider.move_slider_mouse(mouse_pos)

                            value = slider.get_value()
                            current_val = max(0.0, min(1.0, value / 100.0))
                            if slider == music_slider:
                                settings.music_volume = current_val
                            elif slider == sfx_slider:
                                settings.sfx_volume = current_val


            if event.type == pygame.MOUSEMOTION:
                if mouse[0] and current_slider:
                    current_slider.move_slider_mouse(mouse_pos)
                    value = current_slider.get_value()
                    current_val = max(0.0, min(1.0, value / 100.0))
                    if current_slider == music_slider:
                        settings.music_volume = current_val
                    elif current_slider == sfx_slider:
                        settings.sfx_volume = current_val
                        esc_sound.set_volume(settings.sfx_volume)

            if event.type == pygame.KEYDOWN:
                if current_slider:
                    if event.key == pygame.K_RIGHT:
                        current_slider.move_slider_button('right')
                    if event.key == pygame.K_LEFT:
                        current_slider.move_slider_button('left')

                    value = current_slider.get_value()
                    current_val = max(0.0, min(1.0, value / 100.0))
                    if current_slider == music_slider:
                        settings.music_volume = current_val
                    elif current_slider == sfx_slider:
                        settings.sfx_volume = current_val
                        esc_sound.set_volume(settings.sfx_volume)

                if event.key == pygame.K_TAB:
                    if current_slider == music_slider:
                        current_slider = sfx_slider
                    elif current_slider == sfx_slider:
                        current_slider = music_slider



        clock.tick(60)