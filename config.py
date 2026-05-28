"""
Конфигурация игры - все магические числа вынесены сюда
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
    'PLAYER1_BG': (50, 50, 80, 200),
    'PLAYER2_BG': (80, 50, 50, 200),
}

# Физические параметры
BALL_RADIUS = 14
FRICTION = 0.985
WALL_BOUNCE_DAMP = 0.95
MAX_POWER = 25
POWER_BAR_WIDTH = 250
POWER_BAR_HEIGHT = 25

# Лузы (координаты)
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

# Цвета для 15 шаров (как в классическом пуле)
COLOR_BALLS = [
    COLORS['YELLOW'],   # 1
    COLORS['BLUE'],     # 2
    COLORS['RED'],      # 3
    COLORS['PURPLE'],   # 4
    COLORS['ORANGE'],   # 5
    COLORS['GREEN'],    # 6
    COLORS['MAROON'],   # 7
    COLORS['BLACK'],    # 8
    (255, 180, 180),    # 9 (жёлтый полосатый)
    (180, 180, 255),    # 10 (синий полосатый)
    (180, 255, 180),    # 11 (красный полосатый)
    (255, 180, 255),    # 12 (фиолетовый полосатый)
    (180, 255, 255),    # 13 (оранжевый полосатый)
    (255, 255, 180),    # 14 (зелёный полосатый)
    (200, 150, 255),    # 15 (бордовый полосатый)
]

# РАССТАНОВКА КАК НА СКРИНШОТЕ POOLIANS
# Треугольник внизу справа (или внизу)
# Расстояние между центрами шаров
BALL_DISTANCE = BALL_RADIUS * 2 + 2

# Треугольник располагается внизу стола (ближе к игроку)
# Как на скриншоте - треугольник в нижней части
TRIANGLE_BASE_X = SCREEN_WIDTH - TABLE_MARGIN - 150  # Смещён вправо
TRIANGLE_BASE_Y = SCREEN_HEIGHT - TABLE_MARGIN - 100  # Внизу

# БЕЛЫЙ ШАР (биток) - на противоположной стороне (вверху слева для разнообразия)
# Как на скриншоте - биток может быть вверху или слева
CUE_BALL_X = TABLE_MARGIN + 120
CUE_BALL_Y = TABLE_MARGIN + 80

# Можно также вариант: белый внизу, треугольник вверху (раскомментировать при желании)
# Но по скриншоту Poolians - биток часто вверху

FPS = 60

# Пути к звукам
SOUNDS_DIR = "sounds"
MUSIC_FILE = os.path.join(SOUNDS_DIR, "background_music.mp3")
POCKET_SOUND_FILE = os.path.join(SOUNDS_DIR, "pocket.mp3")
CUE_HIT_SOUND_FILE = os.path.join(SOUNDS_DIR, "cue_hit.mp3")
