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

        # Später: self.checkpoint.check_reached() => Erreichen des Checkpoints prüfen

    def check_collisions(self):
        # Szenario 1: Runner trifft Hindernis
        hits = pg.sprite.spritecollide(self.runner, self.game.obstacles, False) # hits (Liste aller berührten Hindernisse vom Runner): Pygame-Funktion prüft auf Kollision von 'runner' und 'obstacles', False: Nicht-Löschen von Hindernis
            # spritecollider: Pygame-Funktion zum Finden von Kollisionen von Runner mit Hindernissen

        for obstacle in hits: # Iteration aller berührten Hindernisse des Runners (hits)
            self.runner.collide_with_obstacle(obstacle) # Kollision: Runner - Hindernis: Weitergabe zu 'collide_with_obstacle' für Reaktion des Runners (z.B. Zurückschieben durch Hindernis)
                    # To-Do: Implementierung der Methode 'collide_with_obstacle'

        # Szenario 2: Projektil trifft Runner
        hits = pg.sprite.spritecollide(self.runner, self.game.projectiles, False) # hits (Liste aller berührten Projektile vom Runner): Pygame-Funktion prüft auf Kollision von 'runner' und 'projectiles'
            # spritecollider: Pygame-Funktion zum Finden von Kollisionen von Runner mit Projektilen
        for projectile in hits: # Iteration aller berührten Projektile des Runners (hits)
            projectile.check_collision_with_runner(self.runner) # Kollision: Projektil - Runner: Weitergabe zu 'check_collision_with_runner' für Reaktion jedes Projektils: Berührung mit Runner? (Wenn ja: Punkt an Kanone + Löschen Projektil)
                    # To-Do: Implementierung der Methode 'check_collision_with_runner'

        # Szenario 3: Projektil trifft Hindernis
        hits = pg.sprite.groupcollide(self.game.projectiles, self.game.obstacles, False, False) # hits (Liste aller Projektile und dazugehöriger getroffener Hindernisse): Pygame-Funktion prüft auf Kollision von 'projectiles' und 'obstacles'
            # groupcollider: Pygame-Funktion zum Finden von Kollisionen von Projektilen und Hindernissen => Rückgabe: Dictionary { projectil: [liste_getroffener_hindernisse] }

        for projectile, obstacle_hit in hits.items():
            for obstacle in obstacle_hit: # Iteration aller getroffener Hindernisse von Projektilen
                projectile.check_collision_with_obstacle(obstacle) # Kollision: Projektil - Hindernis: Weitergabe zu 'check_collision_with_obstacle' für Reaktion jedes Projektils: Berührung mit Hindernis? (Wenn ja: Projectil löscht sich selbst durch Kollision)
                    # To-Do: Implementierung der Methode 'check_collision_with_obstacle'
        
    def draw(self, screen):
        screen.fill(BLACK)
        
        # Zeichnen der Bahnen/Linien 
        for i in range(NUM_LANES + 1):
            y = i * LANE_HEIGHT
            pg.draw.line(screen, DARKGRAY, (0, y), (WIDTH, y), 1)
        
        # Zeichnen aller Sprites
        self.game.all_sprites.draw(screen)