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
LIGHTGRAY = (200, 200, 200)

#  Einstellungen Darstellung des Runners
RUNNER_SIZE = 70
RUNNER_WIDTH = 70
RUNNER_HEIGHT = 70 
RUNNER_COLOR = BLUE

# Bewegung des runners
RUNNER_ACC = 2200               # Beschleunigung in pixel pro sekunden, für spätere ziellogik wichtig
RUNNER_FRICTION = -6.0          # reibung bzw. abbremsung
RUNNER_SMOOTH_FACTOR = 10.0     # zwischen den ebenen smoother übergang
RUNNER_MAX_SCREEN = 4 / 5       # Wie weit der Runner nach rechts laufen darf (Anteil der Bildschirmbreite)
RUNNER_LEFT_PACE_FACTOR = 1.8   # Geschwindigkeitsmultiplikator, wenn der Runner nach links läuft
RUNNER_MAX_X_LEFT_FACTOR = 0.4  # Wie weit der Runner nach links laufen darf = Gamer Over
LANE_SWITCH_SPEED_RUNNER = 25

# Einstellungen der Kanone
CANNON_WIDTH = 90
CANNON_HEIGHT = 90
CANNON_OFFSET = 80 
CANNON_COOLDOWN = 0.3
CANNON_SMOOTH_FACTOR = 8.0
CANNON_COLOR = RED
LANE_SWITCH_SPEED_CANNON = 27

# Projektil der Kanone 
PROJECTILE_WIDTH = 32
PROJECTILE_HEIGHT = 32
PROJECTILE_SPEED = 1150
PROJECTILE_COLOR = ORANGE       # Pixel/Sekunde nach links

#Ebenen/Lanes System, finale Logik Stand: 16.11 Jonte und Mares
NUM_LANES = 8
LANE_HEIGHT = HEIGHT // NUM_LANES 


#Hindernisse =  NEU: eingeführte Konstanzen
OBSTACLE_BASE_WIDTH = 60    #Basis mit der multibliziert wird
OBSTACLE_TYPE_SHORT = 2     #multiplikator kurze Hindernisse
OBSTACLE_TYPE_LONG = 6      #multiplikator lange hindernisse
OBSTACLE_GAP  = 250         #mindestasbstand zwischen den blöcken beim spawnin
OBSTACLE_HEIGHT = 90        #Höhe = Ebenenhöhe
OBSTACLE_SPAWN_INTERVAL = 0.55  #Neues Obstacle balancing tool ausgelagert aus gameworld
SCROLL_SPEED = 400       # Geschwindigkeit, mit der Hindernisse scrollen
OBSTACLE_COLOR = GRAY

# Einstellungen des Checkpoints
CHECKPOINT_DISTANCE = 10000
CHECKPOINT_WIDTH = 60
CHECKPOINT_HEIGHT = HEIGHT  #evtl. checkpoint größe noch anpassen später, stand jetzt ganzer bildschirm lang
CHECKPOINT_COLOR = GREEN

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
# UI_FONT_SIZE = 36
# UI_FONT_SIZE_LARGE = 72
UI_FONT_SIZE = 25
UI_FONT_SIZE_LARGE = 50
UI_MARGIN = 20
UI_LINE_SPACING = 40
UI_OVERLAY_ALPHA = 200

# Eingabefelder für Spielernamen
MAX_NAME_LENGTH = 15
INPUT_BOX_WIDTH = 400
INPUT_BOX_HEIGHT = 50