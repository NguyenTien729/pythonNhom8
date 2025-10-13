import pygame
import sys
import json
import os

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Leaderboard")
clock = pygame.time.Clock()

# Font Undertale
font = pygame.font.Font("font/MonsterFriendBack.otf", 32)
font_small = pygame.font.Font("font/MonsterFriendBack.otf", 20)


# Màu sắc
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)


# ==============================
# HÀM TẢI DỮ LIỆU BẢNG XẾP HẠNG
# ==============================
def load_leaderboard():
    if os.path.exists("leaderboard.json"):
        with open("leaderboard.json", "r") as f:
            return json.load(f)
    return []


# ==============================
# HÀM VẼ GIAO DIỆN BẢNG XẾP HẠNG
# ==============================
def draw_leaderboard(data):
    screen.fill(BLACK)

    # Tiêu đề
    title = font.render("LEADERBOARD", True, YELLOW)
    title_rect = title.get_rect(center=(500, 100))
    screen.blit(title, title_rect)

    # Hiển thị danh sách điểm
    if not data:
        empty_text = font.render("No scores yet!", True, WHITE)
        empty_rect = empty_text.get_rect(center=(500, 250))
        screen.blit(empty_text, empty_rect)
    else:
        for i, entry in enumerate(data):
            name = entry["name"]
            score = entry["score"]
            text = font.render(f"{i+1}. {name} - {score}", True, WHITE)
            text_rect = text.get_rect(center=(500, 200 + i * 40))  # căn giữa
            screen.blit(text, text_rect)

    # Gợi ý quay lại (đặt góc dưới bên phải)
    back_text = font_small.render("Press ESC to go back", True, GRAY)
    back_rect = back_text.get_rect(bottomright=(980, 580))  # góc dưới phải, cách viền 20px
    screen.blit(back_text, back_rect)

    pygame.display.flip()


# ==============================
# HÀM CHÍNH
# ==============================
def main():
    data = load_leaderboard()

    while True:
        draw_leaderboard(data)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        clock.tick(30)


# ==============================
# CHẠY FILE TRỰC TIẾP
# ==============================
if __name__ == "__main__":
    main()
