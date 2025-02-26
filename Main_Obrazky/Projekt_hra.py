import pygame
import sys

# Inicializace Pygame
pygame.init()

# Nastavení obrazovky
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HELL YEAHHH")
clock = pygame.time.Clock()
FPS = 60

# Barvy
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 100, 255)
DARK_GRAY = (98, 98, 98)
LIGHT_BLUE = (64, 199, 238)

# Fonty
font = pygame.font.SysFont('Arial', 40)
small_font = pygame.font.SysFont('Arial', 30)
debug_font = pygame.font.Font(None, 36)

#písničky
pisnicky = ["Bad_piggies_theme.mp3", "SIGMA-BOY-PHONK-REMIX-.mp3"]
aktualni_pisnicka = 1 
is_playing = True 

pygame.mixer.music.load(pisnicky[aktualni_pisnicka])
pygame.mixer.music.play(-1)

# Grid setup
pocet_čtvercu_strana = 5
grid = [[[] for x in range(pocet_čtvercu_strana)] for y in range(pocet_čtvercu_strana)]
cell_size = WIDTH // pocet_čtvercu_strana

# Omezení počtu obrázků
pocet_obrazku = {1: 0, 2: 0, 3: 0, 4: 0}
max_pocet_obrazku = {1: 1, 2: 5, 3: 1, 4: 2}

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

#Obrázky s poupravením
obrazky = {
    1: load_and_scale_image("Hlava_hrac.png", (cell_size, cell_size)),
    2: load_and_scale_image("stavebni_block.png", (cell_size, cell_size)),
    3: load_and_scale_image("motor_hotov.png", (cell_size, cell_size)),
    4: load_and_scale_image("pneumatika.png", (cell_size, cell_size))
}

# Image selection
current_image = 1

závodní_plocha = load_and_scale_image("Závodní plocha.jpg", (5000,800))
závodní_plocha_x = 0
závodní_plocha_y = 0

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
    
    # Zobrazit počet zbývajících obrázků
    for i in range(1, 5):
        count_text = debug_font.render(f"Obrázek {i}: {pocet_obrazku[i]}/{max_pocet_obrazku[i]}", True, BLACK)
        screen.blit(count_text, (10, 40 + (i - 1) * 30))
    
    help_text = debug_font.render("Klávesy 1-4: Změna obrázku, DEL: Smazat, ESC: Zpět", True, BLACK)
    screen.blit(help_text, (10, HEIGHT - 40))

def main_menu():
    # Vytvoření tlačítek
    start_button = Button("Spustit Hru", WIDTH/2 - 100, 200, 200, 50, WHITE, GRAY)
    options_button = Button("Nastavení", WIDTH/2 - 100, 300, 200, 50, WHITE, GRAY)
    quit_button = Button("Ukončit", WIDTH/2 - 100, 400, 200, 50, WHITE, GRAY)
    
    # Hlavní menu smyčka
    running = True
    while running:
        screen.fill(LIGHT_BLUE)
        
        # Vykreslení nadpisu
        title = font.render("HLAVNÍ MENU", True, DARK_GRAY)
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

def race_screen():
    # Obrazovka pro závodění
    global závodní_plocha_x,závodní_plocha_y
    running = True
    back_button = Button("Zpět do Editoru", WIDTH/2 - 150, HEIGHT - 100, 300, 50, WHITE, GRAY)
    
    while running:
        screen.fill(BLUE)  # Modrá barva pozadí pro závodní obrazovku
        screen.blit(závodní_plocha, (závodní_plocha_x, závodní_plocha_y))
        
        key = pygame.key.get_pressed()
        
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
                    
            if key[pygame.K_RIGHT] == True:
                závodní_plocha_x -= 4
        
        
        # Nadpis závodní obrazovky
        race_title = font.render("ZÁVODNÍ PLOCHA", True, WHITE)
        title_rect = race_title.get_rect(center=(WIDTH/2, 100))
        screen.blit(race_title, title_rect)
        
        # Kontrola tlačítka
        back_button.is_hover(mouse_pos)
        back_button.draw(screen)
        
        pygame.display.update()
        clock.tick(FPS)

