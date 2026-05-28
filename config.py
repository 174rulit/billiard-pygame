"""
Конфигурация игры - правильная расстановка как в реальном пуле
Треугольник на правой половине, белый шар на левой
"""

import os
import math

# Размеры окна
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 850
TABLE_MARGIN = 70

# Размеры стола
TABLE_WIDTH = SCREEN_WIDTH - TABLE_MARGIN * 2
TABLE_HEIGHT = SCREEN_HEIGHT - TABLE_MARGIN * 2

# Границы левой и правой половин
HALF_LINE = SCREEN_WIDTH // 2

# Цвета (RGB)
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
    'DARK_GREEN': (0, 100, 0),
    'NAVY': (0, 0, 128),
    'GOLD': (255, 215, 0),
    'BLACK': (0, 0, 0),
    'UI_BG': (0, 0, 0, 180),
    'UI_TEXT': (255, 215, 0),
}

# Физические параметры
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
POCKET_RADIUS = 28

# Игровые параметры
WIN_SCORE = 7
NUM_COLOR_BALLS = 15

# Цвета для 15 шаров (1-7 сплошные, 8 чёрный, 9-15 полосатые)
COLOR_BALLS = {
    1: COLORS['YELLOW'],    # 1 - жёлтый
    2: COLORS['BLUE'],      # 2 - синий
    3: COLORS['RED'],       # 3 - красный
    4: COLORS['PURPLE'],    # 4 - фиолетовый
    5: COLORS['ORANGE'],    # 5 - оранжевый
    6: COLORS['GREEN'],     # 6 - зелёный
    7: COLORS['MAROON'],    # 7 - бордовый
    8: COLORS['BLACK'],     # 8 - чёрный
    9: (255, 180, 180),     # 9 - жёлтый полосатый
    10: (180, 180, 255),    # 10 - синий полосатый
    11: (180, 255, 180),    # 11 - красный полосатый
    12: (255, 180, 255),    # 12 - фиолетовый полосатый
    13: (180, 255, 255),    # 13 - оранжевый полосатый
    14: (255, 255, 180),    # 14 - зелёный полосатый
    15: (200, 150, 255),    # 15 - бордовый полосатый
}

# РАССТАНОВКА КАК В РЕАЛЬНОМ ПУЛЕ
# Расстояние между центрами шаров
BALL_DISTANCE = BALL_RADIUS * 2 + 2

# === ПРАВАЯ ПОЛОВИНА: ТРЕУГОЛЬНИК из 15 шаров ===
# Центр правой половины по Y
RIGHT_HALF_CENTER_Y = SCREEN_HEIGHT // 2
# Треугольник располагается на правой половине
# Вершина треугольника (шар №1) направлена влево (к белому шару)
TRIANGLE_TIP_X = HALF_LINE + 80  # Чуть правее центральной линии
TRIANGLE_TIP_Y = RIGHT_HALF_CENTER_Y

# === ЛЕВАЯ ПОЛОВИНА: БЕЛЫЙ ШАР ===
# Напротив шара №1 (по той же горизонтали)
CUE_BALL_X = HALF_LINE - 80   # Левая половина, напротив вершины треугольника
CUE_BALL_Y = RIGHT_HALF_CENTER_Y

# Параметры интерфейса
POWER_BAR_WIDTH = 250
POWER_BAR_HEIGHT = 25

FPS = 60

# Звуки
SOUNDS_DIR = "sounds"
MUSIC_FILE = os.path.join(SOUNDS_DIR, "background_music.mp3")
POCKET_SOUND_FILE = os.path.join(SOUNDS_DIR, "pocket.mp3")
CUE_HIT_SOUND_FILE = os.path.join(SOUNDS_DIR, "cue_hit.mp3")
