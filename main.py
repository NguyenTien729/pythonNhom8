import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Undertail')
clock = pygame.time.Clock()
#Background

test_surface = pygame.Surface((400,200))
test_surface.fill('White')
test_surface2 = pygame.Surface((390,190))
test_surface2.fill('Black')
test_surface3 = pygame.Surface((800,400))
test_surface3.fill('Black')
#Player
player_surf = pygame.image.load('char_python/heart.png').convert_alpha()
player_rect = player_surf.get_rect(topleft = (400,370))
#player_gravity = 0
player_speed = 5



#enermy
skull_surf = pygame.image.load('char_python/skull-export.png').convert_alpha()
skull_rect = skull_surf.get_rect(topleft = (100,100))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE and player_rect.bottom >=370:
        #         player_gravity = -10

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

    # Giới hạn trong hộp trắng (200,200,400,200)
    if player_rect.left < 200:
        player_rect.left = 200
    if player_rect.right > 600:
        player_rect.right = 600
    if player_rect.top < 200:
        player_rect.top = 200
    if player_rect.bottom > 400:
        player_rect.bottom = 400



    screen.blit(test_surface3,(0,0)) 
    screen.blit(test_surface,(200,200))    
    screen.blit(test_surface2,(205,205)) 

    #Player
    #player_gravity += 1
    #player_rect.y += player_gravity
    #if player_rect.y>370:player_rect.y = 370
    screen.blit(player_surf,player_rect)

    
    #Enemy
    screen.blit(skull_surf,skull_rect)


    pygame.display.update()
    clock.tick(60)

    

    