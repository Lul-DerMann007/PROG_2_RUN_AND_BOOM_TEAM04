# player.py
# Die Player-Klasse repräsentiert den menschlichen Spieler bzw Nutzer, nicht die Spielfigur.

class Player:
    
    def __init__(self, name: str, controls: dict):
        # Attribute (Eigenschaften)
        self.name: str = name       
        self.score: int = 0         
        self.role: str = None       
        self.controls: dict = controls 
        
    def increase_score(self):
        # Methode (Verhalten): Erhöht den Punktestand um 1.
        self.score += 1
        
    def switch_role(self):
        #Methode: Wechselt die Rolle zwischen "runner" und "cannon".
        if self.role == "runner":
            self.role = "cannon"
        else:
            self.role = "runner"
            
    def reset(self):
        # Setzt den Spieler für ein neues Spiel zurück.
        self.score = 0
        self.role = None