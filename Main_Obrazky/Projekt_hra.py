import pygame
import sys
import time
pygame.init()

okno = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Načtení_Obrázků")

clock = pygame.time.Clock()
FPS = 60

#obrázky
hlava = pygame.image.load("Hlava_hrac.png")
hlava = pygame.transform.scale(hlava, (250,250))

block = pygame.image.load("stavebni_block.png")
block = pygame.transform.scale(block, (250,250))
                               
motor = pygame.image.load("motor_hotov.png")
motor = pygame.transform.scale(motor, (250,200))

pneumatika = pygame.image.load("pneumatika.png")
pneumatika = pygame.transform.scale(pneumatika, (250,250))

while True:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    okno.fill((255, 255, 255))
    okno.blit(hlava, (250,0))
    okno.blit(block,(250,270))
    okno.blit(motor,(250,540))
    okno.blit(pneumatika, (540, 250))
    
    pygame.display.update()
    clock.tick(60)