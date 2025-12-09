import pygame as pg
from settings import *

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x: float, lane: int):
        self.groups = game.all_sprites, game.obstacles
        super().__init__(self.groups)
        self.game = game
        self.image = pg.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.image.fill(GRAY)
        y = lane * LANE_HEIGHT + LANE_HEIGHT // 2 # Position in der Bahn berechnen
        self.rect = self.image.get_rect(center=(int(x), y))
        
    def update(self, dt: float):
        self.rect.x -= SCROLL_SPEED * dt # Bewegung des Hindernisses mit der Welt


        if self.rect.right<0:           #Obstacle wird entfernt wenn es aus dem Bild ist (nicht weiter rendern)
            self.kill()


    #Hinderniss Spawn Logik !Später!