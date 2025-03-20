import pygame
import sys
import random
import math
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
aktualni_pisnicka = 0
is_playing = True
#správné načtení písniček
Zvuk_ready = True
try:
    pygame.mixer.init()
    print("zkuv funguje")
except pygame.error as e:
    Zvuk_ready = False
    print(f"Chyba při inicializaci zvuku: {e}")
    
if Zvuk_ready:
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

závodní_plocha = load_and_scale_image("trat3.png", (10000,800))
závodní_plocha_x = 0
závodní_plocha_y = 0

def rainbow_color_sin(time_passed):
    r = int(127.5 * (math.sin(time_passed * 0.3) + 1))
    g = int(127.5 * (math.sin(time_passed * 0.3 + 2.094) + 1))  # 2.094 = 2π/3
    b = int(127.5 * (math.sin(time_passed * 0.3 + 4.188) + 1))  # 4.188 = 4π/3
    return (r, g, b)

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
    quit_button = Button("Ukončit", WIDTH/2 - 100, 500, 200, 50, WHITE, GRAY)
    help_button = Button("Nápověda",WIDTH/2 - 100, 400, 200, 50, WHITE, GRAY)
    
    # Hlavní menu smyčka
    running = True
    while running:
        color = rainbow_color_sin(pygame.time.get_ticks() / 1000)
        screen.fill(LIGHT_BLUE)
        
        # Vykreslení nadpisu
        title = font.render("HLAVNÍ MENU", True, color)
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
                    game()  # Spustit stavbu
                if options_button.is_hover(mouse_pos):
                    options()  # Otevřít nastavení
                if help_button.is_hover(mouse_pos):
                    pomoc()
                if quit_button.is_hover(mouse_pos):
                    pygame.quit()
                    sys.exit()
        
        # Kontrola pohybu myši přes tlačítka
        start_button.is_hover(mouse_pos)
        options_button.is_hover(mouse_pos)
        quit_button.is_hover(mouse_pos)
        help_button.is_hover(mouse_pos)
        
        # Vykreslení tlačítek
        start_button.draw(screen)
        options_button.draw(screen)
        quit_button.draw(screen)
        help_button.draw(screen)
        
        pygame.display.update()

