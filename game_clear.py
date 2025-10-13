import pygame
import sys
import os
import subprocess

def open_leaderboard():
    pygame.quit()
    lb_path = os.path.join(os.path.dirname(__file__), "leaderboard.py")
    subprocess.Popen([sys.executable, lb_path])
    sys.exit()

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Game Clear")
clock = pygame.time.Clock()

# Font Undertale
title_font = pygame.font.Font("font/MonsterFriendBack.otf", 80)
press_font = pygame.font.Font("font/MonsterFriendBack.otf", 20)

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

running = True
while running:
    screen.fill(BLACK)

    # === Tiêu đề GAME CLEAR ===
    title_text = title_font.render("YOU WIN!", True, YELLOW)
    title_rect = title_text.get_rect(center=(500, 250))
    screen.blit(title_text, title_rect)

    # === Dòng hướng dẫn nhỏ ở góc phải ===
    press_text = press_font.render("PRESS ANY KEY TO CONTINUE", True, (200, 200, 200))
    press_rect = press_text.get_rect(bottomright=(980, 580))
    screen.blit(press_text, press_rect)

    pygame.display.update()
    clock.tick(60)

    # === Sự kiện ===
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            open_leaderboard()
