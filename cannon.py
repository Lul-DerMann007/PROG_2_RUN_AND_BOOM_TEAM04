import pygame as pg
from pygame.math import Vector2 as vec
from settings import *
from projectile import Projectile

def smooth_target_transition(current_Y: float, target_y: float, dt: float, smooth_factor):      
    #Funktion ist Ki-generiert und übernommen aus der runner class. Prompt ist dort beigelegt.
    if abs(current_Y - target_y) > 1.0:
        diff = target_y - current_Y
        return current_Y + diff * smooth_factor * dt
    else:
        return target_y

class Cannon(pg.sprite.Sprite):                     
    #Kanone am rechten Rand, die lane-basiert vertikal bewegt wird und mit Pfeil-links schießt.
    def __init__(self, game, start_lane: int,controls: dict,color):              
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)  
        self.game = game
        self.controls = controls
        self.color = color 
        
        if self.color == "blue":
            self.image = self.game.cannon_blue_img.copy()
        else:
            self.image = self.game.cannon_red_img.copy()

        self.rect = self.image.get_rect()


        # Lane-System (exakt wie beim Runner)
        self.current_lane = start_lane
        self.target_lane = start_lane

        # Position (x fest, y aus Lane)
        self.pos = vec(WIDTH - CANNON_OFFSET, self.get_lane_y(start_lane))

        # schuss steuerung
        self._left_was_pressed = False
        self.shoot_cooldown = 0.0   

        self.key_down_pressed = False
        self.key_up_pressed = False        

        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def get_lane_y(self, lane: int) -> float:
        #Y-Position in der Mitte einer Lane.
        return lane * LANE_HEIGHT + LANE_HEIGHT // 2

    def handle_input(self):
        keys = pg.key.get_pressed()
        # Nur wenn wir die Ziel-Lane erreicht haben, darf eine neue gewählt werden
        if self.current_lane == self.target_lane:

            # eine Lane nach oben (entspricht Runner: W/SPACE) 'up' und 'down' implementieren, da wir tasten übergeben wollen
            if keys[self.controls['up']]:                                                                                      
                if self.target_lane > 0:
                    self.target_lane -= 1

            # eine Lane nach unten (entspricht Runner: S)
            if keys[self.controls['down']]:   
                if self.target_lane < NUM_LANES - 1:
                    self.target_lane += 1

        # Schießen mit linkem Pfeil (mit Debounce) bzw. A bei WASD 
        if keys[self.controls['left']] and not self._left_was_pressed:
            self.shoot()

        # Tastenzustand für das nächste Frame merken, verhindert das dauerhafte schießen        #Anregung von ChatGPT. Prompt: mit welcher pygame funktion kann man abfragen, ob eine taste im Zustand gedrückt ist?
        self._left_was_pressed = keys[self.controls['left']]                                                  #Antwort von ChatGPT: "Funktion: pygame.key.get_pressed()--> gibt eine Liste zurück, die den Zustand der Taste enthält"

    def shoot(self):
        # Erzeugt ein Projektil und fügt es in die Sprite-Gruppen der GameWorld ein.
        # Cooldown: wenn noch > 0, nicht schießen
        if self.shoot_cooldown > 0.0:
            return

        # Austrittspunkt: linke Seite der Kanone
        x = self.pos.x - CANNON_WIDTH // 2
        y = self.pos.y

        projectile = Projectile(self.game, x, y, self.color)        #Farbe wird an Projectile übergeben
        
        self.shoot_cooldown = CANNON_COOLDOWN       #cooldown setzen

    def update(self, dt: float):
        # Lane-basierte Bewegung wie beim Runner + Schuss-Cooldown.
        self.handle_input()

        # Cooldown herunterzählen
        if self.shoot_cooldown > 0.0:
            self.shoot_cooldown -= dt               
            if self.shoot_cooldown < 0.0:
                self.shoot_cooldown = 0.0

        # Vertikale Bewegung – identisch zum Runner
        target_y = self.get_lane_y(self.target_lane)
        self.pos.y = smooth_target_transition(self.pos.y, target_y, dt, CANNON_SMOOTH_FACTOR)
        
        # if self.pos.y == target_y:
        #     self.current_lane=self.target_lane

        # Sanfter Lane-Wechsel
        target_y = self.get_lane_y(self.target_lane)
        diff = target_y - self.pos.y
        self.pos.y += diff * (LANE_SWITCH_SPEED * 1.2) * dt # 20% schneller
        
        if abs(diff) < 1:
            self.pos.y = target_y
            self.current_lane = self.target_lane

        # x bleibt fix, nur y ändert sich
        self.rect.center= (int(self.pos.x), int(self.pos.y))

        
    def reset_position(self, start_lane):
        #Kanone zurücksetzen
        self.current_lane = start_lane
        self.target_lane = start_lane
        self.pos.y = self.get_lane_y(start_lane)
        self.can_shoot = True
        self.shoot_cooldown = 0.0
        
        for p in self.projectiles:
            p.kill()
        self.projectiles = []

    def get_keys(self):
        keys = pg.key.get_pressed()
        
        if keys[self.controls['up']]:
            if not self.key_up_pressed: 
                if self.target_lane > 0:
                    self.target_lane -= 1
                self.key_up_pressed = True
        else:
            self.key_up_pressed = False

        if keys[self.controls['down']]:
            if not self.key_down_pressed:
                if self.target_lane < NUM_LANES - 1:
                    self.target_lane += 1
                self.key_down_pressed = True
        else:
            self.key_down_pressed = False        