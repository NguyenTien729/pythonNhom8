import pygame
import sys
import os
import subprocess

# Tải background trước khi khởi tạo
background = pygame.image.load("graphics/sprites/bones/background3.jpg")

def open_leaderboard(user_id, player_name):
    """Mở leaderboard nhưng có thể quay lại menu"""
    pygame.quit()
    lb_path = os.path.join(os.path.dirname(__file__), "leaderboard.py")
    # Gọi leaderboard và giữ user_id, player_name để khi quay lại không mất
    subprocess.Popen([sys.executable, lb_path, str(user_id), player_name])
    sys.exit()

def run_menu(user_id, player_name):
    """Menu chính sau khi đăng nhập"""
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("Undertale Menu")
    clock = pygame.time.Clock()

    # Font Undertale
    font = pygame.font.Font("font/MonsterFriendBack.otf", 36)
    small_font = pygame.font.Font("font/MonsterFriendBack.otf", 18)

    # Màu sắc
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)

    options = ["START", "LEADERBOARD", "EXIT"]
    selected = 0

    def draw_menu(mouse_pos):
        screen.fill(BLACK)
        screen.blit(background, (0, 0))

        # Tiêu đề
        title = font.render("UNDERTAIL", True, WHITE)
        title_rect = title.get_rect(center=(screen.get_width() // 2, 150))
        screen.blit(title, title_rect)

        # Hiển thị player_name
        name_text = small_font.render(f"PLAYER: {player_name}", True, YELLOW)
        screen.blit(name_text, (20, 20))

        # Nút bấm
        buttons = []
        for i, opt in enumerate(options):
            text_color = RED if i == selected else WHITE
            text = font.render(opt, True, text_color)
            text_rect = text.get_rect(center=(screen.get_width() // 2, 300 + i * 80))
            buttons.append((opt, text_rect))
            # Đổi màu khi hover chuột
            if text_rect.collidepoint(mouse_pos):
                text = font.render(opt, True, RED)
            screen.blit(text, text_rect)

        pygame.display.flip()
        return buttons

    def run_game():
        """Chạy main.py và truyền user_id + player_name"""
        pygame.quit()
        main_path = os.path.join(os.path.dirname(__file__), "main.py")
        subprocess.Popen([sys.executable, main_path, str(user_id), player_name])
        sys.exit()

    # --- Main loop ---
    while True:
        mouse_pos = pygame.mouse.get_pos()
        buttons = draw_menu(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected] == "START":
                        run_game()
                    elif options[selected] == "LEADERBOARD":
                        open_leaderboard(user_id, player_name)
                    elif options[selected] == "EXIT":
                        pygame.quit()
                        sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for opt, rect in buttons:
                    if rect.collidepoint(mouse_pos):
                        if opt == "START":
                            run_game()
                        elif opt == "LEADERBOARD":
                            open_leaderboard(user_id, player_name)
                        elif opt == "EXIT":
                            pygame.quit()
                            sys.exit()

        clock.tick(30)
