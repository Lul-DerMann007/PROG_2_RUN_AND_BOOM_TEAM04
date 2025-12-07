# gameworld.py
import pygame as pg
import random
from runner import Runner
from cannon import Cannon
from checkpoint import Checkpoint
from obstacle import Obstacle
from projectile import Projectile
from settings import * 

class GameWorld:
    def __init__(self, game):   #baut welt struktur auf
        self.game = game    # zugriff auf game funktionen
        
        self.runner: Runner = None
        self.cannon: Cannon = None              #Platzhalter für wichtigsten ojekte
        self.checkpoint: Checkpoint = None
        
        # Zustände der Welt
        self.scroll_speed: float = SCROLL_SPEED     #tempo der welt relativ zum runner
        self.obstacle_spawn_interval: float = 1.0   #wichtiges Balancing Tool für spätere Tests
        
    def setup_round(self):      #Initalisiert neue runde und füllr mit objekten
        
        # alle Gruppen werden erstmal  geleert
        self.game.all_sprites.empty()       #Entnommen nach KI Feedback ChatGPT. Prompt: "Aus Basis des Codes. Was müssen wir beachten, wenn wir eine neue Runde starten wollen? Halte dich kurz via Stichpunkten "
        self.game.obstacles.empty()         #KI Antwort: Sprite-Gruppen leeren, Spielerzustand zurücksetzen, Eingabe-Flags zurücksetzen, Score und Rundenzähler zurücksetzen, Sounds stoppen/neustarten, Kollisionszustände und Projektile löschen, UI-Elemente aktualisieren
        self.game.projectiles.empty()
        
        # Elemente erstellen (Komposition)
        start_x = 100
        checkpoint_x = start_x + CHECKPOINT_DISTANCE       #simple rechenlogik für platzierung objekte
        start_lane = NUM_LANES //2

        runner_controls = self.game.current_runner.controls
        cannon_controls = self.game.current_cannon.controls                          
        
        self.runner = Runner(self.game, start_x, start_lane,runner_controls)        
        self.cannon = Cannon(self.game, start_lane, cannon_controls)             #zugriff für wichtigsten elemente auf game, startpunkt usw.
        self.checkpoint = Checkpoint(self.game, checkpoint_x)

        self.checkpoint.is_reached = False
        
        # Werden zur Gruppe hinzugefügt und regelmäßig abgefragt
        self.game.all_sprites.add(self.runner, self.cannon, self.checkpoint)
        
        # Spawning (später)  
        # self.spawn_initial_obstacles()
        
    def update(self, dt: float):
        # Ruft die update-Methode in jedem Sprite auf
        self.game.all_sprites.update(dt)

        # Später: self.spawn_obstacles(dt)

        # Kollisionsprüfung: Ruft die check_collisions-Metode auf
        self.check_collisions()      

        if self.checkpoint and not self.checkpoint.is_reached :
            self.checkpoint.check_reached(self.runner)                               #Erreichen des Checkpoints prüfen

    def check_collisions(self):
        # Szenario 1: Runner trifft Hindernis       !Später! Erst nach Hinderniss Spawn Logik

        # Szenario 2: Projektil trifft Runner
        hits = pg.sprite.spritecollide(self.runner, self.game.projectiles, False) # hits (Liste aller berührten Projektile vom Runner): Pygame-Funktion prüft auf Kollision von 'runner' und 'projectiles'
            # spritecollider: Pygame-Funktion zum Finden von Kollisionen von Runner mit Projektilen
        for projectile in hits: # Iteration aller berührten Projektile des Runners (hits)
            projectile.check_collision_with_runner(self.runner) # Kollision: Projektil - Runner: Weitergabe zu 'check_collision_with_runner' für Reaktion jedes Projektils: Berührung mit Runner? (Wenn ja: Punkt an Kanone + Löschen Projektil)

        # Szenario 3: Projektil trifft Hindernis        !Später! Erst nach Hinderniss Spawn Logik
        
    def draw(self, screen):
        screen.fill(BLACK)
        
        # Zeichnen der Bahnen/Linien 
        for i in range(NUM_LANES + 1):
            y = i * LANE_HEIGHT
            pg.draw.line(screen, DARKGRAY, (0, y), (WIDTH, y), 1)
        
        # Zeichnen aller Sprites
        self.game.all_sprites.draw(screen)