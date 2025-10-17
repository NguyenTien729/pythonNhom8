import pygame
import sys
from game.db.database import Database

def login_ui(screen, clock):
    username = ""
    password = ""
    active_box = None
    message = ""
    mode = "login"
    db = Database()

    # color
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (150, 150, 150)
    YELLOW = (255, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 150, 255)

    pygame.display.set_caption("Login System")

    heart_img = pygame.image.load("graphics/sprites/player/heart.png").convert_alpha()
    background = pygame.image.load("graphics/sprites/bones/background3.jpg")
    font = pygame.font.Font("font/MonsterFriendBack.otf", 24)
    small_font = pygame.font.Font("font/MonsterFriendBack.otf", 18)

    select_sound = pygame.mixer.Sound("sound/sans_battle/snd_select.wav")

    input_boxes = {
        "username": pygame.Rect(250, 180, 300, 50),
        "password": pygame.Rect(250, 260, 300, 50)
    }

    pygame.key.set_repeat(500, 50)

    def draw_text(text, font, color, surface, x, y):
        text_obj = font.render(text, True, color)
        rect = text_obj.get_rect(center=(x, y))
        surface.blit(text_obj, rect)

    def input_box(x, y, w, h, text, active):
        color = YELLOW if active else GRAY
        pygame.draw.rect(screen, color, (x, y, w, h), 2)
        txt_surface = font.render(text, True, WHITE)
        screen.blit(txt_surface, (x + 10, y + 10))

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.key.set_repeat(0)
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_boxes["username"].collidepoint(event.pos):
                    select_sound.play()
                    active_box = "username"
                elif input_boxes["password"].collidepoint(event.pos):
                    select_sound.play()
                    active_box = "password"
                else:
                    active_box = None

                if login_btn.collidepoint(event.pos):
                    mode = "login"
                    user_id = db.login(username, password)
                    select_sound.play()
                    if user_id:
                        pygame.key.set_repeat(0)
                        player_name = db.get_player_name(user_id)
                        return user_id, player_name
                    else:
                        message = "Invalid login!"

                elif register_btn.collidepoint(event.pos):
                    mode = "register"
                    select_sound.play()
                    if username.strip() == "" or password.strip() == "":
                        message = "Please fill all fields!"
                    else:
                        success = db.register_user(username, password)
                        if success:
                            message = "Registered successfully!"
                        else:
                            message = "Username already exists!"

            elif event.type == pygame.KEYDOWN:
                if active_box == "username":
                    if event.key == pygame.K_BACKSPACE:  #xóa
                        username = username[:-1]
                    else:
                        if len(username) < 12 and event.unicode.isprintable():
                            username += event.unicode
                elif active_box == "password":
                    if event.key == pygame.K_BACKSPACE:  #xóa
                        password = password[:-1]
                    elif len(password) < 12 and event.unicode.isprintable():
                        password += event.unicode

        clock.tick(30)