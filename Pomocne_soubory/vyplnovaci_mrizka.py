import pygame
#import sys

# Inicializace Pygame
pygame.init()

# Nastavení okna
WINDOW_SIZE = 800
GRID_SIZE = 40  # Počet čtverců na každé straně
CELL_SIZE = WINDOW_SIZE // GRID_SIZE

# Vytvoření okna
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Vybarvování čtverců")

# Vytvoření mřížky (0 = prázdné, 1 = červené)
grid = [[0 for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

def draw_grid():
    screen.fill(WHITE)
    
    # Vykreslení čtverců
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[y][x] == 1:  # Pokud je čtverec vyplněný
                pygame.draw.rect(screen, RED, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)  # Ohraničení čtverce

def get_clicked_cell(pos):
    x = pos[0] // CELL_SIZE
    y = pos[1] // CELL_SIZE
    return x, y

# Hlavní herní smyčka
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = get_clicked_cell(pygame.mouse.get_pos())
            if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                grid[y][x] = 1  # Vyplnění čtverce
    
    draw_grid()
    pygame.display.flip()

pygame.quit()
sys.exit()