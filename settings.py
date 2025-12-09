import pygame as pg

#  Alle festen globalen Werte, die das Spiel definieren sind in diesem Modul settings
#  Bildschrimgröße und Frames per Second (FPS)
WIDTH = 1280         # Breite des Spielfensters in Pixeln
HEIGHT = 720         # Höhe des Spielfensters in Pixeln
FPS = 60             # Ziel-Bildwiederholrate
TITLE = "Run & Boom" # Fenstertitel

#Score-Regeln / Satz System             # Hinzugefügt von Jonte 06.12 21:00
ROUNDS_TO_WIN_SET = 3                       
SETS_TO_WIN_MATCH = 3

# Farben (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
DARKGRAY = (40, 40, 40)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

#  Einstellungen Darstellung des Runners
RUNNER_SIZE = 40
RUNNER_COLOUR = BLUE

# Bewegung des runners
RUNNER_ACC = 400       # Beschleunigung in pixel pro sekunden, für spätere ziellogik wichtig
RUNNER_FRICTION = -0.25     #reibung bzw. abbremsung
RUNNER_SPEED = 400
RUNNER_SMOOTH_FACTOR = 10.0         #zwischen den ebenen smoother übergang
RUNNER_MAX_SCREEN = 4 / 5   # Wie weit der Runner nach rechts laufen darf (Anteil der Bildschirmbreite)

# Einstellungen der Kanone
CANNON_WIDTH = 60
CANNON_HEIGHT = 40
CANNON_OFFSET = 80 
CANNON_COOLDOWN = 0.3
CANNON_SMOOTH_FACTOR = 8.0
CANNON_COLOUR = RED

# Projektil der Kanone 
PROJECTILE_WIDTH = 10
PROJECTILE_HEIGHT = 10
PROJECTILE_SPEED = 600
PROJECTILE_COLOUR = ORANGE       # Pixel/Sekunde nach links

#Ebenen/Lanes System, finale Logik Stand: 16.11 Jonte und Mares
NUM_LANES = 8
LANE_HEIGHT = HEIGHT // NUM_LANES 
LANE_SWITCH_SPEED = 0.15

#Hindernisse =  NEU: eingeführte Konstanzen
OBSTACLE_BASE_WIDTH = 60    #Basis mit der multibliziert wird
OBSTACLE_TYPE_SHORT = 2     #multiplikator kurze Hindernisse
OBSTACLE_TYPE_LONG = 6      #multiplikator lange hindernisse
OBSTACLE_GAP  = 250         #mindestasbstand zwischen den blöcken für später
OBSTACLE_HEIGHT = 90        #Höhe = Ebenenhöhe
SCROLL_SPEED = 400       # Geschwindigkeit, mit der Hindernisse scrollen
OBSTACLE_COLOUR = GRAY

# Einstellungen des Checkpoints
CHECKPOINT_DISTANCE = 10000
CHECKPOINT_WIDTH = 60
CHECKPOINT_HEIGHT = HEIGHT  #evtl. checkpoint größe noch anpassen später, stand jetzt ganzer bildschirm lang
CHECKPOINT_COLOUR = GREEN

# Steuerung (Wird in player.py genutzt)   Änderung Jonte 06.12 20:50 Strings als Pygame Konstanten abgespeichert (ermöglicht den Rollenwechsel)
PLAYER1_CONTROLS = {
    'up': pg.K_w, 
    'down': pg.K_s,
    'left': pg.K_a,         
    'right': pg.K_d
    }

PLAYER2_CONTROLS = {
    'up': pg.K_UP, 
    'down': pg.K_DOWN, 
    'left': pg.K_LEFT,          
    'right': pg.K_RIGHT         
    }

#UI magische zahlen ausgelagert
UI_FONT_SIZE = 36
UI_FONT_SIZE_LARGE = 72
UI_MARGIN = 20
UI_LINE_SPACING = 40
UI_OVERLAY_ALPHA = 200

