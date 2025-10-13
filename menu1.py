import pygame
import sys
import os
import subprocess
from enter_name import get_player_name
def open_leaderboard():
    pygame.quit()
    lb_path = os.path.join(os.path.dirname(__file__), "leaderboard.py")
    subprocess.Popen([sys.executable, lb_path])
    sys.exit()

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Undertale Menu")
clock = pygame.time.Clock()

# Font Undertale
font = pygame.font.Font("font/MonsterFriendBack.otf", 36)

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

options = ["START", "LEADERBOARD", "EXIT"]
selected = 0

def draw_menu(mouse_pos):
    screen.fill(BLACK)

    # === Canh giữa tiêu đề chuẩn ===
    title = font.render("UNDERTAIL", True, WHITE)
    title_rect = title.get_rect(center=(screen.get_width() // 2 + 15, 150))  # dịch nhẹ sang trái
    screen.blit(title, title_rect)

    buttons = []
    for i, opt in enumerate(options):
        text_color = RED if i == selected else WHITE
        text = font.render(opt, True, text_color)
        text_rect = text.get_rect(center=(screen.get_width() // 2, 300 + i * 80))
        buttons.append((opt, text_rect))
        if text_rect.collidepoint(mouse_pos):
            text = font.render(opt, True, RED)
        screen.blit(text, text_rect)

    pygame.display.flip()
    return buttons

def run_game():
    # Hiển thị màn nhập tên
    player_name = get_player_name(screen, font)
    pygame.quit()
    main_path = os.path.join(os.path.dirname(__file__), "main.py")
    subprocess.Popen([sys.executable, main_path, player_name])
    sys.exit()

while True:
    mouse_pos = pygame.mouse.get_pos()
    buttons = draw_menu(mouse_pos)
    
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
                if options[selected] == "START":
                    run_game()
                elif options[selected] == "LEADERBOARD":
                    open_leaderboard()
                elif options[selected] == "EXIT":
                    pygame.quit()
                    sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for opt, rect in buttons:
                if rect.collidepoint(mouse_pos):
                    if opt == "START":
                        run_game()
                    elif opt == "EXIT":
                        pygame.quit()
                        sys.exit()
                    elif opt == "LEADERBOARD":
                        open_leaderboard()

    clock.tick(30)
