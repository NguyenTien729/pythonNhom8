import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,500))
pygame.display.set_caption('Undertail')
clock = pygame.time.Clock()

#font
g_font = pygame.font.Font("font/MonsterFriendBack.otf",22)


#Background
test_surface = pygame.Surface((300,150))
test_surface.fill('White')
test_surface2 = pygame.Surface((290,140))
test_surface2.fill('Black')
mainbackground = pygame.Surface((800,400))
mainbackground.fill('Black')


#Player
player_surf = pygame.image.load('char_python/heart.png').convert_alpha()
player_rect = player_surf.get_rect(topleft = (400,370))
player_speed = 5



#enermy
skull_surf = pygame.image.load('char_python/skull-export.png').convert_alpha()
skull_rect = skull_surf.get_rect(topleft = (100,100))


def draw_health_bar(surface, x, y, current_hp, max_hp, width=100, height=30):
    ratio = current_hp / max_hp
    if ratio < 0: ratio = 0
    pygame.draw.rect(surface, (255,255,0), (x, y, width, height))
    pygame.draw.rect(surface, (255,0,0), (x, y, width * ratio, height))
    #HP text
    hp_text = g_font.render("HP", True, (255,255,255))  
    hp_rect = hp_text.get_rect(midright=(x - 5, y + height // 2))
    surface.blit(hp_text, hp_rect)
    #HP val
    hp_val = g_font.render(f"{current_hp}\{max_hp}", True, (255,255,255))  
    hp_val_rect = hp_val.get_rect(midleft=(x + width + 5, y + height // 2)) 
    surface.blit(hp_val, hp_val_rect)
    

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    #input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed
    if keys[pygame.K_UP]:
        player_rect.y -= player_speed
    if keys[pygame.K_DOWN]:
        player_rect.y += player_speed

    #Khung
    if player_rect.left < 250:
        player_rect.left = 250
    if player_rect.right > 550:
        player_rect.right = 550
    if player_rect.top < 250:
        player_rect.top = 250
    if player_rect.bottom > 400:
        player_rect.bottom = 400


    #background
    screen.blit(mainbackground,(0,0)) 
    screen.blit(test_surface,(250,250))    
    screen.blit(test_surface2,(255,255)) 


    #Vẽ thanh máu
    player_hp = 75   # giả sử còn 75 máu
    max_hp = 100
    draw_health_bar(screen, 315, 420, player_hp, max_hp)


    #Player
    screen.blit(player_surf,player_rect)

    
    #Enemy
    screen.blit(skull_surf,skull_rect)


    pygame.display.update()
    clock.tick(60)

    

    