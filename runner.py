# Der Runner als ein Sprite
import pygame as pg
from pygame.math import Vector2 as vec
from settings import *

def smooth_target_transition(current_Y: float, target_y: float, dt: float, smooth_factor: float):          # die Funktion ist Ki generiert mit Claude AI. Prompt: "Erstelle eine Python Funktion auf Basis des beigelegten Codes, mit den notwendigen Parametern,++ wie die aktuelle Y-Position, die Ziel Y Position und Deltatime. Diese Funktion soll die aktuelle Y-Position des Runners und später der Cannon sanft in Richtung der Ziel-Y Position bewegen. Dadurch sollte der Übergang maximal fließend wirken. Die Bewegung sollte entsprechend von der Delta Time (dt) aus dem Game Loop abhängen. Erkläre bitte zusätzlich, wie man die Funktion anschließend in der Klasse implementiert" 
    if abs(current_Y - target_y) > 1.0:
        diff = target_y - current_Y
        return current_Y + diff * smooth_factor * dt                           #die Funktion sollte noch in die Klasse selber implementiert werden
    else:
        return target_y

class Runner(pg.sprite.Sprite):
   
    def __init__(self, game, x: float, start_lane: int, controls: dict):
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game # Referenz auf die Game-Klasse für Scoring
        self.controls = controls
        
        # Zustand (Attribute)
        self.image = pg.Surface((RUNNER_SIZE, RUNNER_SIZE))
        self.image.fill(RUNNER_COLOUR)
        self.rect = self.image.get_rect()

        #Lane/Ebenen System
        self.current_lane = start_lane 
        self.target_lane = start_lane
        
        # Bewegung (als Float-Vektor für exakte Bewegung) 
        self.pos = vec(x, self.get_lane_y(start_lane)) #Position
        self.vel = vec(0, 0) # Velocity (X-Geschwindigkeit)
        self.acc = vec(0, 0)
    def get_lane_y(self,lane):
        return lane * LANE_HEIGHT + LANE_HEIGHT // 2    #berechnet y-pixel position in der mitte einer lane

    def update(self, dt: float):
        self.get_keys()     #eingaben verarbeiten
        
        #Horizontale Bewegung
        self.pos.x += self.vel.x * dt 

        if self.pos.x < -RUNNER_SIZE:                               #links raus wenn runner mehr als seine eigene größe links raus ist
            self.game.cannon_scores(reason = "pushed_off")
            return
        
        #vertikale Bewegung + smoothing funktion für kanone und runner
        target_y= self.get_lane_y(self.target_lane)
        self.pos.y = smooth_target_transition(self.pos.y, target_y, dt,RUNNER_SMOOTH_FACTOR)
        
        if self.pos.y == target_y:
            self.current_lane = self.target_lane
        
        max_x = WIDTH * RUNNER_MAX_SCREEN   # Maximalposition nach rechts: einstellbar über RUNNER_MAX_SCREEN in settings.py

        if self.pos.x > max_x:
            self.pos.x = max_x
            self.vel.x = 0
                                                    
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def get_keys(self):
        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()
        
        self.vel.x = 0  
            # Horizontale Bewegung
        if keys[self.controls['left']]:
            self.vel.x = -RUNNER_SPEED
        if keys[self.controls['right']]:
            self.vel.x = RUNNER_SPEED
        
       #Lane wechsel, nur möglich wenn man nicht  gerade wechselt

        if self.current_lane == self.target_lane:

            if keys[self.controls['up']]:
                if self.target_lane > 0:
                    self.target_lane -= 1

            if keys[self.controls['down']]:
                if self.target_lane < NUM_LANES - 1:
                    self.target_lane += 1     

    def collide_with_obstacle(self, obstacle):  #Kollision mit Hinderniss
        # Wird von der GameWorld aufgerufen + muss noch hinzugefügt werden !Später!
        pass
        
    def reset_position(self, x, lane):
        self.current_lane = lane
        self.target_lane = lane
        self.pos = vec(x, self.get_lane_y(lane))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)