def game():
    global current_image, pocet_obrazku
    
    # Reset počítadla obrázků při vstupu do hry
    pocet_obrazku = {1: 0, 2: 0, 3: 0, 4: 0}
    
    # Vytvoření tlačítka Závodit
    race_button = Button("ZÁVODIT", WIDTH - 150, HEIGHT - 100, 140, 50, GREEN, GRAY)
    
    # Hlavní herní smyčka s mřížkou pro vykreslování obrázků
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Pozice myši při kliknutí
                mouse_pos = pygame.mouse.get_pos()
                
                # Kliknutí na tlačítko Závodit
                if race_button.is_hover(mouse_pos):
                    race_screen()
                    continue
                
                x, y = kliknuti(mouse_pos)
                
                if 0 <= x < pocet_čtvercu_strana and 0 <= y < pocet_čtvercu_strana:
                    if event.button == 1:  # Levé tlačítko - přidej obrázek
                        # Kontrola jestli už nemáme maximální počet obrázků daného typu
                        if pocet_obrazku[current_image] < max_pocet_obrazku[current_image]:
                            grid[y][x].append(current_image)
                            pocet_obrazku[current_image] += 1
                            print(f"Přidán obrázek {current_image} na pozici [{x}, {y}]")
                        else:
                            print(f"Nelze přidat další obrázek typu {current_image}, dosažen maximální počet.")
                    elif event.button == 3:  # Pravé tlačítko - odeber poslední obrázek
                        if grid[y][x]:  # Pokud jsou v buňce nějaké obrázky
                            removed = grid[y][x].pop()
                            pocet_obrazku[removed] -= 1
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
                elif event.key == pygame.K_DELETE:
                    x, y = kliknuti(pygame.mouse.get_pos())
                    if 0 <= x < pocet_čtvercu_strana and 0 <= y < pocet_čtvercu_strana:
                        # Aktualizace počtu obrázků před vymazáním
                        for img_id in grid[y][x]:
                            pocet_obrazku[img_id] -= 1
                        grid[y][x].clear()
                        print(f"Smazány všechny obrázky na pozici [{x}, {y}]")
        
        # Vykreslení mřížky
        draw_grid()
        
        # Zjištění pozice myši pro efekt hover na tlačítku
        mouse_pos = pygame.mouse.get_pos()
        race_button.is_hover(mouse_pos)
        
        # Vykreslení tlačítka Závodit
        race_button.draw(screen)
        
        pygame.display.update()
        clock.tick(FPS)

def options():
    # Menu nastavení
    running = True
    back_button = Button("Zpět", WIDTH/2 - 100, 400, 200, 50, WHITE, GRAY)
    mute_button = Button("Mute", WIDTH/2 - 100, 300, 100, 50, WHITE, GRAY)
    unmute_button = Button("Unmute", WIDTH/2 + 15, 300, 100, 50,WHITE, GRAY)
    
    while running:
        screen.fill(BLUE)
        
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mute_button.is_hover(mouse_pos):
                    pygame.mixer.music.pause()
                elif unmute_button.is_hover(mouse_pos):
                    pygame.mixer.music.unpause()
                elif back_button.is_hover(mouse_pos):
                    running = False
                    
        
        options_text = font.render("NASTAVENÍ", True, RED)
        text_rect = options_text.get_rect(center=(WIDTH/2, 100))
        screen.blit(options_text, text_rect)
        
        back_button.is_hover(mouse_pos)
        back_button.draw(screen)
        mute_button.is_hover(mouse_pos)
        mute_button.draw(screen)
        unmute_button.is_hover(mouse_pos)
        unmute_button.draw(screen)
        
        pygame.display.update()
        clock.tick(FPS)

# Spuštění menu
if __name__ == "__main__":
    main_menu()