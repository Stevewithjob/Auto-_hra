import pygame
import sys
import os  # Přidáme pro mazání souborů

# Inicializace Pygame
pygame.init()

# Vytvoření okna
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Ukládání obrázku")

# Načteme uložený obrázek při startu (pokud existuje)
try:
    saved_image = pygame.image.load('saved_screen.png')
    saved_image = pygame.transform.scale(saved_image,(200, 200))
    screen.blit(saved_image, (0, 0))
    print("Načten uložený obrázek")
except:
    screen.fill((255, 255, 255))  # Bílé pozadí pokud není uložený obrázek
    print("Žádný uložený obrázek nenalezen")

# Hlavní smyčka
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            pygame.draw.rect(screen, (255, 0, 0), (x, y, 50, 50))
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:  # Vymazání obrazovky
                screen.fill((255, 255, 255))
            elif event.key == pygame.K_t:  # Uložení obrázku
                pygame.image.save(screen, 'saved_screen.png')
                print("Obrázek byl uložen")
            elif event.key == pygame.K_r:  # Smazání uloženého obrázku
                try:
                    os.remove('saved_screen.png')
                    print("Uložený obrázek byl smazán")
                except:
                    print("Žádný uložený obrázek k smazání")
    
    pygame.display.flip()

pygame.quit()
sys.exit()