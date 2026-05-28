#
"""
Конфигурация игры - все магические числа вынесены сюда
Принципы: DRY, отсутствие magic constants
"""

# Размеры окна
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
TABLE_MARGIN = 50

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
    'LINE': (218, 165, 32),  # Золотой
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
    'UI_BG': (0, 0, 0, 180),
    'UI_TEXT': (255, 215, 0),
}

# Физические параметры
BALL_RADIUS = 10
FRICTION = 0.985
WALL_BOUNCE_DAMP = 0.95
MAX_POWER = 22
POWER_BAR_WIDTH = 200
POWER_BAR_HEIGHT = 20

# Лузы (координаты)
POCKETS = [
    (TABLE_MARGIN, TABLE_MARGIN),  # левый верх
    (SCREEN_WIDTH - TABLE_MARGIN, TABLE_MARGIN),  # правый верх
    (TABLE_MARGIN, SCREEN_HEIGHT - TABLE_MARGIN),  # левый низ
    (SCREEN_WIDTH - TABLE_MARGIN, SCREEN_HEIGHT - TABLE_MARGIN),  # правый низ
    (SCREEN_WIDTH // 2, TABLE_MARGIN),  # центр верх
    (SCREEN_WIDTH // 2, SCREEN_HEIGHT - TABLE_MARGIN),  # центр низ
]
POCKET_RADIUS = 16

# Игровые параметры
WIN_SCORE = 7
NUM_COLOR_BALLS = 15  # 15 цветных шаров (классический пул)

# Цвета для 15 шаров (классическая нумерация)
# 1-7: сплошные, 9-15: полосатые
COLOR_BALLS = [
    COLORS['YELLOW'],   # 1
    COLORS['BLUE'],     # 2
    COLORS['RED'],      # 3
    COLORS['PURPLE'],   # 4
    COLORS['ORANGE'],   # 5
    COLORS['GREEN'],    # 6
    COLORS['MAROON'],   # 7
    COLORS['BLACK'],    # 8 (черный)
    (255, 180, 180),    # 9
    (180, 180, 255),    # 10
    (180, 255, 180),    # 11
    (255, 180, 255),    # 12
    (180, 255, 255),    # 13
    (255, 255, 180),    # 14
    (200, 150, 255),    # 15
]

# Координаты для треугольной расстановки
# Центр треугольника (где стоит первый шар)
TRIANGLE_CENTER_X = SCREEN_WIDTH // 2 + 30
TRIANGLE_CENTER_Y = SCREEN_HEIGHT // 2

# Позиция битка (белый шар) - внизу
CUE_BALL_X = SCREEN_WIDTH // 2
CUE_BALL_Y = SCREEN_HEIGHT - TABLE_MARGIN - 60

FPS = 60
