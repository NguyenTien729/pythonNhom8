import pygame
from sys import exit

from entities.blaster import MultiBlaster, GasterBlaster

pygame.init()
screen_width = 800
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Undertail')
clock = pygame.time.Clock()
is_active = True

# font
g_font = pygame.font.Font("font/MonsterFriendBack.otf", 22)

# Background
boxlen,boxwidth = 150,150
mainbackground = pygame.Surface((800, 400))
mainbackground.fill('Black')

# Player
player_surf = pygame.image.load('graphics/Sprites/player/heart.png').convert_alpha()
player_rect = player_surf.get_rect(topleft=(400, 370))
player_hit = pygame.image.load('graphics/Sprites/player/heart_hit1.png').convert_alpha()
player_speed = 5

# enermy
skull_surf = pygame.image.load('graphics/Sprites/blasters/beam.png').convert_alpha()
skull_rect = skull_surf.get_rect(topleft=(100, 100))

bone_surf1 = pygame.image.load('graphics/Sprites/bones/bone.png').convert_alpha()
bone_rect1 = bone_surf1.get_rect(topleft=(800, 300))

bone_speed = 2

player_hp = 100
max_hp = 100
last_hit_time = 0
immunity_dur = 2000

#lv1 blaster
blasters = MultiBlaster()


def draw_health_bar(surface, x, y, current_hp, max_hp, width=100, height=30):
    ratio = current_hp / max_hp
    if ratio < 0: ratio = 0
    box_rect = pygame.Rect(0, 0, 800, 500)
    pygame.draw.rect(surface, (0,0,0), box_rect)  
    pygame.draw.rect(surface, (255, 255, 0), (x, y, width, height))
    pygame.draw.rect(surface, (255, 0, 0), (x, y, width * ratio, height))
    # HP text
    hp_text = g_font.render("HP", True, (255, 255, 255))
    hp_rect = hp_text.get_rect(midright=(x - 5, y + height // 2))
    surface.blit(hp_text, hp_rect)
    #HP value
    hp_val = g_font.render(f"{current_hp}/{max_hp}", True, (255, 255, 255))
    hp_val_rect = hp_val.get_rect(midleft=(x + width + 5, y + height // 2))
    surface.blit(hp_val, hp_val_rect)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_UP:
        #        blaster = blasters.create_blaster(-100, -100, 150, 325, -123, start_angle = 0)
        #     if event.key == pygame.K_DOWN:
        #        blaster = blasters.create_blaster(900, -100, 550, 150, 32, start_angle = 0)
        #     if event.key == pygame.K_RIGHT:
        #         blaster = blasters.create_blaster(900, -100, 650, 325, 47, start_angle = 0)
        #     if event.key == pygame.K_LEFT:
        #         blaster = blasters.create_blaster(-100, 600, 150, 325, -146, start_angle = 0)
            

    # input
    if is_active:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed
        if keys[pygame.K_UP]:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN]:
            player_rect.y += player_speed

        

        # Vẽ thanh máu
        draw_health_bar(screen, 315, 420, player_hp, max_hp)

        box = pygame.Surface((boxlen, boxwidth))
        box.fill('White')
        box2 = pygame.Surface((boxlen-10, boxwidth-10))
        box2.fill('Black')
        # background
        screen.blit(mainbackground, (0, 0))
        screen.blit(box, (((800-boxlen)//2), (400-boxwidth)))
        screen.blit(box2, (((800-boxlen)//2)+5, (400-boxwidth)+5))
        
        # Khung
        if player_rect.left < ((800-boxlen)//2)+5:
            player_rect.left = ((800-boxlen)//2)+5
        if player_rect.right > ((800-boxlen)//2)+boxlen-5:
            player_rect.right = ((800-boxlen)//2)+boxlen-5
        if player_rect.top < (400-boxwidth)+5:
            player_rect.top = (400-boxwidth)+5
        if player_rect.bottom > 395:
            player_rect.bottom = 395

        # Enemy
        screen.blit(skull_surf, skull_rect)

        screen.blit(bone_surf1, bone_rect1)
        bone_rect1.x -= bone_speed
        if bone_rect1.right < 0:
            bone_rect1.left = 800
            bone_rect1.y = 250
        

        # Player
        screen.blit(player_surf, player_rect)

        cur_time = pygame.time.get_ticks()
        if bone_rect1.colliderect(player_rect):
                if cur_time - last_hit_time > immunity_dur:
                    player_hp -= 5
                    last_hit_time = cur_time
        if (cur_time - last_hit_time) < immunity_dur:
            #nhấp nháy lúc immunity
            if (cur_time // 100) % 2 == 0:   
                screen.blit(player_hit, player_rect)
            else:
                screen.blit(player_surf, player_rect)
        else:
            screen.blit(player_surf, player_rect)

        
                
        for blaster in blasters.blasters:
            if blaster.beam and blaster.beam.is_active:
                beam_img = blaster.beam.sprite.image
                beam_rect = beam_img.get_rect(center=(blaster.beam.abs_x, blaster.beam.abs_y))

                # Tạo mask từ hình ảnh beam và player
                beam_mask = pygame.mask.from_surface(beam_img)
                player_mask = pygame.mask.from_surface(player_surf)

                offset = (player_rect.x - beam_rect.x, player_rect.y - beam_rect.y)

                if beam_mask.overlap(player_mask, offset):
                    if cur_time - last_hit_time > immunity_dur:
                        player_hp -= 10
                        last_hit_time = cur_time


        
    else:
        screen.fill("Red")

    blasters.update()
    blasters.draw(screen)

    pygame.display.update()
    clock.tick(60)