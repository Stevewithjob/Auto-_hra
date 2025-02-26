import pygame
import time

pygame.init()

screen = pygame.display.set_mode((1600, 800))

pygame.display.set_caption("Co to je :D")

screen_width = 1600
screen_height = 800
down_border = 550

is_jumping = False
jump_count = 10

player = pygame.Rect((750, 320, 250, 250))
auto = pygame.image.load("transparent_objects.png")
auto = pygame.transform.scale(auto, (600, 400))

auto_left = pygame.transform.flip(auto, True, False)

current_player_img = auto

clock = pygame.time.Clock()

pozadi = pygame.image.load(r"G:\Thonny\Pygame\obrázky\Pozadi_V2.png")
pozadi = pygame.transform.scale(pozadi, (1600, 800))

FPS = 60

def jump():
    player.move_ip((0, -5))

run = True
while run:
    
    clock.tick(FPS)
     
    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        player.move_ip(-10, 0)
        current_player_img = auto_left
        
    elif key[pygame.K_d] == True:
        player.move_ip(10, 0)
        current_player_img = auto
        
    if not is_jumping:
        if key[pygame.K_SPACE]:
            is_jumping = True
        
    if is_jumping:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            player.y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jumping = False
            jump_count = 10
        
    
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
                
    screen.blit(pozadi, (0, 0))
    
    screen.blit(current_player_img, player)
    
    player.x = max(0, min(player.x, screen_width - player.width))
    player.y = max(0, min(player.y, down_border - player.height))
    
    pygame.display.update()
            
pygame.quit()