import pygame
import sys
import json

# Inicializace Pygame
pygame.init()

# Vytvoření okna
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Trvalé ukládání Rectů")

# Pokusíme se načíst uložené pozice při startu programu
try:
    with open('rects.json', 'r') as f:
        rects = json.load(f)
    print("Načteny uložené pozice")
except FileNotFoundError:
    rects = []  # Pokud soubor neexistuje, začneme s prázdným seznamem
    print("Žádné uložené pozice nenalezeny")

# Hlavní smyčka
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Uložíme pozice před ukončením programu
            with open('rects.json', 'w') as f:
                json.dump(rects, f)
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            rects.append([x, y])
            # Uložíme pozice po každém novém obdélníku
            with open('rects.json', 'w') as f:
                json.dump(rects, f)
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:  # Vymazání všech obdélníků
                rects = []
                with open('rects.json', 'w') as f:
                    json.dump(rects, f)
    
    # Vykreslení
    screen.fill((255, 255, 255))
    for x, y in rects:
        pygame.draw.rect(screen, (255, 0, 0), (x, y, 50, 50))
    pygame.display.flip()

pygame.quit()
sys.exit()