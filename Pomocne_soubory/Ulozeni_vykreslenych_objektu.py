import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

def create_test_image():
    # Vytvoření průhledné surface
    surface = pygame.Surface((200, 200), pygame.SRCALPHA)
    
    # Nakreslení červeného kruhu s průhledným pozadím
    pygame.draw.circle(surface, (255, 0, 0, 255), (100, 100), 50)  # Plně neprůhledný červený kruh
    # První parametr je surface, druhý je barva (R,G,B,A), třetí je obdélník (x,y,šířka,výška)
    pygame.draw.ellipse(surface, (222, 200, 225, 255), (50, 40, 100, 40))
    # Uložení obrázku
    pygame.image.save(surface, "test_transparent.png")
    return surface

def main():
    running = True
    
    # Vytvoření testovacího obrázku
    test_surface = create_test_image()
    
    # Pozice pro vykreslení
    pos_x = 300
    pos_y = 200
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Vykreslení šachovnicového pozadí pro demonstraci průhlednosti
        screen.fill((255, 255, 255))  # Bílé pozadí
        
        # Vytvoření šachovnice
        for x in range(0, 800, 50):
            for y in range(0, 600, 50):
                if (x + y) // 50 % 2 == 0:
                    pygame.draw.rect(screen, (200, 200, 200), (x, y, 50, 50))
        
        # Vykreslení našeho průhledného obrázku
        screen.blit(test_surface, (pos_x, pos_y))
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()