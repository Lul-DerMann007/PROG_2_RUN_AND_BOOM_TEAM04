import pygame as pg 
from settings import *
class Checkpoint(pg.sprite.Sprite):
    def __init__(self, game, x: float):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
        #Grafik wird geladen
        self.image = self.game.checkpoint_img.copy()
        self.rect = self.image.get_rect()

        self.rect.center = (x,HEIGHT // 2)
        # Attribute passend zu, UML-Design
        self.is_reached: bool = False
        
        
        
    def update(self, dt: float):
       
        # Anpassung der Position basierend auf der Scroll-Geschwindigkeit (Geschwindigkeit der Map)
        self.rect.x -= SCROLL_SPEED * dt
   
    #Checkpoint erreicht Logik
    def check_reached(self,runner):
        if self.is_reached:
            return  #prüft, ob checkpoint noch nicht erreicht ist und runner und checkpoint überlappen
        if runner.pos.x >= self.rect.left:   #Bugfix mi Gemini. Prompt: Ich habe diese Funktion zur Checkpoint Erreichung erstellt. Ich bekomme eine Fehlermeldung, das ich string nicht mit tupel vergleichen kann. Wie kann ich die Mitte des Checkpoints vergleichen?
            self.is_reached = True              #wenn die überlappen, wird self.is_reached auf True gestellt
            self.game.checkpoint_reached()      #game.py wird benachrichtigt

