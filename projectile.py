import pygame as pg
from pygame.math import Vector2 as vec
from settings import *


class Projectile(pg.sprite.Sprite):
    def __init__(self, game, x: float, y: float, color):            #Farbe der Cannone wird hier entnommen 
        self.groups = game.all_sprites, game.projectiles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.color = color

        #Grafik der richtigen Farbe laden
        if self.color == "blue":
            self.image = self.game.projectile_blue_img.copy()
        else:
            self.image = self.game.projectile_red_img.copy()

        self.rect = self.image.get_rect(center=(x, y))

        # Bewegung
        self.speed = PROJECTILE_SPEED     # Pixel pro Sekunde
        self.pos = vec(x, y)                     # exakte Position
        self.vel = vec(-self.speed, 0)           # fliegt nach links

        self.active = True

    def update(self, dt: float):
        # Bewegt das Projektil und entfernt es, wenn es aus dem Bild ist.
        if not self.active:
            return

        # Position aktualisieren: v * t
        self.pos += self.vel * dt
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        # Aus dem Bild nach links geflogen? Dann entfernen
        if self.rect.right < 0:
            self.kill_me()

    def kill_me(self):
        # Entfernt das Projektil aus allen Sprite-Gruppen.
        self.active = False
        self.kill()


    def check_collision_with_runner(self,runner):              #Jonte Anpassungen 16:34 !Später! darunter check_collisions_with_obstacle
        if self.active and self.rect.colliderect(runner.rect):

            s = getattr(self.game, 'sfx_proj_hit_runner',None)      #Soundeffekte bei Treffer
            if s: s.play()

            # pg.tim e.delay(600)                                      #Idee con Claude AI, damit Sound Timing optimiert ist           Tim- Nicht ganz zufrieden mit der Lösung Sound hört sich dennoch leicht versetzt an, ggf später ändern 

        self.game.cannon_scores(reason = "hit")
        self.kill_me()

    def check_collision_with_obstacle(self, obstacle):
        if self.active and self.rect.colliderect(obstacle.rect): # self.active verhindert, dass ein Projekti, das im selben Frame 2 Hindernisse trifft, doppelt zählt
            self.deactivate()
            
    def deactivate(self):
        self.active = False
        self.kill()