def race_screen():
    # Obrazovka pro závodění
    global závodní_plocha_x, závodní_plocha_y
    running = True
    back_button = Button("Zpět do Editoru", WIDTH/2 - 150, HEIGHT - 100, 300, 50, WHITE, GRAY)
    
    # Nové tlačítko pro další mapu - bude viditelné až po dokončení závodu
    next_level_button = Button("Další Mapa", WIDTH - 150, HEIGHT//2, 140, 50, GREEN, (50, 255, 50))
    
    # Definuj rozměry pro menší obrázky
    small_cell_size = 30  # Menší velikost obrázků
    
    # Vytvoř kopii mřížky pro závodní obrazovku
    race_grid = [[[] for _ in range(pocet_čtvercu_strana)] for _ in range(pocet_čtvercu_strana)]
    
    # Zkopíruj původní mřížku
    for y in range(pocet_čtvercu_strana):
        for x in range(pocet_čtvercu_strana):
            race_grid[y][x] = [img for img in grid[y][x]]
    
    # Kontrola, zda auto má motor (ID 3)
    has_motor = False
    for y in range(pocet_čtvercu_strana):
        for x in range(pocet_čtvercu_strana):
            if 3 in race_grid[y][x]:
                has_motor = True
                break
        if has_motor:
            break
    
    # Kontrola, zda auto má řidiče/hlavu
    has_driver = False
    for y in range(pocet_čtvercu_strana):
        for x in range(pocet_čtvercu_strana):
            if 1 in race_grid[y][x]:  # Předpokládám, že ID 1 je hlava/řidič
                has_driver = True
                break
        if has_driver:
            break
    
    # Kontrola, zda auto má kola
    has_wheels = False
    wheel_positions = []
    for y in range(pocet_čtvercu_strana):
        for x in range(pocet_čtvercu_strana):
            if 4 in race_grid[y][x]:  # ID 4 jsou kola
                wheel_positions.append((x, y))
                has_wheels = True
    
    # Funkce pro detekci výšky šedé lajny na aktuální x-pozici
    def get_line_height(x_position):
        # Převod globální x-pozice na pozici v rámci obrázku závodní_plocha
        local_x = int(x_position - závodní_plocha_x)
        
        # Kontrola, zda je x_position v platném rozsahu
        if local_x < 0 or local_x >= závodní_plocha.get_width():
            return 600  # Výchozí výška
        
        # Projdeme sloupec pixelů odshora dolů, hledáme šedou barvu (lajnu)
        for y in range(závodní_plocha.get_height()):
            # Získání barvy pixelu
            try:
                color = závodní_plocha.get_at((local_x, y))
                # Kontrola, zda je pixel šedý (přibližně)
                if abs(color[0] - color[1]) < 10 and abs(color[1] - color[2]) < 10 and 50 < color[0] < 150:
                    return y + závodní_plocha_y  # Vrátíme globální y-pozici
            except IndexError:
                pass  # Ignorujeme chyby mimo rozsah
        
        return 600  # Pokud nenajdeme šedou barvu, vrátíme výchozí výšku
    
    # Proměnné pro sledování polohy auta
    car_x = WIDTH // 2  # Auto zůstává horizontálně ve středu obrazovky
    car_y = 600  # Výchozí výška auta
    car_angle = 0  # Úhel naklonění auta
    
    # Najdi nejnižší komponentu v mřížce (ne jen kolo)
    lowest_component = None
    lowest_y = -1
    
    # Hledání nejnižší komponenty v mřížce
    for y in range(pocet_čtvercu_strana):
        for x in range(pocet_čtvercu_strana):
            if race_grid[y][x]:  # Pokud je v tomto poli jakýkoliv obrázek
                if y > lowest_y:
                    lowest_y = y
                    lowest_component = (x, y)
    
    # Funkce pro kontrolu, zda kola dotýkají lajny
    def wheels_touch_ground():
        if not wheel_positions:
            return False
            
        for wheel_x, wheel_y in wheel_positions:
            # Vypočítat globální x-souřadnici tohoto kola na obrazovce
            global_wheel_x = car_x + (wheel_x - pocet_čtvercu_strana//2) * small_cell_size
            
            # Získat výšku lajny na pozici kola
            line_height = get_line_height(global_wheel_x)
            
            # Pokud některé kolo je v kontaktu s lajnou
            wheel_bottom = car_y + wheel_y * small_cell_size + small_cell_size
            if abs(wheel_bottom - line_height) < 5:
                return True
        
        return False
    
    # Proměnné pro efekt rozjíždění
    car_speed = 0
    car_acceleration = 0.075
    car_deceleration = 0.2
    max_car_speed = 6
    min_car_speed = -4  # Umožníme zápornou rychlost pro pohyb dozadu
    
    # Proměnné pro rotaci kol
    wheel_rotation_angle = 0
    wheel_rotation_speed = 0  # Rychlost rotace kol
    
    # Proměnné pro zobrazení stavu
    is_accelerating = False
    is_braking = False
    is_rolling_back = False
    is_rolling_forward = False
    
    # Parametry závodní trati
    track_length = 9500 # Délka závodní trati (šířka obrázku závodní_plocha)
    finish_line_x = -track_length# + WIDTH  # X-pozice cílové čáry (konec trati)
    race_completed = False
    race_time = 0  # Čas závodu v sekundách
    race_timer_active = False
    finish_celebration_timer = 0
    
    # Načteme originální obrázek kola pro rotaci
    original_wheel = None
    try:
        original_wheel = pygame.image.load("pneumatika.png")
        original_wheel = pygame.transform.scale(original_wheel, (small_cell_size, small_cell_size))
    except pygame.error:
        print("Nelze načíst originální obrázek kola pro rotaci")
        original_wheel = pygame.Surface((small_cell_size, small_cell_size))
        original_wheel.fill(RED)
    
    # Sledování předchozích výšek lajny pro plynulý přechod
    prev_line_heights = [600] * 10
    
    # Gravitační konstanta pro automatické rozjíždění na svahu
    gravity_factor = 0.05
    
    # Hodnota pro rozlišení, kdy je auto na rovině (blízko nule)
    flat_surface_threshold = 0.5

    while running:
        screen.fill(BLUE)  # Modrá barva pozadí pro závodní obrazovku
        screen.blit(závodní_plocha, (závodní_plocha_x, závodní_plocha_y))
        random_color = rainbow_color_sin(pygame.time.get_ticks() / 1000)
        
        # Aktualizace časovače závodu
        if race_timer_active and not race_completed:
            race_time += 1/FPS
        
        key = pygame.key.get_pressed()
        
        # Reset stavů
        is_accelerating = False
        is_braking = False
        is_rolling_back = False
        is_rolling_forward = False
        
        # Kontrola, zda jsme dosáhli cíle
        if závodní_plocha_x <= finish_line_x and not race_completed:
            race_completed = True
            car_speed = 0
            wheel_rotation_speed = 0
            # Spustíme časovač pro oslavnou animaci
            finish_celebration_timer = 3  # 3 sekundy oslav
            
            # Zkusíme přehrát zvuk vítězství, pokud je k dispozici
            if Zvuk_ready:
                try:
                    victory_sound = pygame.mixer.Sound("victory.wav")
                    victory_sound.play()
                except:
                    print("Nelze přehrát zvuk vítězství")
        
        # Získání aktuální výšky lajny pod středem auta
        current_line_height = get_line_height(car_x)
        
        # Přidáme aktuální výšku do seznamu předchozích výšek a odstraníme nejstarší
        prev_line_heights.append(current_line_height)
        prev_line_heights.pop(0)
        
        # Vypočítáme průměrnou výšku pro plynulejší pohyb
        avg_line_height = sum(prev_line_heights) / len(prev_line_heights)
        
        # Pokud máme nejnižší komponentu, vypočítáme výšku auta přesně tak, aby se tato komponenta dotýkala lajny
        if lowest_component:
            component_x, component_y = lowest_component
            
            # Vypočítáme pozici auta tak, aby spodní hrana nejnižší komponenty byla přesně na lajně
            # Výpočet bere v úvahu pozici nejnižší komponenty vzhledem ke středu auta
            offset_from_center = (component_y + 1) * small_cell_size - (pocet_čtvercu_strana * small_cell_size / 2)
            target_car_y = avg_line_height - offset_from_center
        else:
            # Pokud nemáme žádnou komponentu, použijeme výchozí logiku
            target_car_y = avg_line_height - small_cell_size * pocet_čtvercu_strana / 2
        
        # Nyní přesně nastavíme pozici auta bez plynulého přechodu pro přesné umístění na lajně
        car_y = target_car_y
        
        # Vypočítáme úhel naklonění auta podle sklonu lajny
        if len(prev_line_heights) > 2:
            # Změna výšky za posledních několik snímků
            height_diff = prev_line_heights[0] - prev_line_heights[-1]
            # Omezíme maximální úhel naklonění
            car_angle = max(-35, min(35, height_diff * 1.5))
        
        # Kontrola stisknutých kláves - jen pokud závod neskončil, máme motor, řidiče A KOLA
        if not race_completed and has_motor and has_driver and has_wheels:
            # Efekt gravitace na svahu - auto se rozjíždí automaticky při náklonu
            if abs(car_angle) > flat_surface_threshold:  # Pokud jsme na svahu
                if car_angle > flat_surface_threshold:  # Do kopce
                    if not key[pygame.K_RIGHT]:# Pokud neakcelerujeme, auto se rozjíždí dozadu
                        car_speed -= car_angle * gravity_factor
                        is_rolling_back = True
                        race_timer_active = True  # Spustíme časovač
            elif car_angle < -flat_surface_threshold:  # Z kopce - auto se rozjíždí dopředu
                car_speed -= car_angle * gravity_factor  # Záporný úhel vytváří kladnou rychlost
                is_rolling_forward = True
                race_timer_active = True  # Spustíme časovač
            
            # Omezení rychlosti
            if car_speed > max_car_speed:
                car_speed = max_car_speed
            elif car_speed < min_car_speed:
                car_speed = min_car_speed
            
            # Aktivní ovládání uživatelem
            if key[pygame.K_RIGHT]:
                # Zrychlování - funguje vždy
                is_accelerating = True
                race_timer_active = True  # Spustíme časovač při prvním zrychlení
                
                if car_speed < max_car_speed:
                    car_speed += car_acceleration
                if car_speed > max_car_speed:
                    car_speed = max_car_speed
                    
                # Zvyšujeme rychlost rotace kol
                wheel_rotation_speed = 10 + abs(car_speed) * 2  # Závisí na rychlosti auta
            
            elif key[pygame.K_LEFT]:
                # Brzdění - funguje pouze pokud je auto na rovině
                if abs(car_angle) <= flat_surface_threshold:
                    is_braking = True
                    if car_speed > 0:
                        car_speed -= car_deceleration
                    elif car_speed < 0:
                        car_speed += car_deceleration
                    
                    # Kola se zpomalují při brzdění
                    wheel_rotation_speed = max(0, wheel_rotation_speed - 5)
                else:
                    # Když nejsme na rovině, brzdění nefunguje
                    pass
            
            else:
                # Postupné přirozené zpomalení na rovině, když není stisknutá žádná klávesa
                if abs(car_angle) <= flat_surface_threshold:
                    if car_speed > 0:
                        car_speed -= 0.07
                        if car_speed < 0:
                            car_speed = 0
                    elif car_speed < 0:
                        car_speed += 0.07
                        if car_speed > 0:
                            car_speed = 0
                
                # Kola se postupně zpomalují
                wheel_rotation_speed = max(0, wheel_rotation_speed - 1)
        else:
            # Pokud jsme v cíli a běží oslavný časovač
            if finish_celebration_timer > 0:
                finish_celebration_timer -= 1/FPS
                
                # Kola se zastaví postupně
                wheel_rotation_speed = max(0, wheel_rotation_speed - 2)
        
        # Aktualizace úhlu rotace kol - směr rotace podle směru pohybu
        if car_speed > 0:
            wheel_rotation_angle -= wheel_rotation_speed  # Dopředu
        else:
            wheel_rotation_angle += wheel_rotation_speed  # Dozadu
            
        if wheel_rotation_angle >= 360:
            wheel_rotation_angle %= 360
        elif wheel_rotation_angle <= -360:
            wheel_rotation_angle %= 360
        
        # Posunutí závodní plochy podle rychlosti
        if (not race_completed or závodní_plocha_x > finish_line_x) and has_motor and has_driver and has_wheels:
            # Základní pohyb podle rychlosti auta
            závodní_plocha_x -= car_speed
            
            # Zajistíme, že nepřejedeme za cílovou čáru
            if závodní_plocha_x < finish_line_x:
                závodní_plocha_x = finish_line_x
        
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
                    závodní_plocha_x = 0
                    running = False
                # Kontrola kliknutí na tlačítko "Další Mapa" (pouze pokud je závod dokončen)
                if race_completed and next_level_button.is_hover(mouse_pos):
                    # Zde by se přešlo na další úroveň
                    závodní_plocha_x = 0
                    race_completed = False
                    race_time = 0
                    race_timer_active = False
                    # Zde by se mohlo načíst další závodní mapa nebo změnit obtížnost
                    print("Přechod na další mapu!")
        
        # Vykreslení auta (s efektem rotujících kol)
        # Vytvoříme povrch pro rotaci celého auta
        car_surface = pygame.Surface((pocet_čtvercu_strana * small_cell_size, 
                                     pocet_čtvercu_strana * small_cell_size), pygame.SRCALPHA)
        
        car_surface.fill((0, 0, 0, 0))  # Průhledný povrch
        
        # Vykreslíme auto na car_surface
        for y in range(pocet_čtvercu_strana):
            for x in range(pocet_čtvercu_strana):
                # Pokud má buňka nějaké obrázky
                if race_grid[y][x]:
                    for img_index, img_id in enumerate(race_grid[y][x]):
                        # Umístění obrázků se zachováním původní struktury mřížky
                        local_x = x * small_cell_size
                        local_y = y * small_cell_size
                        
                        # Speciální zpracování pro kola (id 4) - rotace
                        if img_id == 4 and original_wheel:
                            # Vytvoření rotované kopie kola
                            rotated_wheel = pygame.transform.rotate(original_wheel, wheel_rotation_angle)
                            
                            # Získání nového obdélníku rotovaného kola (aby bylo vystředěno)
                            wheel_rect = rotated_wheel.get_rect(center=(local_x + small_cell_size/2, 
                                                                     local_y + small_cell_size/2))
                            
                            # Vykreslení rotovaného kola
                            car_surface.blit(rotated_wheel, wheel_rect.topleft)
                        else:
                            # Standardní vykreslení ostatních obrázků
                            small_img = pygame.transform.scale(obrazky[img_id], (small_cell_size, small_cell_size))
                            car_surface.blit(small_img, (local_x, local_y))
        
        # Pokud máme úhel naklonění, aplikujeme korekci pozice podle úhlu
        angle_correction = 0
        if car_angle != 0:
            # Korekce pozice pro naklonění - pozitivní úhel = nakloněné dopředu = vyšší pozice
            angle_correction = math.sin(math.radians(car_angle)) * small_cell_size * 0.5
            car_y -= angle_correction  # Přičtení korekce k y-pozici
        
        # Rotujeme celé auto podle sklonu lajny
        if car_angle != 0:
            rotated_car = pygame.transform.rotate(car_surface, car_angle)
            car_rect = rotated_car.get_rect(center=(car_x, car_y))
            screen.blit(rotated_car, car_rect.topleft)
        else:
            # Vykreslení auta bez rotace
            car_rect = car_surface.get_rect(center=(car_x, car_y))
            screen.blit(car_surface, car_rect.topleft)
        
        # Vykreslíme šedou čáru pro debugování pouze pokud je v debug módu
        pygame.draw.circle(screen, (255, 0, 0), (car_x, avg_line_height), 5)
        
        # Pro každou komponentu vykreslíme bod kontaktu s povrchem (pro debugování)
        # Zvýrazníme nejnižší komponentu červeným bodem
        if lowest_component:
            lowest_x, lowest_y = lowest_component
            global_lowest_x = car_x + (lowest_x - pocet_čtvercu_strana//2) * small_cell_size
            global_lowest_y = car_y + lowest_y * small_cell_size + small_cell_size
            
            # Vykreslíme červený bod pro nejnižší komponentu
            pygame.draw.circle(screen, (255, 0, 0), (global_lowest_x, global_lowest_y), 5)
            
            # Zjistíme výšku lajny pod touto komponentou
            component_line_height = get_line_height(global_lowest_x)
            
            # Vykreslíme modrou čáru mezi nejnižší komponentou a lajnou
            pygame.draw.line(screen, (0, 0, 255), 
                          (global_lowest_x, global_lowest_y), 
                          (global_lowest_x, component_line_height), 2)
            
            # Vizualizace vzdálenosti mezi nejnižší komponentou a lajnou
            distance = abs(global_lowest_y - component_line_height)
            distance_text = small_font.render(f"Vzdálenost: {distance:.1f}", True, WHITE)
            screen.blit(distance_text, (10, 150))
        
        # Pro každé kolo vykreslíme bod jeho kontaktu s povrchem (pro debugování)
        if wheel_positions:
            for wheel_x, wheel_y in wheel_positions:
                global_wheel_x = car_x + (wheel_x - pocet_čtvercu_strana//2) * small_cell_size
                global_wheel_y = car_y + wheel_y * small_cell_size + small_cell_size
                # Zjistíme výšku lajny pod tímto kolem
                wheel_line_height = get_line_height(global_wheel_x)
                # Vykreslíme zelený bod v místě kontaktu kola s lajnou
                pygame.draw.circle(screen, (0, 255, 0), (global_wheel_x, wheel_line_height), 3)
        
        # Zobrazení rychlosti a stavu
        speed_text = small_font.render(f"Rychlost: {int(car_speed * 10)} km/h", True, WHITE)
        screen.blit(speed_text, (10, 50))
        
        # Zobrazení úhlu terénu
        angle_text = small_font.render(f"Úhel: {car_angle:.2f}°", True, WHITE)
        screen.blit(angle_text, (10, 80))
        
        # Zobrazení času závodu
        time_text = small_font.render(f"Čas: {race_time:.2f} s", True, WHITE)
        screen.blit(time_text, (10, 120))
        
        # Zobrazení stavu závodu
        if race_completed:
            completed_text = font.render("CÍL DOSAŽEN!", True, (255, 215, 0))  # Zlatá barva
            screen.blit(completed_text, (WIDTH//2 - completed_text.get_width()//2, 200))
            
            # Pokud máme finální čas, zobrazíme ho
            final_time_text = font.render(f"Váš čas: {race_time:.2f} s", True, (255, 215, 0))
            screen.blit(final_time_text, (WIDTH//2 - final_time_text.get_width()//2, 250))
            
            # Zobrazíme tlačítko pro další mapu - pouze když je závod dokončen
            next_level_button.is_hover(mouse_pos)
            next_level_button.draw(screen)
        else:
            # Zobrazení upozornění, pokud nemáme motor, řidiče nebo kola
            if not has_motor:
                no_motor_text = font.render("CHYBÍ MOTOR!", True, random_color)
                screen.blit(no_motor_text, (WIDTH//2 - no_motor_text.get_width()//2, 200))
                
                hint_text = small_font.render("Přidejte motor ke svému vozidlu", True, random_color)
                screen.blit(hint_text, (WIDTH//2 - hint_text.get_width()//2, 250))
            elif not has_driver:
                no_driver_text = font.render("CHYBÍ ŘIDIČ!", True, random_color)
                screen.blit(no_driver_text, (WIDTH//2 - no_driver_text.get_width()//2, 200))
                
                hint_text = small_font.render("Přidejte hlavu ke svému vozidlu", True, random_color)
                screen.blit(hint_text, (WIDTH//2 - hint_text.get_width()//2, 250))
            elif not has_wheels:
                no_wheels_text = font.render("CHYBÍ KOLA!", True, random_color)
                screen.blit(no_wheels_text, (WIDTH//2 - no_wheels_text.get_width()//2, 200))
                
                hint_text = small_font.render("Přidejte kola ke svému vozidlu pro pohyb", True, random_color)
                screen.blit(hint_text, (WIDTH//2 - hint_text.get_width()//2, 250))
            else:
                # Zobrazení stavu jízdy
                status_text = ""
                status_color = WHITE
                if is_accelerating:
                    status_text = "ZRYCHLOVÁNÍ!"
                    status_color = GREEN
                elif is_braking:
                    status_text = "BRZDĚNÍ!"
                    status_color = RED
                elif is_rolling_back:
                    status_text = "COUVÁNÍ (SVAH)!"
                    status_color = LIGHT_BLUE
                elif is_rolling_forward:
                    status_text = "ZRYCHLOVÁNÍ (SVAH)!"
                    status_color = LIGHT_BLUE
                
                if status_text:
                    state_text = small_font.render(status_text, True, status_color)
                    screen.blit(state_text, (WIDTH//2 - state_text.get_width()//2, 180))
        
        # Nadpis závodní obrazovky
        race_title = font.render("ZÁVOD 1.", False, random_color)
        title_rect = race_title.get_rect(center=(WIDTH/2, 50))
        screen.blit(race_title, title_rect)
        
        # Kontrola tlačítka
        back_button.is_hover(mouse_pos)
        back_button.draw(screen)
        
        pygame.display.update()
        clock.tick(FPS)
    

# Funkce pro bezpečné snížení počtu obrázků
def bezpecne_sniz_pocet(img_id):
    global pocet_obrazku
    if pocet_obrazku[img_id] > 0:
        pocet_obrazku[img_id] -= 1
        return True
    return False

# Funkce pro bezpečné zobrazení počtu obrázků
def bezpecne_spocitej_obrazky():
    global pocet_obrazku, grid
    
    # Resetování počtu obrázků
    pocet_obrazku = {1: 0, 2: 0, 3: 0, 4: 0}
    
    # Spočítání aktuálního počtu každého typu obrázku v mřížce
    for y in range(pocet_čtvercu_strana):
        for x in range(pocet_čtvercu_strana):
            for img_id in grid[y][x]:
                if img_id in pocet_obrazku:
                    pocet_obrazku[img_id] += 1

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
                            # Kontrola pravidel pro přidávání obrázků
                            if current_image == 2:  # Stavební blok lze přidat kdykoliv
                                grid[y][x].append(current_image)
                                pocet_obrazku[current_image] += 1
                                print(f"Přidán stavební blok na pozici [{x}, {y}]")
                            else:
                                # Kontrola, zda v buňce už není jiný obrázek než stavební blok
                                non_block_images = [img for img in grid[y][x] if img != 2]
                                if not non_block_images:  # Pokud v buňce není žádný jiný obrázek kromě bloků
                                    grid[y][x].append(current_image)
                                    pocet_obrazku[current_image] += 1
                                    print(f"Přidán obrázek {current_image} na pozici [{x}, {y}]")
                                else:
                                    print(f"V buňce [{x}, {y}] již existuje jiný obrázek.")
                        else:
                            print(f"Nelze přidat další obrázek typu {current_image}, dosažen maximální počet.")
                    elif event.button == 3:  # Pravé tlačítko - odeber poslední obrázek
                        if grid[y][x]:  # Pokud jsou v buňce nějaké obrázky
                            # Najdi poslední ne-blokový obrázek, pokud existuje
                            non_block_indices = [i for i, img in enumerate(grid[y][x]) if img != 2]
                            if non_block_indices:
                                # Odeber poslední ne-blokový obrázek
                                index = non_block_indices[-1]
                                removed = grid[y][x].pop(index)
                                # Bezpečně sníží počet obrázků
                                bezpecne_sniz_pocet(removed)
                                print(f"Odebrán obrázek {removed} z pozice [{x}, {y}]")
                            elif grid[y][x]:  # Jinak odeber poslední blok
                                removed = grid[y][x].pop()
                                # Bezpečně sníží počet obrázků
                                bezpecne_sniz_pocet(removed)
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
                            bezpecne_sniz_pocet(img_id)
                        grid[y][x].clear()
                        print(f"Smazány všechny obrázky na pozici [{x}, {y}]")
        
        # Vykreslení mřížky
        draw_grid()
        
        # Zjištění pozice myši pro efekt hover na tlačítku
        mouse_pos = pygame.mouse.get_pos()
        race_button.is_hover(mouse_pos)
        race_button.draw(screen)
        
        pygame.display.update()
        clock.tick(FPS)
        
        # Pro jistotu pravidelně aktualizuj počty obrázků
        bezpecne_spocitej_obrazky()
        
def pomoc():
    running = True
    back_button = Button("Zpět", WIDTH/2 - 100, 700, 200, 50, WHITE, GRAY)
    
    # Barvy pro jednotlivé sekce
    title_color = WHITE
    section_color = LIGHT_BLUE
    text_color = WHITE
    
    while running:
        color = rainbow_color_sin(pygame.time.get_ticks() / 1000)
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
                if back_button.is_hover(mouse_pos):
                    running = False
        
        # Nadpis
        title = font.render("NÁPOVĚDA", True, color)
        title_rect = title.get_rect(center=(WIDTH/2, 50))
        screen.blit(title, title_rect)
        
        # Informace o stavění auta
        build_title = small_font.render("Stavění auta:", True, section_color)
        screen.blit(build_title, (50, 120))
        
        # Vysvětlení jednotlivých obrázků
        img1_text = debug_font.render("Obrázek 1: Hlava (řidič) - lze umístit pouze 1×", True, text_color)
        img2_text = debug_font.render("Obrázek 2: Stavební blok - lze umístit až 5×", True, text_color)
        img3_text = debug_font.render("Obrázek 3: Motor - lze umístit pouze 1×", True, text_color)
        img4_text = debug_font.render("Obrázek 4: Kolo - lze umístit až 2×", True, text_color)
        
        screen.blit(img1_text, (70, 160))
        screen.blit(img2_text, (70, 190))
        screen.blit(img3_text, (70, 220))
        screen.blit(img4_text, (70, 250))
        
        # Vysvětlení ovládání při stavění
        build_controls = small_font.render("Ovládání stavění:", True, section_color)
        screen.blit(build_controls, (50, 300))
        
        controls1 = debug_font.render("Klávesy 1-4: Výběr typu obrázku", True, text_color)
        controls2 = debug_font.render("Levé tlačítko myši: Umístění obrázku", True, text_color)
        controls3 = debug_font.render("Pravé tlačítko myši: Odebrání posledního obrázku", True, text_color)
        controls4 = debug_font.render("Klávesa DELETE: Smazání všech obrázků v buňce", True, text_color)
        controls5 = debug_font.render("Klávesa ESC: Návrat do menu", True, text_color)
        
        screen.blit(controls1, (70, 340))
        screen.blit(controls2, (70, 370))
        screen.blit(controls3, (70, 400))
        screen.blit(controls4, (70, 430))
        screen.blit(controls5, (70, 460))
        
        # Vysvětlení ovládání při závodění
        race_title = small_font.render("Ovládání závodu:", True, section_color)
        screen.blit(race_title, (50, 510))
        
        race1 = debug_font.render("Pravá šipka: Zrychlení auta", True, text_color)
        race2 = debug_font.render("Levá šipka: Brzdění", True, text_color)
        race3 = debug_font.render("Pro úspěšný závod potřebujete motor a hlavu řidiče!", True, text_color)
        race4 = debug_font.render("Kola by měla být umístěna tak, aby se dotýkala země.", True, text_color)
        
        screen.blit(race1, (70, 550))
        screen.blit(race2, (70, 580))
        screen.blit(race3, (70, 610))
        screen.blit(race4, (70, 640))
        
        # Tlačítko pro návrat
        back_button.is_hover(mouse_pos)
        back_button.draw(screen)
        
        pygame.display.update()
        clock.tick(FPS)
    

def options():
    # Menu nastavení
    running = True
    back_button = Button("Zpět", WIDTH/2 - 100, 450, 200, 50, WHITE, GRAY)
    mute_button = Button("Mute", WIDTH/2 - 100, 300, 100, 50, WHITE, GRAY)
    unmute_button = Button("Unmute", WIDTH/2, 300, 100, 50, WHITE, GRAY)
    
    # Tlačítka pro ovládání hlasitosti
    volume_up_button = Button("+", WIDTH/2 + 50, 350, 50, 50, WHITE, GRAY)
    volume_down_button = Button("-", WIDTH/2 - 100, 350, 50, 50, WHITE, GRAY)
    
    # Aktuální hlasitost (0.0 až 1.0)
    try:
        current_volume = pygame.mixer.music.get_volume()
    except pygame.error:
        current_volume = 0.5  # Výchozí hodnota
    
    while running:
        color = rainbow_color_sin(pygame.time.get_ticks() / 1000)
        
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
                    try:
                        pygame.mixer.music.pause()
                    except pygame.error:
                        print("nelze zastavit kvůli nefunkčnímu modulu")
                elif unmute_button.is_hover(mouse_pos):
                    try:
                        pygame.mixer.music.unpause()
                    except pygame.error:
                        print("nelze pustit kvůli nefunkčnímu modulu")
                
                # Ovládání hlasitosti
                elif volume_up_button.is_hover(mouse_pos):
                    try:
                        current_volume = min(1.0, current_volume + 0.1)  # Zvýšit o 10%, max 1.0
                        pygame.mixer.music.set_volume(current_volume)
                    except pygame.error:
                        print("nelze změnit hlasitost kvůli nefunkčnímu modulu")
                elif volume_down_button.is_hover(mouse_pos):
                    try:
                        current_volume = max(0.0, current_volume - 0.1)  # Snížit o 10%, min 0.0
                        pygame.mixer.music.set_volume(current_volume)
                    except pygame.error:
                        print("nelze změnit hlasitost kvůli nefunkčnímu modulu")
                        
                elif back_button.is_hover(mouse_pos):
                    running = False
        
        options_text = font.render("NASTAVENÍ", True, color)
        text_rect = options_text.get_rect(center=(WIDTH/2, 100))
        screen.blit(options_text, text_rect)
        
        # Zobrazení aktuální hlasitosti
        volume_text = font.render(f"Hlasitost: {int(current_volume * 100)}%", True, WHITE)
        volume_rect = volume_text.get_rect(center=(WIDTH/2, 250))
        screen.blit(volume_text, volume_rect)
        
        back_button.is_hover(mouse_pos)
        back_button.draw(screen)
        mute_button.is_hover(mouse_pos)
        mute_button.draw(screen)
        unmute_button.is_hover(mouse_pos)
        unmute_button.draw(screen)
        
        # Vykreslení tlačítek pro hlasitost
        volume_up_button.is_hover(mouse_pos)
        volume_up_button.draw(screen)
        volume_down_button.is_hover(mouse_pos)
        volume_down_button.draw(screen)
        
        pygame.display.update()
        clock.tick(FPS)

# Spuštění menu
if True == True:
    main_menu()
