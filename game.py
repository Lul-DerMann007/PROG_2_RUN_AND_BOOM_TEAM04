# game.py

import pygame 
from settings import *
from gameworld import GameWorld
from player import Player

class Game:
    
    #Das ist die entscheidende Hauptklasse des Spiels (Context). Verwaltet Initialisierung, den Game Loop und den Spielzustand.
    
    
    def __init__(self):
        # Initialisierung und Fenster erstellen
        pygame.init() 
        
        try:
            pygame.mixer.init()
        except Exception:
            print("Audio mixer fehlgeschlagen, weiter ohne audio")
        
        # Fenster erstellen und Einstellungen setzen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE) 
        
        # Zeitmodule und interne Zustände
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.all_sprites = pygame.sprite.Group()    #alle sprites werden in einer gruppe gespeichert (sehr leicht so aufzurufen)
        self.obstacles = pygame.sprite.Group()      #nur für hindernisse (kollisionen)  !Spätere Implementierung!
        self.projectiles = pygame.sprite.Group()    #nur für projektile (kollisionen) !Spätere Implementierung!
        
        #Player Objekte erstellen
        self.player1 = Player("Spieler 1", PLAYER1_CONTROLS)
        self.player2 = Player("Spieler 2", PLAYER2_CONTROLS)

        #referenz auf aktuelle rollen (!Später!)
        self.current_runner = None
        self.current_cannon = None

        #Spielwelt erstellen
        self.world = GameWorld(self)
        self.world.setup_round()

    def events(self):   #Events: Verarbeitet alle Benutzer- und Systemereignisse.
        # Wenn Nutzer fenster schließt oder ESC drückt, wird das Spiel beendet
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False                
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

                #!Später! Hier Startlogik für neue Runden rein

    def update(self, dt):
        # zentrale Update-Logik, aufgerufen pro Frame (dt=Deltatime), steuert wann die welt aktualisiert wird
        self.world.update(dt)

    def draw(self):
        self.world.draw(self.screen)    #ermöglicht "zeichnen" im Fenster       (über gameworld)
        pygame.display.update()         #zeigt das gezeichnete dann an
        
    def run(self):      #Gameloop (läuft so lange self.running True ist)
        while self.running:                     
            dt_ms = self.clock.tick(FPS)
            dt_s = dt_ms / 1000             #zeit messung (framerate)                             
            self.events()       #events verarbeiten
            self.update(dt_s)  #spielstand für aktuellen frame aktualisieren
            self.draw() 

        # Schließen des Programms, wenn Schleife beendet ist
        pygame.quit()