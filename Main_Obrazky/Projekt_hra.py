import pygame
import sys
import time

# Inicializace Pygame
pygame.init()

# Nastavení obrazovky
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Menu s Editorem Obrázků")
clock = pygame.time.Clock()
FPS = 60

# Barvy
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
RED = (255, 0, 0)

# Fonty
font = pygame.font.SysFont('Arial', 40)
small_font = pygame.font.SysFont('Arial', 30)
debug_font = pygame.font.Font(None, 36)

# Grid setup
pocet_čtvercu_strana = 5
grid = [[[] for x in range(pocet_čtvercu_strana)] for y in range(pocet_čtvercu_strana)]
cell_size = WIDTH // pocet_čtvercu_strana

# Load and scale images
def load_and_scale_image(path, size):
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)
    except pygame.error:
        print(f"Nelze načíst obrázek: {path}")
        surface = pygame.Surface(size)
        surface.fill(RED)
        return surface

# Images with proper scaling to cell size
obrazky = {
    1: load_and_scale_image("Hlava_hrac.png", (cell_size, cell_size)),
    2: load_and_scale_image("stavebni_block.png", (cell_size, cell_size)),
    3: load_and_scale_image("motor_hotov.png", (cell_size, cell_size)),
    4: load_and_scale_image("pneumatika.png", (cell_size, cell_size))
}

# Image selection
current_image = 1

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, (self.x, self.y, self.width, self.height))
        text_surf = small_font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=(self.x + self.width/2, self.y + self.height/2))
        screen.blit(text_surf, text_rect)
        
    def is_hover(self, pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            self.current_color = self.hover_color
            return True
        self.current_color = self.color
        return False

def create_transparent_screenshot():
    # Vytvoření průhledné surface
    transparent_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    # Vykresli pouze obrázky (bez mřížky a UI)
    for y in range(pocet_čtvercu_strana):
        for x in range(pocet_čtvercu_strana):
            for img_id in grid[y][x]:
                if img_id in obrazky:
                    transparent_surface.blit(obrazky[img_id], (x * cell_size, y * cell_size))
    
    # Uložení průhledného screenshotu
    pygame.image.save(transparent_surface, "transparent_objects.png")
    print("Průhledný screenshot uložen jako transparent_objects.png")

def kliknuti(pos):
    x = pos[0] // cell_size
    y = pos[1] // cell_size
    return x, y

def draw_grid():
    screen.fill(WHITE)
    
    # Draw squares and images
    for y in range(pocet_čtvercu_strana):
        for x in range(pocet_čtvercu_strana):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            
            # Vykresli všechny obrázky v buňce
            for img_id in grid[y][x]:
                if img_id in obrazky:
                    screen.blit(obrazky[img_id], (x * cell_size, y * cell_size))
            
            # Draw grid lines
            pygame.draw.rect(screen, BLACK, rect, 1)
    
    # Zobraz aktuálně vybraný obrázek
    text = debug_font.render(f"Vybraný obrázek: {current_image}", True, BLACK)
    screen.blit(text, (10, 10))
    
    help_text = debug_font.render("Klávesy 1-4: Změna obrázku, P: Screenshot, DEL: Smazat, ESC: Zpět", True, BLACK)
    screen.blit(help_text, (10, HEIGHT - 40))

def main_menu():
    # Vytvoření tlačítek
    start_button = Button("Spustit Hru", WIDTH/2 - 100, 200, 200, 50, WHITE, GRAY)
    options_button = Button("Nastavení", WIDTH/2 - 100, 300, 200, 50, WHITE, GRAY)
    quit_button = Button("Ukončit", WIDTH/2 - 100, 400, 200, 50, WHITE, GRAY)
    
    # Hlavní menu smyčka
    running = True
    while running:
        screen.fill(BLACK)
        
        # Vykreslení nadpisu
        title = font.render("HLAVNÍ MENU", True, RED)
        title_rect = title.get_rect(center=(WIDTH/2, 100))
        screen.blit(title, title_rect)
        
        # Zpracování událostí
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_hover(mouse_pos):
                    game()  # Spustit editor mřížky
                if options_button.is_hover(mouse_pos):
                    options()  # Otevřít nastavení
                if quit_button.is_hover(mouse_pos):
                    pygame.quit()
                    sys.exit()
        
        # Kontrola pohybu myši přes tlačítka
        start_button.is_hover(mouse_pos)
        options_button.is_hover(mouse_pos)
        quit_button.is_hover(mouse_pos)
        
        # Vykreslení tlačítek
        start_button.draw(screen)
        options_button.draw(screen)
        quit_button.draw(screen)
        
        pygame.display.update()

def game():
    global current_image
    
    # Hlavní herní smyčka s mřížkou pro vykreslování obrázků
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = kliknuti(pygame.mouse.get_pos())
                
                if 0 <= x < pocet_čtvercu_strana and 0 <= y < pocet_čtvercu_strana:
                    if event.button == 1:  # Levé tlačítko - přidej obrázek
                        grid[y][x].append(current_image)
                        print(f"Přidán obrázek {current_image} na pozici [{x}, {y}]")
                    elif event.button == 3:  # Pravé tlačítko - odeber poslední obrázek
                        if grid[y][x]:  # Pokud jsou v buňce nějaké obrázky
                            removed = grid[y][x].pop()
                            print(f"Odebrán obrázek {removed} z pozice [{x}, {y}]")
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_1:
                    current_image = 1
                elif event.key == pygame.K_2:
                    current_image = 2
                elif event.key == pygame.K_3:
                    current_image = 3
                elif event.key == pygame.K_4:
                    current_image = 4
                elif event.key == pygame.K_p:  # Screenshot s průhledným pozadím
                    create_transparent_screenshot()
                elif event.key == pygame.K_DELETE:
                    x, y = kliknuti(pygame.mouse.get_pos())
                    if 0 <= x < pocet_čtvercu_strana and 0 <= y < pocet_čtvercu_strana:
                        grid[y][x].clear()
                        print(f"Smazány všechny obrázky na pozici [{x}, {y}]")
        
        draw_grid()
        pygame.display.update()
        clock.tick(FPS)

def options():
    # Menu nastavení
    running = True
    back_button = Button("Zpět", WIDTH/2 - 100, 400, 200, 50, WHITE, GRAY)
    
    while running:
        screen.fill(BLACK)
        
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_hover(mouse_pos):
                    running = False
        
        options_text = font.render("NASTAVENÍ", True, RED)
        text_rect = options_text.get_rect(center=(WIDTH/2, 100))
        screen.blit(options_text, text_rect)
        
        back_button.is_hover(mouse_pos)
        back_button.draw(screen)
        
        pygame.display.update()

# Spuštění menu
if __name__ == "__main__":
    main_menu()