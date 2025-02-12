import pygame
import sys
import time

pygame.init()

# Window setup
window_size = 800
okno = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption("Načtení_Obrázků")
clock = pygame.time.Clock()
FPS = 60

# Font pro debugování
font = pygame.font.Font(None, 36)

# Grid setup - každá buňka je nyní seznam
pocet_čtvercu_strana = 5
grid = [[[] for x in range(pocet_čtvercu_strana)] for y in range(pocet_čtvercu_strana)]
cell_size = window_size // pocet_čtvercu_strana

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Load and scale images
def load_and_scale_image(path, size):
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)
    except pygame.error:
        print(f"Nelze načíst obrázek: {path}")
        surface = pygame.Surface(size)
        surface.fill(red)
        return surface

# Images with proper scaling to cell size
obrazky = {
    1: load_and_scale_image("Hlava_hrac.png", (cell_size, cell_size)),
    2: load_and_scale_image("stavebni_block.png", (cell_size, cell_size)),
    3: load_and_scale_image("motor_hotov.png", (cell_size, cell_size)),
    4: load_and_scale_image("pneumatika.png", (cell_size, cell_size))
}

# Image selection
current_image = 1  # 1: hlava, 2: block, 3: motor, 4: pneumatika

def draw_grid():
    okno.fill(white)
    
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
    
    # Zobraz aktuálně vybraný obrázek
    text = font.render(f"Vybraný obrázek: {current_image}", True, black)
    okno.blit(text, (10, 10))

def kliknuti(pos):
    x = pos[0] // cell_size
    y = pos[1] // cell_size
    return x, y

# Main game loop
while True:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        elif udalost.type == pygame.MOUSEBUTTONDOWN:
            x, y = kliknuti(pygame.mouse.get_pos())
            if 0 <= x < pocet_čtvercu_strana and 0 <= y < pocet_čtvercu_strana:
                if udalost.button == 1:  # Levé tlačítko - přidej obrázek
                    grid[y][x].append(current_image)
                    print(f"Přidán obrázek {current_image} na pozici [{x}, {y}]")
                elif udalost.button == 3:  # Pravé tlačítko - odeber poslední obrázek
                    if grid[y][x]:  # Pokud jsou v buňce nějaké obrázky
                        removed = grid[y][x].pop()
                        print(f"Odebrán obrázek {removed} z pozice [{x}, {y}]")
        
        elif udalost.type == pygame.KEYDOWN:
            if udalost.key == pygame.K_1:
                current_image = 1
            elif udalost.key == pygame.K_2:
                current_image = 2
            elif udalost.key == pygame.K_3:
                current_image = 3
            elif udalost.key == pygame.K_4:
                current_image = 4
                
            elif udalost.key == pygame.K_DELETE:  # Přidáno mazání všech obrázků v buňce
                x, y = kliknuti(pygame.mouse.get_pos())
                if 0 <= x < pocet_čtvercu_strana and 0 <= y < pocet_čtvercu_strana:
                    grid[y][x].clear()
                    print(f"Smazány všechny obrázky na pozici [{x}, {y}]")
    
    draw_grid()
    pygame.display.update()
    clock.tick(FPS)