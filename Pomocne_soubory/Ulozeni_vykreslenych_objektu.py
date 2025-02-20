import pygame
import sys

pygame.init()
window_size = 800
okno = pygame.display.set_mode((window_size,window_size))

clock = pygame.time.Clock()

pocet_čtvercu_strana = 5
grid = [[[] for x in range(pocet_čtvercu_strana)] for y in range(pocet_čtvercu_strana)]
cell_size = window_size // pocet_čtvercu_strana

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)


def create_test_image():
    # Vytvoření průhledné surface
    surface = pygame.Surface((200, 200), pygame.SRCALPHA)
    
   
    # Draw squares and images
    for y in range(pocet_čtvercu_strana):
        for x in range(pocet_čtvercu_strana):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            
            # Vykresli všechny obrázky v buňce
            for img_id in grid[y][x]:
                if img_id in obrazky:
                    okno.blit(obrazky[img_id], (x * cell_size, y * cell_size))
                
            # Draw grid lines
            pygame.draw.rect(okno, black, rect, 1)
    # Uložení obrázku
    pygame.image.save(surface, "test_transparent.png")
    return surface

test_surface = create_test_image()
    
# Pozice pro vykreslení
pos_x = 300
pos_y = 200
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
                
        # Vykreslení šachovnicového pozadí pro demonstraci průhlednosti
    okno.fill((255, 255, 255))  # Bílé pozadí
        
        # Vykreslení našeho průhledného obrázku
    okno.blit(test_surface, (pos_x, pos_y))
        
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

