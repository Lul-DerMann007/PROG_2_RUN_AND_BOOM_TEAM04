import pygame 
from settings import *

class Checkpoint(pygame.sprite.Sprite):
    def __init__(self, game, x: float):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        
        # Attribute passend zu, UML-Design
        self.is_reached: bool = False
        
        # Visuelle Darstellung (Platzhalter)
        self.image = pygame.Surface((CHECKPOINT_WIDTH, CHECKPOINT_HEIGHT))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, 0))
        
    def update(self, dt: float):
       
        # Anpassung der Position basierend auf der Scroll-Geschwindigkeit (Geschwindigkeit der Map)
        self.rect.x -= SCROLL_SPEED * dt
   
    #Checkpoint erreicht Logik
    def check_reached(self,runner):
        if not self.is_reached and self.rect.colliderect(runner.rect):  #prüft, ob checkpoint noch nicht erreicht ist und runner und checkpoint überlappen
            self.is_reached = True              #wenn die überlappen, wird self.is_reached auf True gestellt
            self.game.checkpoint_reached()      #game.py wird benachrichtigt

