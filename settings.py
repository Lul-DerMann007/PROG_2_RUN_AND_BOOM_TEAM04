#   Alle festen globalen Werte, die das Spiel definieren sind in diesem Modul settings
#  Bildschrimgröße und Frames per Second (FPS)
WIDTH = 1280         # Breite des Spielfensters in Pixeln
HEIGHT = 720         # Höhe des Spielfensters in Pixeln
FPS = 60             # Ziel-Bildwiederholrate
TITLE = "Run & Boom" # Fenstertitel

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

# horizontale bewegung
RUNNER_ACC = 400       # Beschleunigung in pixel pro sekunden, für spätere ziellogik wichtig
RUNNER_FRICTION = -0.25     #reibung bzw. abbremsung
RUNNER_SPEED = 400

#vertikale bewegung
LANE_SWITCH_SPEED = 0.15
RUNNER_SMOOTH_FACTOR = 10.0

#runner einstellungen
RUNNER_SIZE = 40
RUNNER_COLOR = BLUE

# Cannon setting
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

#Hindernisse
OBSTACLE_WIDTH = 60
OBSTACLE_HEIGHT = 60
OBSTACLE_COLOUR = GRAY

#checkpoint setting
CHECKPOINT_DISTANCE = 3000
CHECKPOINT_WIDTH = 60
CHECKPOINT_HEIGHT = HEIGHT  #evtl. checkpoint größe noch anpassen später
CHECKPOINT_COLOUR = GREEN

# Steuerung (Wird in player.py genutzt)
PLAYER1_CONTROLS = {'up': 'w', 'down': 's', 'left': 'a', 'right': 'd'}
PLAYER2_CONTROLS = {'up': 'up', 'down': 'down', 'shoot': 'left'}

SCROLL_SPEED = 400       # Geschwindigkeit, mit der Hindernisse scrollen

SCORE_LIMIT = 3