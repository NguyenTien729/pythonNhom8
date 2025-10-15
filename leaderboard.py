import pygame
import sys
import subprocess
import os
from database import Database  

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Leaderboard")
clock = pygame.time.Clock()
font = pygame.font.Font("font/MonsterFriendBack.otf", 32)
font_small = pygame.font.Font("font/MonsterFriendBack.otf", 20)

# Màu sắc
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)

def load_leaderboard():
    db = Database()
    try:
        # Lấy top 5 người có điểm cao nhất
        query = """
            SELECT u.player_name, s.score
            FROM scores s
            JOIN users u ON s.user_id = u.id
            ORDER BY s.score DESC
            LIMIT 5
        """
        db.cursor.execute(query)
        rows = db.cursor.fetchall()
        leaderboard = [{"name": row[0], "score": row[1]} for row in rows]
        return leaderboard
    except Exception as e:
        print("Lỗi khi tải leaderboard:", e)
        return []

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
            text_rect = text.get_rect(center=(500, 200 + i * 50))
            screen.blit(text, text_rect)

    # Gợi ý quay lại (ESC)
    back_text = font_small.render("Press ESC to go back", True, GRAY)
    back_rect = back_text.get_rect(bottomright=(980, 580))
    screen.blit(back_text, back_rect)

    pygame.display.flip()

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
                    menu_path = os.path.join(os.path.dirname(__file__), "menu1.py")
                    subprocess.Popen([sys.executable, menu_path])
                    pygame.display.quit()
                    return

        clock.tick(30)

if __name__ == "__main__":
    main()
