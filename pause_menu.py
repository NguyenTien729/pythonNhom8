import pygame
import sys
import os
import subprocess

def pause_menu(screen):
    pygame.mixer.pause()  # Tạm dừng nhạc (nếu có)
    paused = True

    # Font Undertale
    title_font = pygame.font.Font("font/MonsterFriendBack.otf", 48)
    option_font = pygame.font.Font("font/MonsterFriendBack.otf", 28)

    # Danh sách nút
    options = ["RESUME", "BACK TO MENU", "QUIT"]
    selected = 0

    clock = pygame.time.Clock()

    while paused:
        screen.fill((0, 0, 0))

        # Tiêu đề “PAUSED”
        title_surf = title_font.render("PAUSED", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(500, 180))
        screen.blit(title_surf, title_rect)

        # Các lựa chọn
        for i, text in enumerate(options):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            surf = option_font.render(text, True, color)
            rect = surf.get_rect(center=(500, 280 + i * 60))
            screen.blit(surf, rect)

        pygame.display.update()
        clock.tick(30)

        # Xử lý sự kiện
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
                    choice = options[selected]
                    if choice == "RESUME":
                        pygame.mixer.unpause()
                        return "resume"
                    elif choice == "BACK TO MENU":
                        pygame.mixer.unpause()
                        return "menu"
                    elif choice == "QUIT":
                        pygame.quit()
                        sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for i, text in enumerate(options):
                    rect = pygame.Rect(400, 260 + i * 60, 200, 40)
                    if rect.collidepoint(mouse_pos):
                        choice = options[i]
                        if choice == "RESUME":
                            pygame.mixer.unpause()
                            return "resume"
                        elif choice == "BACK TO MENU":
                            pygame.mixer.unpause()
                            return "menu"
                        elif choice == "QUIT":
                            pygame.quit()
                            sys.exit()
