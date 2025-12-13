import pygame as pg
import random
from settings import *

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x: float, lane: int, obstacle_type: int):
        self.groups = game.all_sprites, game.obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
        if obstacle_type == OBSTACLE_TYPE_SHORT:
            self.image = self.game.obstacle_short_img.copy()
        else:  
            self.image = self.game.obstacle_long_img.copy()
        
        
        self.obstacle_type = obstacle_type        #Obstacle Typ speichern

        obstacle_width = obstacle_type * OBSTACLE_BASE_WIDTH
        
        self.rect = self.image.get_rect()
        
        y = lane * LANE_HEIGHT + LANE_HEIGHT // 2               # Position in der Bahn berechnen
        self.rect = self.image.get_rect(center=(int(x), y))
        
    def update(self, dt: float):
        self.rect.x -= SCROLL_SPEED * dt # Bewegung des Hindernisses mit der Welt


        if self.rect.right<0:           #Obstacle wird entfernt wenn es aus dem Bild ist (nicht weiter rendern)
            self.kill()

class ObstacleFactory:                  #Erstellung eines Factory Patterns um die Entscheidung SHORT oder LONG aus der Gameworld Klasse auszulagern 
    @staticmethod
    def create(game, x, lane):
        obstacle_type = random.choice([OBSTACLE_TYPE_SHORT, OBSTACLE_TYPE_LONG])
        return Obstacle(game, x , lane, obstacle_type)