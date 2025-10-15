import pygame
import sys
from database import Database
from enter_name import get_player_name
from menu1 import run_menu
pygame.init()

#color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 150, 255)

screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("Login System")

heart_img = pygame.image.load("graphics/sprites/player/heart.png").convert_alpha()
background = pygame.image.load("graphics/sprites/bones/background3.jpg")
font = pygame.font.Font("font/MonsterFriendBack.otf", 24)
small_font = pygame.font.Font("font/MonsterFriendBack.otf", 18)
clock = pygame.time.Clock()

db = Database()


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, rect)

def input_box(x, y, w, h, text, active):
    color = YELLOW if active else GRAY
    pygame.draw.rect(screen, color, (x, y, w, h), 2)
    txt_surface = font.render(text, True, WHITE)
    screen.blit(txt_surface, (x + 10, y + 10))

def login_ui():
    username = ""
    password = ""
    active_box = None
    message = ""
    mode = "login"  # hoặc "register"

    input_boxes = {
        "username": pygame.Rect(250, 180, 300, 50),
        "password": pygame.Rect(250, 260, 300, 50)
    }

    while True:
        screen.fill(BLACK)
        bg_rect = background.get_rect(topleft=(0,50))
        screen.blit(background, bg_rect)
        draw_text(f"{mode.upper()}", font, RED, screen, 400, 100)

        # Vẽ input box
        input_box(input_boxes["username"].x, input_boxes["username"].y, 300, 50, username, active_box == "username")
        draw_text("Username", small_font, WHITE, screen, 150, 205)

        input_box(input_boxes["password"].x, input_boxes["password"].y, 300, 50, "*" * len(password), active_box == "password")
        draw_text("Password", small_font, WHITE, screen, 150, 285)

        # Nút bấm
        login_btn = pygame.Rect(250, 340, 120, 45)
        register_btn = pygame.Rect(400, 340, 150, 45)
        pygame.draw.rect(screen, RED if mode == "login" else GRAY, login_btn)
        pygame.draw.rect(screen, RED if mode == "register" else GRAY, register_btn)

        draw_text("LOGIN", small_font, WHITE, screen, login_btn.centerx, login_btn.centery)
        draw_text("REGISTER", small_font, WHITE, screen, register_btn.centerx, register_btn.centery)

        #!!!!!!
        draw_text(message, small_font, YELLOW, screen, 400, 420)
        #trangtri
        heart_rect = heart_img.get_rect(topright=(screen.get_width() - 20, 20))
        screen.blit(heart_img, heart_rect)

        
        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_boxes["username"].collidepoint(event.pos):
                    active_box = "username"
                elif input_boxes["password"].collidepoint(event.pos):
                    active_box = "password"
                elif login_btn.collidepoint(event.pos):
                    mode = "login"
                    try:
                        user_id = db.login(username, password)
                        if user_id:
                            return user_id, username
                        else:
                            message = "Invalid login!"
                    except Exception as e:
                        message = f"{e}"
                elif register_btn.collidepoint(event.pos):
                    mode = "register"
                    if username.strip() == "" or password.strip() == "":
                        message = "Please fill all fields!"
                    else:
                        success = db.register_user(username, password)
                        if success:
                            message = "Registered successfully!"
                        else:
                            message = "Username already exists!"
                else:
                    active_box = None

            elif event.type == pygame.KEYDOWN:
                if active_box == "username":
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        if len(username) < 15 and event.unicode.isprintable():
                            username += event.unicode
                elif active_box == "password":
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        if len(password) < 15 and event.unicode.isprintable():
                            password += event.unicode

if __name__ == "__main__":
    user_id, username = login_ui()
    player_name = db.get_player_name(user_id)
    if player_name:
        #nếu có tên sang menu
        run_menu(user_id, player_name)
    else:
        #k có tên sang entername
        get_player_name(screen, font, db, user_id, run_menu)