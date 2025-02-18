import pygame

# Inicializace Pygame
pygame.init()
pygame.mixer.init()

# Nastavení okna
screen = pygame.display.set_mode((550, 350))
pygame.display.set_caption("Přehrávač hudby")

# Seznam písniček
pisnicky = ["Bad_piggies_theme.mp3", "SIGMA-BOY-PHONK-REMIX-.mp3"]
aktualni_pisnicka = 0  # Index aktuální písničky
is_playing = True      # Sledování stavu přehrávání

# Načtení první písničky
pygame.mixer.music.load(pisnicky[aktualni_pisnicka])
pygame.mixer.music.play()

# Hlavní smyčka
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                    is_playing = False
                else:
                    pygame.mixer.music.unpause()
                    is_playing = True
            elif event.key == pygame.K_RIGHT:  # Další písnička
                aktualni_pisnicka = (aktualni_pisnicka + 1) % len(pisnicky)
                pygame.mixer.music.load(pisnicky[aktualni_pisnicka])
                pygame.mixer.music.play()
                is_playing = True
            elif event.key == pygame.K_LEFT:   # Předchozí písnička
                aktualni_pisnicka = (aktualni_pisnicka - 1) % len(pisnicky)
                pygame.mixer.music.load(pisnicky[aktualni_pisnicka])
                pygame.mixer.music.play()
                is_playing = True
            elif event.key == pygame.K_q:
                running = False
    
    # Vykreslení textu
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 36)
    
    # Zobrazení ovládacích prvků
    text1 = font.render("Mezerník - Pauza/Pokračovat", True, (0, 0, 0))
    text2 = font.render("Q - Ukončit", True, (0, 0, 0))
    text3 = font.render("LEFT - Další písnička", True, (0, 0, 0))
    text4 = font.render("RIGHT - Předchozí písnička", True, (0, 0, 0))
    
    # Zobrazení aktuálního stavu
    status = font.render(f"Hraje: {pisnicky[aktualni_pisnicka]}", True, (0, 100, 0))
    playing_text = font.render("Stav: Hraje" if is_playing else "Stav: Pozastaveno", True, (0, 100, 0))
    
    # Vykreslení všech textů
    screen.blit(text1, (50, 50))
    screen.blit(text2, (50, 100))
    screen.blit(text3, (50, 150))
    screen.blit(text4, (50, 200))
    screen.blit(status, (50, 250))
    screen.blit(playing_text, (50, 280))
    
    pygame.display.flip()

pygame.quit()