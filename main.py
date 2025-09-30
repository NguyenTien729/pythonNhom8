import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,500))
pygame.display.set_caption('Undertail')
clock = pygame.time.Clock()
game_active = True

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
player_surf = pygame.image.load('graphic/heart.png').convert_alpha()
player_rect = player_surf.get_rect(topleft = (400,370))
player_hit = pygame.image.load('graphic/heart_hit1.png').convert_alpha()
player_speed = 5



#enermy
skull_surf = pygame.image.load('graphic/beam4.png').convert_alpha()
skull_rect = skull_surf.get_rect(topleft = (100,100))

bone_surf = pygame.image.load('graphic/bone.png').convert_alpha()
bone_rect = bone_surf.get_rect(topleft = (200,200))
bone_speed = 5

player_hp = 100   
max_hp = 100
last_hit_time = 0
immunity_dur = 2000
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
    box_width, box_height = 150, 40   # kích thước khung vuông
    box_x = x + width + 10            # đặt khung ngay sau thanh máu
    box_y = y + height//2 - box_height//2  # canh giữa theo chiều dọc
    box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
    pygame.draw.rect(surface, (0,0,0), box_rect)  
    hp_val = g_font.render(f"{current_hp}/{max_hp}", True, (255,255,255))  
    hp_val_rect = hp_val.get_rect(midleft=(x + width + 5, y + height // 2)) 
    surface.blit(hp_val, hp_val_rect)
    

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if game_active:
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
        draw_health_bar(screen, 315, 420, player_hp, max_hp)

    
        #Enemy
        screen.blit(skull_surf,skull_rect)
        screen.blit(bone_surf,bone_rect)

        bone_rect.x -= bone_speed
        if bone_rect.right<0:
            bone_rect.left=800
            bone_rect.y = 250
            
        #Player
        cur_time = pygame.time.get_ticks()
        if bone_rect.colliderect(player_rect):
            if cur_time - last_hit_time > immunity_dur:
                player_hp -= 5
                last_hit_time = cur_time
        if (cur_time - last_hit_time) < immunity_dur:
        #nhấp nháy lúc immunity
            if (cur_time // 200) % 2 == 0:   
                screen.blit(player_hit, player_rect)
            else:
                screen.blit(player_surf, player_rect)
        else:
            screen.blit(player_surf, player_rect)

        # if player_hp == 95:
        #     game_active = False
        
    else:
        screen.fill('Red')
        
    pygame.display.update()
    clock.tick(60)

    

    