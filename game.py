# game.py

import pygame as pg
from settings import *
from gameworld import GameWorld
from player import Player

class Game:
    
    #Das ist die entscheidende Hauptklasse des Spiels (Context). Verwaltet Initialisierung, den Game Loop und den Spielzustand.
    
    
    def __init__(self):
        # Initialisierung und Fenster erstellen
        pg.init() 
        
        try:
            pg.mixer.init()
        except Exception:
            print("Audio mixer fehlgeschlagen, weiter ohne audio")
        
        # Fenster erstellen und Einstellungen setzen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE) 
        
        # Zeitmodule und interne Zustände
        self.clock = pg.time.Clock()
        self.running = True
        
        self.all_sprites = pg.sprite.Group()    #alle sprites werden in einer gruppe gespeichert (sehr leicht so aufzurufen)
        self.obstacles = pg.sprite.Group()      #nur für hindernisse (kollisionen)  !Spätere Implementierung!
        self.projectiles = pg.sprite.Group()    #nur für projektile (kollisionen) !Spätere Implementierung!
        
        #Player Objekte erstellen
        self.player1 = Player("Spieler 1", PLAYER1_CONTROLS)
        self.player2 = Player("Spieler 2", PLAYER2_CONTROLS)

        #referenz auf aktuelle rollen (!Später!)
        self.current_runner = None
        self.current_cannon = None

        #Zustände für Score-System              #Anpassungen Jonte 06.12 22:51
        self.current_round_num = 0 
        self.game_state = "menu"
        self.last_point_reason = None
        self.set_won_message = None            
                            

        #Spielwelt erstellen
        self.world = GameWorld(self)

        #Initialisierung von zwei Schriftgrößen (Überschrift + normal)              #eingefügt Jonte 06.12 23:02
        self.font = pg.font.Font(None, 36)  #normale UI schriftgröße
        self.font_large = pg.font.Font(None, 72)    #größere UI Schriftgröße/Überschriften

    def start_game(self):
        self.player1.reset()
        self.player2.reset()

        self.player1.role = "runner"
        self.player2.role = "cannon"
        self.current_runner = self.player1 
        self.current_cannon = self.player2

        self.current_round_num = 1
        self.game_state = "running"
        self.last_point_reason = None
        self.set_won_message = None

        self.start_round()

    def start_round(self):
        self.game_state = "running"
        self.last_point_reason = None
        self.set_won_message =  None

        runner_ctrls = self.current_runner.controls
        cannon_ctrls = self.current_cannon.controls

        self.world.setup_round()


    def checkpoint_reached(self):                               #Logik des Runden Siegs vom Runner bei erreichtem Checkpoint
        self.last_point_reason = None   
        self.current_runner.win_round()
        self.process_round_result(winner=self.current_runner)   

    def cannon_scores(self, reason="hit"):
        self.last_point_reason = reason
        self.current_cannon.win_round()
        self.process_round_result(winner=self.current_cannon)

    def process_round_result(self, winner):
        self.game_state =  "round_end"
        self.set_won_message = None

        if winner.round_score >= ROUNDS_TO_WIN_SET:
            winner.win_set()
            self.set_won_message = f"{winner.name} gewinnt den Satz!"
            self.player1.round_score = 0
            self.player2.round_score = 0

            if winner.set_score >= SETS_TO_WIN_MATCH:
                self.game_state = "game_over"
    
    def next_round(self):
        self.current_round_num += 1
        self.switch_roles()
        self.start_round()
    
    def switch_roles(self):
        self.player1.switch_role()
        self.player2.switch_role()
        if self.player1.role == "runner":
            self.current_runner = self.player1
            self.current_cannon = self.player2
        else:
            self.current_runner = self.player2
            self.current_cannon = self.player1
    
    def reset_game(self):
        self.game_state = "menu"
        self.player1.reset()
        self.player2.reset()
        self.current_round_num = 0
        self.last_point_reason = None

    def events(self):   #Events: Verarbeitet alle Benutzer- und Systemereignisse.
        # Wenn Nutzer fenster schließt oder ESC drückt, wird das Spiel beendet
        for event in pg.event.get():
            if event.type == pg.QUIT:
               return False
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return False
                
                if self.game_state == "menu":
                    if event.key == pg.K_SPACE:
                        self.start_game()
                
                elif self.game_state == "round_end":
                    if event.key == pg.K_SPACE:
                        self.next_round()

                elif self.game_state == "game_over":
                    if event.key == pg.K_SPACE:
                        self.reset_game()
        return True

            
    def update(self,dt):
        # zentrale Update-Logik, aufgerufen pro Frame (dt=Deltatime), steuert wann die welt aktualisiert wird
        if self.game_state == "running":
            self.world.update(dt)

    def draw(self):
        if self.game_state in ["running","round_end"]:
            self.world.draw(self.screen)

        self.draw_ui()

        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "round_end":
            self.draw_round_end()
        elif self.game_state == "game_over":
            self.draw_game_over()
        
        pg.display.flip()

    def draw_ui(self):
        p1_title = self.font.render("SPIELER 1 (BLAU)", True, BLUE)
        p1_score = self.font.render(f"Sätze: {self.player1.set_score} | Runden: {self.player1.round_score}", True, BLACK) 
        
        self.screen.blit(p1_title, (20, 20))
        self.screen.blit(p1_score, (20, 55))
        
        p2_title = self.font.render("SPIELER 2 (ROT)", True, RED)
        p2_score = self.font.render(f"Sätze: {self.player2.set_score} | Runden: {self.player2.round_score}", True, BLACK)
        
        self.screen.blit(p2_title, (WIDTH - 250, 20)) 
        self.screen.blit(p2_score, (WIDTH - 250, 55))
        
        if self.game_state == "running":
            info_text = f"Satz-Ziel: {ROUNDS_TO_WIN_SET} Runden"
            info_surf = self.font.render(info_text, True, GRAY)
            info_rect = info_surf.get_rect(center=(WIDTH // 2, 30))
            self.screen.blit(info_surf, info_rect)
            
            role_text = f"Runner: {self.current_runner.name} | Kanone: {self.current_cannon.name}"
            role_surf = self.font.render(role_text, True, YELLOW)
            role_r = role_surf.get_rect(center=(WIDTH//2, 70))
            self.screen.blit(role_surf, role_r)
            
    def draw_menu(self):
        # Zeichnet das Hauptmenü
        self.screen.fill(BLACK)
        title_surface = self.font_large.render("RUN & BOOM", True, WHITE)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        self.screen.blit(title_surface, title_rect)
        
        instructions = [
            "Spieler 1 (WASD): Runner in Runde 1",
            "Spieler 2 (Pfeiltasten): Kanone in Runde 1",
            "Rollenwechsel nach jeder Runde!",
            "",
            f"Ziel: {ROUNDS_TO_WIN_SET} Runden = 1 Satz",
            f"Matchsieg: {SETS_TO_WIN_MATCH} Saetze",
            "",
            "LEERTASTE zum Starten"
        ]
        y = HEIGHT // 2
        
        for line in instructions:
            text_surface = self.font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, y))
            self.screen.blit(text_surface, text_rect)
            y += 40
            
    def draw_round_end(self):
        # Zeichnet den Endscreen einer Runde
        overlay = pg.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Nachricht über Runden-Ergebnis
        if self.world.checkpoint and self.world.checkpoint.is_reached:
            text = f"{self.current_runner.name} erreicht das Ziel!"
            color = BLUE if self.current_runner == self.player1 else RED
        else:
            if self.last_point_reason == "pushed_off":
                text = "Runner vom Bildschirm gedraengt!"
            else:
                text = "Runner abgeschossen!"
            color = RED if self.current_cannon == self.player2 else BLUE
            
        text_surface = self.font_large.render(text, True, color)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
        self.screen.blit(text_surface, text_rect)
        
        # Satz gewonnen?
        if self.set_won_message:
            set_surf = self.font_large.render(self.set_won_message, True, YELLOW)
            set_rect = set_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(set_surf, set_rect)
        else:
            score_text = f"Runden-Stand: {self.player1.round_score} : {self.player2.round_score}"
            score_surf = self.font.render(score_text, True, WHITE)
            score_rect = score_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(score_surf, score_rect)
        
        continue_surface = self.font.render("LEERTASTE fuer naechste Runde", True, WHITE)
        continue_rect = continue_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
        self.screen.blit(continue_surface, continue_rect)
        
    def draw_game_over(self):
        # Zeichnet den Endscreen des Matches
        self.screen.fill(BLACK)
        
        if self.player1.set_score > self.player2.set_score:
            winner = self.player1
        else:
            winner = self.player2
            
        text = f"{winner.name} GEWINNT DAS MATCH!"
        text_surface = self.font_large.render(text, True, GREEN)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        self.screen.blit(text_surface, text_rect)
        
        score_text = f"Satz-Endstand: {self.player1.set_score} : {self.player2.set_score}"
        score_surface = self.font.render(score_text, True, WHITE)
        score_rect = score_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(score_surface, score_rect)
        
        restart_surface = self.font.render("LEERTASTE fuer neues Spiel", True, WHITE)
        restart_rect = restart_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        self.screen.blit(restart_surface, restart_rect)

    def run(self):      #Gameloop (läuft so lange self.running True ist)
        while self.running:                     
            dt_ms = self.clock.tick(FPS)
            dt_s = dt_ms / 1000             #zeit messung (framerate)                             
            if not self.events():
                self.running = False      
            
            self.update(dt_s)  #spielstand für aktuellen frame aktualisieren
            self.draw() 

        # Schließen des Programms, wenn Schleife beendet ist
        pg.quit()