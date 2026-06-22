"""
Конфигурация игры
"""

import os

# Размеры окна
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 950
TABLE_MARGIN = 70

# Размеры стола
TABLE_WIDTH = SCREEN_WIDTH - TABLE_MARGIN * 2
TABLE_HEIGHT = SCREEN_HEIGHT - TABLE_MARGIN * 2

# Границы
HALF_LINE = SCREEN_WIDTH // 2

# Цвета
COLORS = {
    'BACKGROUND': (20, 30, 20),
    'TABLE': (15, 80, 35),
    'WOOD': (101, 67, 33),
    'CLOTH': (25, 100, 45),
    'POCKET': (0, 0, 0),
    'POCKET_INNER': (40, 40, 40),
    'LINE': (218, 165, 32),
    'WHITE': (255, 255, 255),
    'YELLOW': (255, 215, 0),
    'RED': (255, 80, 80),
    'GREEN': (80, 255, 80),
    'BLUE': (80, 80, 255),
    'ORANGE': (255, 165, 80),
    'PURPLE': (200, 80, 255),
    'CYAN': (80, 255, 255),
    'PINK': (255, 105, 180),
    'BROWN': (139, 69, 19),
    'GRAY': (128, 128, 128),
    'MAROON': (128, 0, 0),
    'BLACK': (0, 0, 0),
    'GOLD': (255, 215, 0),
    'UI_BG': (0, 0, 0, 180),
    'UI_TEXT': (255, 215, 0),
    'MENU_BG': (30, 30, 50, 240),
    'INPUT_BG': (60, 60, 80, 200),
    'INPUT_ACTIVE': (80, 80, 120, 220),
    'BUTTON': (40, 180, 40),
    'BUTTON_HOVER': (60, 220, 60),
}

# Физика
BALL_RADIUS = 14
FRICTION = 0.985
WALL_BOUNCE_DAMP = 0.95
MAX_POWER = 25

# Лузы
POCKETS = [
    (TABLE_MARGIN, TABLE_MARGIN),
    (SCREEN_WIDTH - TABLE_MARGIN, TABLE_MARGIN),
    (TABLE_MARGIN, SCREEN_HEIGHT - TABLE_MARGIN),
    (SCREEN_WIDTH - TABLE_MARGIN, SCREEN_HEIGHT - TABLE_MARGIN),
    (SCREEN_WIDTH // 2, TABLE_MARGIN),
    (SCREEN_WIDTH // 2, SCREEN_HEIGHT - TABLE_MARGIN),
]
POCKET_RADIUS = 42

# Игровые параметры
WIN_SCORE = 7
NUM_COLOR_BALLS = 15

# Цвета для 15 шаров
COLOR_BALLS = {
    1: (255, 215, 0),      # жёлтый
    2: (0, 0, 200),        # синий
    3: (200, 0, 0),        # красный
    4: (120, 0, 120),      # фиолетовый
    5: (255, 140, 0),      # оранжевый
    6: (0, 150, 0),        # зелёный
    7: (128, 0, 0),        # бордовый
    8: (0, 0, 0),          # чёрный
    9: (255, 215, 0),      # жёлтый полосатый
    10: (0, 0, 200),       # синий полосатый
    11: (200, 0, 0),       # красный полосатый
    12: (120, 0, 120),     # фиолетовый полосатый
    13: (255, 140, 0),     # оранжевый полосатый
    14: (0, 150, 0),       # зелёный полосатый
    15: (128, 0, 0),       # бордовый полосатый
}

# Расстановка
BALL_DISTANCE = BALL_RADIUS * 2 + 2
RIGHT_HALF_CENTER_Y = SCREEN_HEIGHT // 2
TRIANGLE_TIP_X = HALF_LINE + 80
TRIANGLE_TIP_Y = RIGHT_HALF_CENTER_Y
CUE_BALL_X = HALF_LINE - 80
CUE_BALL_Y = RIGHT_HALF_CENTER_Y

# Интерфейс
POWER_BAR_WIDTH = 250
POWER_BAR_HEIGHT = 25

FPS = 60

# Звуки
SOUNDS_DIR = "sounds"
MUSIC_FILE = os.path.join(SOUNDS_DIR, "background_music.mp3")
POCKET_SOUND_FILE = os.path.join(SOUNDS_DIR, "pocket.mp3")
CUE_HIT_SOUND_FILE = os.path.join(SOUNDS_DIR, "cue_hit.mp3")
