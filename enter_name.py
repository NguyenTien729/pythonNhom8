import pygame
import sys

def get_player_name(screen, font, db, user_id, go_to_menu1):
    clock = pygame.time.Clock()
    name = ""
    input_box = pygame.Rect(350, 250, 300, 50)
    active = True
    screen_width, screen_height = screen.get_size()

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name.strip() != "": # nếu không có tên thì gọi nhập tên
                        db.update_player_name(user_id, name.strip())
                        go_to_menu1(user_id, name.strip())
                        return  
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 15 and event.unicode.isprintable():
                        name += event.unicode

        # Giao diện
        screen.fill((0, 0, 0))
        title_text = font.render("ENTER YOUR NAME:", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen_width // 2, 180))
        screen.blit(title_text, title_rect)

        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
        name_text = font.render(name, True, (255, 255, 0))
        name_rect = name_text.get_rect(center=input_box.center)
        screen.blit(name_text, name_rect)

        hint_text = font.render("(Press ENTER to continue)", True, (150, 150, 150))
        hint_rect = hint_text.get_rect(center=(screen_width // 2, input_box.bottom + 30))
        screen.blit(hint_text, hint_rect)

        pygame.display.flip()
        clock.tick(30)
