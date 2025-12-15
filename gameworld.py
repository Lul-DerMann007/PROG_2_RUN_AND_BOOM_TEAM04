# gameworld.py
import pygame as pg
import random
from runner import Runner
from cannon import Cannon
from checkpoint import Checkpoint
from obstacle import ObstacleFactory
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
        self.obstacle_spawn_interval: float = OBSTACLE_SPAWN_INTERVAL   #wichtiges Balancing Tool 
        self.obstacle_spawn_timer: float = 0.0 #Timer für kontinuierliches Spawning  


    def setup_round(self, runner_color, cannon_color):      #Initalisiert neue runde und füllr mit objekten
        
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


        self.runner = Runner(self.game, start_x, start_lane,runner_controls, runner_color)    #Übergibt die Farbe an die Runner Klasse damit richtiges Sprite geladen wird     
        self.cannon = Cannon(self.game, start_lane, cannon_controls, cannon_color)             #zugriff für wichtigsten elemente auf game, startpunkt usw.
        self.checkpoint = Checkpoint(self.game, checkpoint_x) 

        self.checkpoint.is_reached = False
        
        self.obstacle_spawn_timer = 0               #Timer zurücksetzen und intiale Hinderisse spawnen
        self.spawn_initial_obstacle() 

    #Funktion is_lane_free ist Ki-generiert mit Claude AI. Prompt:"Basierend auf dem bestehenden Code und der vorhandenen Obstacle Logik. Entwerfe eine Methode, die prüft ob die Lane, in der ein neues Hindernis spawnen soll, frei ist. Ergänze wie und wo diese Methode implementiert werden soll"
    def is_lane_free(self, lane, x_pos):
        target_lane_y = lane * LANE_HEIGHT + LANE_HEIGHT // 2               #Y-Koordinate an der Mitte der gewünschten Spur

        for obs in self.game.obstacles:
            obs_lane_y = obs.rect.centery                   #vergleich mit y-koordinate

            if abs(obs_lane_y - target_lane_y) < 5 :        #abs() gibt positiven abstand zu 0 zurück, hier mit 5 toleranz
                if x_pos < obs.rect.right + OBSTACLE_GAP:       
                    return False
        return True
        

    def spawn_initial_obstacle(self):
        current_x = 600         #Start weiter rechts, damit Runner Platz hat 
        while current_x < WIDTH + 200:      #Zufällige Lane-Reihenfolge, wo die Obstacles gespawnt werden
            lanes = list(range(NUM_LANES))
            random.shuffle(lanes)       #Funktion herausgefunden durch Google Anfrage "Liste neu mischen in pygame"

            for lane in lanes:  
                if self.is_lane_free(lane, current_x):                          #Es wird nicht mehr entschieden "WAS" gespawnt wird sonndern nur noch "WO und WANN" -> das "WAS" wurde an die ObstacleFactory ausgelagert
                    ObstacleFactory.create(self.game, current_x, lane)          
                    break               #Nur ein Hindernis pro X-Position

            current_x += random.randint(300,500)


    def spawn_obstacle(self,dt):        #Spawnt immer neue Obstacles während dem Spiel        
        self.obstacle_spawn_timer += dt
        if self.obstacle_spawn_timer >= self.obstacle_spawn_interval: 
            self.obstacle_spawn_timer = 0.0      #setzt den Timer zurück 

            spawn_x = WIDTH + 200       # Spawn außerhalb vom Bildschirm 

            for _ in range(9):  
                lane = random.randint(0,NUM_LANES -1)

                if self.is_lane_free(lane, spawn_x):    #Es wird nicht mehr entschieden "WAS" gespawnt wird sonndern nur noch "WO und WANN" -> das "WAS" wurde an die ObstacleFactory ausgelagert
                    ObstacleFactory.create(self.game,spawn_x,lane)
                    break 
               


    def update(self, dt: float):
        # Ruft die update-Methode in jedem Sprite auf
        self.game.all_sprites.update(dt)

        self.spawn_obstacle(dt)         #Aktiviert das Random Obstacle Spawning

        # Kollisionsprüfung: Ruft die check_collisions-Metode auf
        self.check_collisions()      

        if self.checkpoint and not self.checkpoint.is_reached :
            self.checkpoint.check_reached(self.runner)                               #Erreichen des Checkpoints prüfen

    def check_collisions(self):
        # Szenario 1: Runner trifft Hindernis
        hits = pg.sprite.spritecollide(self.runner, self.game.obstacles, False)
        for obstacle in hits:
            self.runner.collide_with_obstacle(obstacle)

        # Szenario 2: Projektil trifft Runner
        hits = pg.sprite.spritecollide(self.runner, self.game.projectiles, False) # hits (Liste aller berührten Projektile vom Runner): Pygame-Funktion prüft auf Kollision von 'runner' und 'projectiles'
            # spritecollider: Pygame-Funktion zum Finden von Kollisionen 
        for projectile in hits: # Iteration aller berührten Projektile des Runners (hits)
            projectile.check_collision_with_runner(self.runner) # Kollision: Projektil - Runner: Weitergabe zu 'check_collision_with_runner' für Reaktion jedes Projektils: Berührung mit Runner? (Wenn ja: Punkt an Kanone + Löschen Projektil)

        # Szenario 3: Projektil trifft Hindernis
        for projectile in self.game.projectiles: # Iteration durch alle Projektile: Prüfen für jedes, ob es Hindernisse trifft
            hits = pg.sprite.spritecollide(projectile, self.game.obstacles, False) # Liste mit allen Hindernissen, die das Projektil berühren
            
            for obstacle in hits: # Für alle berühreten Hindernisse (die von Prpjektilen getroffen wurden)
                projectile.check_collision_with_obstacle(obstacle) # Methodenaufruf
    
    def draw(self, screen):
        screen.blit(self.game.background_img, (0, 0))       #1. schicht: hintergrund
        
        self.game.obstacles.draw(screen)            #2. Schicht Hindernisse

        if self.runner:                                 #3. Schicht runner
            screen.blit(self.runner.image, self.runner.rect)
        
        self.game.projectiles.draw(screen)          #4. Schicht Projektile

        if self.checkpoint:                         #5. schicht checkpoint
            screen.blit(self.checkpoint.image, self.checkpoint.rect)

        if self.cannon:                             #6. schicht cannon
            screen.blit(self.cannon.image, self.cannon.rect)