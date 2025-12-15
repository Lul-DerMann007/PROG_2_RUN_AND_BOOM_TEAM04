# Der Runner als ein Sprite
import pygame as pg
from pygame.math import Vector2 as vec
from settings import *

class Runner(pg.sprite.Sprite):
   
    def __init__(self, game, x: float, start_lane: int, controls: dict,color):
        self.groups = game.all_sprites                  
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game                # Referenz auf die Game-Klasse für Scoring
        self.controls = controls
        self.color = color      #Speichert die Farbe des Runners
        self.key_states =  {'up': False, 'down': False}

        if self.color == "blue":
            self.image = self.game.runner_blue_img.copy()
        else:
            self.image = self.game.runner_red_img.copy()
        
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
    
    #Funktion um "unmögliche" Lane-Wechsel zu verhindern 
    def is_target_lane_safe(self, target_lane_index):
        target_y = self.get_lane_y(target_lane_index) #Hier wird die Ziel Position bestimmt
        check_rect = pg.Rect(0, 0, RUNNER_SIZE - 10, RUNNER_SIZE - 10)      #Es wird ein "Testrechteck", welches kleiner als der Runner ist erzeugt 
        check_rect.center = (self.pos.x, target_y)      #Testrechteck wird dort plaziert wo der Runner nachdem Spurwechsel wäre 
        hits = [obs for obs in self.game.obstacles if check_rect.colliderect(obs.rect)]     #Hier wird Kollision geprüft 
        if hits: 
            return False        #Übergabe an get_keys "Lane ist blocked"
        return True             #Übergabe an get_keys "Lane ist Frei"


    def update(self, dt: float):
        self.get_keys()     #eingaben verarbeiten
        
        #Horizontale Bewegung
        self.acc.x += self.vel.x * RUNNER_FRICTION      #reibung anwenden
        self.vel.x += self.acc.x * dt                   #geschwindigkeit aktualisieren
        self.pos.x += self.vel.x * dt + 0.5 * self.acc.x * dt ** 2      #position aktualisieren

        
        #vertikale Bewegung + smoothing kanone und runner. Keine externe smooth_fuktion. KI-generiert mit Claude AI. Prompt: Analysiere nun auf Basis der anderen Module das Modul runner.
        #Suche nach Funktionen und Aspekten, die unlogisch sind und liefer entsprechende Verbesserungen.
        target_y= self.get_lane_y(self.target_lane)
        diff = target_y - self.pos.y

        self.pos.y += diff * LANE_SWITCH_SPEED_RUNNER * dt

        if abs(self.pos.y - target_y) < 1:          #Genaueres Einrasten, wenn nah genug dran
            self.pos.y = target_y
            self.current_lane = self.target_lane

        max_x = WIDTH * RUNNER_MAX_SCREEN       #Begrenzung auf 4/5 Maximalposition nach rechts: einstellbar über RUNNER_MAX_SCREEN in settings.py
        

        # Game Over wenn der Runner zu weit nach links läuft
        if self.pos.x < -RUNNER_WIDTH * RUNNER_MAX_X_LEFT_FACTOR:
            self.game.cannon_scores(reason="pushed_off")
            return
        
        #stoppen am rechten rand / der rechten begrenzung
        if self.pos.x > max_x:
            self.pos.x = max_x
            self.vel.x = 0
                                                    
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def get_keys(self):
        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()
        
            # Horizontale Bewegung
        if keys[self.controls['left']]:
            self.acc.x = -RUNNER_ACC * RUNNER_LEFT_PACE_FACTOR  #Abbremsung wenn nach links gelaufen wird 
        if keys[self.controls['right']]:
            self.acc.x = RUNNER_ACC
        
       #Lane wechsel, nur möglich wenn man nicht  gerade wechselt
        can_switch = abs(self.current_lane - self.target_lane) < 0.1      #Idee von Claude AI. Prompt: Wie kann man die Runner classer vor allem im movement noch weiter optimieren?

        if keys[self.controls['up']]:       #Prüft Wechsel nach Oben
            if not self.key_states['up']:       #kei ngedrückt halten erlauben
                if can_switch:
                    new_lane = self.target_lane - 1
                    if new_lane >= 0 and self.is_target_lane_safe(new_lane):      #Prüft ob die Lane frei ist mit der is_target_lane_safe Funktion 
                            self.target_lane = new_lane             # Wechsel wird freigeben

                            s = getattr(self.game, 'sfx_lane_switch', None)   #Sound Effekte für Lane Swap (Up), kommt nur wenn ein gültiger Sound geladen wurde
                            if s: s.play()

                self.key_states['up'] = True  
        else:
                self.key_states['up'] = False

        if keys[self.controls['down']]:     #Prüft Wechsel nach Unten 
                if not self.key_states['down']:               #kein gedrückt halten erlauben
                    if can_switch:
                        new_lane = self.target_lane + 1 
                        if new_lane < NUM_LANES and self.is_target_lane_safe(new_lane):      
                            self.target_lane = new_lane 

                            s = getattr(self.game, 'sfx_lane_switch', None)   #Sound Effekte für Lane Swap (Down)
                            if s: s.play()

                self.key_states['down'] = True
        else:
            self.key_states['down'] = False
    
    def collide_with_obstacle(self, obstacle):  #Kollision mit Hinderniss
      if self.rect.colliderect(obstacle.rect):          #Die Prüfung wird schon von Gameworld übenrommen, aus sicherheit drin lassen
            left_overlap = self.rect.right - obstacle.rect.left
            right_overlap = obstacle.rect.right - self.rect.left
            
            if left_overlap < right_overlap:
                self.pos.x = obstacle.rect.left - RUNNER_WIDTH // 2
                if self.vel.x > 0:
                    self.vel.x = 0

            else:
                target_x = obstacle.rect.right + RUNNER_WIDTH // 2
                self.pos.x = target_x                              
                if self.vel.x < 0:  
                    self.vel.x = 0

            self.rect.center = self.pos

            
    def reset_position(self, x, lane):
        self.current_lane = lane
        self.target_lane = lane
        self.pos = vec(x, self.get_lane_y(lane))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)