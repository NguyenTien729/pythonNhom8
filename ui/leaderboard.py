import pygame
import sys
from game.db.database import Database

def leaderboard_main(screen, clock, settings):
    pygame.display.set_caption("Leaderboard")
    font = pygame.font.Font("font/MonsterFriendBack.otf", 32)
    font_small = pygame.font.Font("font/MonsterFriendBack.otf", 20)

    esc_sound = pygame.mixer.Sound("sound/sans_battle/snd_select.wav")

    # Màu sắc
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    GRAY = (150, 150, 150)

    data = []
    try:
        db = Database()
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
        data = [{"name": row[0], "score": row[1]} for row in rows]
    except Exception as e:
        print("Lỗi khi tải leaderboard:", e)

    while True:
        esc_sound.set_volume(settings.sfx_volume)

        screen.fill(BLACK)

        # Tiêu đề
        title = font.render("LEADERBOARD", True, YELLOW)
        title_rect = title.get_rect(center=(500, 100))
        screen.blit(title, title_rect)

        if not data:
            empty_text = font.render("No scores yet!", True, WHITE)
            empty_rect = empty_text.get_rect(center=(500, 250))
            screen.blit(empty_text, empty_rect)
        else:
            for i, entry in enumerate(data):
                name = entry["name"]
                score = entry["score"]
                text = font.render(f"{i + 1}. {name} - {score}", True, WHITE)
                text_rect = text.get_rect(center=(500, 200 + i * 50))
                screen.blit(text, text_rect)

        back_text = font_small.render("Press ESC to go back", True, GRAY)
        back_rect = back_text.get_rect(bottomright=(980, 580))
        screen.blit(back_text, back_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    esc_sound.play()
                    return "MENU"

        clock.tick(30)