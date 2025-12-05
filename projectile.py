import pygame
from pygame.math import Vector2 as vec
from settings import *


class Projectile(pygame.sprite.Sprite):
    def __init__(self, game, x: float, y: float):
        super().__init__()
        self.game = game

        # Darstellung: kleiner "Ball"
        self.image = pygame.Surface((PROJECTILE_WIDTH, PROJECTILE_HEIGHT))
        self.image.fill(PROJECTILE_COLOUR)                      # vorher: YELLOW
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


# class Projectile(pygame.sprite.Sprite):
#     def __init__(self, game, x, y):
#         pygame.sprite.Sprite.__init__(self)
#         self.game = game
#         self.image = pygame.Surface((PROJECTILE_WIDTH, PROJECTILE_HEIGHT))
#         self.image.fill(YELLOW)
#         self.rect = self.image.get_rect(center=(x, y))
#         self.speed: float = PROJECTILE_SPEED
#         self.active: bool = True
        
#     def update(self, dt: float):
#         pass

#     def kill_me(self):
#         self.kill()