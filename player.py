# player.py
# Die Player-Klasse repräsentiert den menschlichen Spieler bzw Nutzer, nicht die Spielfigur.

class Player:
    
    def __init__(self, name: str, controls: dict, color:  str):
        # Attribute (Eigenschaften)
        self.name: str = name       
        
        #Punktesystem im neuen Satz Modus                           #angepasst von Jonte 06.12 21:54 alles auf neues punktesystem ausrichten
        self.round_score = 0        #gewonnene runden im Satz
        self.set_score = 0          #gewonnene Sätze im Match
        self.score = 0              #Gesamtpunktestand, kann man eventuell noch verwerfen am Ende
        
        self.role: str = None       
        self.controls: dict = controls 
        self.color: str = color
    
    def win_round(self):                                    #increase_score ersetzt durch win_round, sinnvoller bei neuem score-system
        self.round_score += 1   #runde im satz


    def win_set(self):          
        self.set_score += 1

        
    def switch_role(self):
        #Methode: Wechselt die Rolle zwischen "runner" und "cannon".
        if self.role == "runner":
            self.role = "cannon"
        else:
            self.role = "runner"
            
    def reset(self):
        # Setzt den Spieler für ein neues Spiel zurück.
        self.round_score = 0
        self.set_score = 0
        self.role = None