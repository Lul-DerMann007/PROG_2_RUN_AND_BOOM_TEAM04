import pygame 
from settings import *

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x: float, lane: int):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.image.fill(GRAY)
        y = lane * LANE_HEIGHT + LANE_HEIGHT // 2 # Position in der Bahn berechnen
        self.rect = self.image.get_rect(center=(int(x), y))
        
    def update(self, dt: float):
        self.rect.x -= SCROLL_SPEED * dt # Bewegung des Hindernisses mit der Welt