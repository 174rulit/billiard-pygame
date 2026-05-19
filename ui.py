import pygame
from config import *

class UI:
    """Класс для отрисовки интерфейса"""
    
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.font_tiny = pygame.font.Font(None, 24)
    
    def draw_table(self):
        """Отрисовка бильярдного стола"""
        pygame.draw.rect(self.screen, COLORS['TABLE'], 
                        (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Деревянные борта
        pygame.draw.rect(self.screen, COLORS['WOOD'],
                        (0, 0, SCREEN_WIDTH, TABLE_MARGIN))
        pygame.draw.rect(self.screen, COLORS['WOOD'],
                        (0, SCREEN_HEIGHT - TABLE_MARGIN, SCREEN_WIDTH, TABLE_MARGIN))
        pygame.draw.rect(self.screen, COLORS['WOOD'],
                        (0, 0, TABLE_MARGIN, SCREEN_HEIGHT))
        pygame.draw.rect(self.screen, COLORS['WOOD'],
                        (SCREEN_WIDTH - TABLE_MARGIN, 0, TABLE_MARGIN, SCREEN_HEIGHT))
        
        # Сукно
        pygame.draw.rect(self.screen, COLORS['CLOTH'],
                        (TABLE_MARGIN, TABLE_MARGIN, TABLE_WIDTH, TABLE_HEIGHT))
        
        # Разметка
        pygame.draw.rect(self.screen, COLORS['LINE'],
                        (TABLE_MARGIN, TABLE_MARGIN, TABLE_WIDTH, TABLE_HEIGHT), 3)
        
        # Линия раздела (центр)
        pygame.draw.line(self.screen, COLORS['LINE'],
                        (SCREEN_WIDTH // 2, TABLE_MARGIN),
                        (SCREEN_WIDTH // 2, SCREEN_HEIGHT - TABLE_MARGIN), 2)
        
        # Лузы
        for px, py in POCKETS:
            pygame.draw.circle(self.screen, COLORS['POCKET'], (px, py), POCKET_RADIUS)
            pygame.draw.circle(self.screen, COLORS['POCKET_INNER'], (px, py), POCKET_RADIUS - 5)
    
    def draw_scores(self, scores, current_player, player1_type, player2_type):
        """Отрисовка счета и типов шаров игроков"""
        # Игрок 1
        p1_rect = pygame.Rect(20, 20, 220, 100)
        if current_player == 1:
            pygame.draw.rect(self.screen, (218, 165, 32, 100), p1_rect, 3, 10)
        pygame.draw.rect(self.screen, (0, 0, 0, 150), p1_rect, 0, 10)
        
        p1_text = self.font_small.render("ИГРОК 1", True, COLORS['UI_TEXT'])
        p1_score = self.font_medium.render(str(scores[1]), True, COLORS['WHITE'])
        self.screen.blit(p1_text, (35, 30))
        self.screen.blit(p1_score, (35, 65))
        
        # Тип шаров игрока 1
        if player1_type == 'solid':
            type_text = self.font_tiny.render("СПЛОШНЫЕ", True, (255, 255, 100))
        elif player1_type == 'stripe':
            type_text = self.font_tiny.render("ПОЛОСАТЫЕ", True, (255, 255, 100))
        else:
            type_text = self.font_tiny.render("—", True, (150, 150, 150))
        self.screen.blit(type_text, (35, 95))
        
        # Игрок 2
        p2_rect = pygame.Rect(SCREEN_WIDTH - 240, 20, 220, 100)
        if current_player == 2:
            pygame.draw.rect(self.screen, (218, 165, 32, 100), p2_rect, 3, 10)
        pygame.draw.rect(self.screen, (0, 0, 0, 150), p2_rect, 0, 10)
        
        p2_text = self.font_small.render("ИГРОК 2", True, COLORS['UI_TEXT'])
        p2_score = self.font_medium.render(str(scores[2]), True, COLORS['YELLOW'])
        self.screen.blit(p2_text, (SCREEN_WIDTH - 225, 30))
        self.screen.blit(p2_score, (SCREEN_WIDTH - 225, 65))
        
        # Тип шаров игрока 2
        if player2_type == 'solid':
            type_text = self.font_tiny.render("СПЛОШНЫЕ", True, (255, 255, 100))
        elif player2_type == 'stripe':
            type_text = self.font_tiny.render("ПОЛОСАТЫЕ", True, (255, 255, 100))
        else:
            type_text = self.font_tiny.render("—", True, (150, 150, 150))
        self.screen.blit(type_text, (SCREEN_WIDTH - 225, 95))
    
    def draw_power_bar(self, power):
        """Отрисовка шкалы силы"""
        bar_x = SCREEN_WIDTH // 2 - POWER_BAR_WIDTH // 2
        bar_y = SCREEN_HEIGHT - 60
        
        pygame.draw.rect(self.screen, (50, 50, 50),
                        (bar_x, bar_y, POWER_BAR_WIDTH, POWER_BAR_HEIGHT))
        
        fill_width = int((power / 22) * POWER_BAR_WIDTH)
        color = (100, 255, 100) if power < 11 else (255, 100, 100)
        pygame.draw.rect(self.screen, color,
                        (bar_x, bar_y, fill_width, POWER_BAR_HEIGHT))
        
        pygame.draw.rect(self.screen, COLORS['UI_TEXT'],
                        (bar_x, bar_y, POWER_BAR_WIDTH, POWER_BAR_HEIGHT), 2)
        
        power_text = self.font_tiny.render(f"СИЛА: {int(power)}", True, COLORS['UI_TEXT'])
        self.screen.blit(power_text, (bar_x + POWER_BAR_WIDTH // 2 - 40, bar_y - 25))
    
    def draw_aim_line(self, start, end):
        """Линия прицела"""
        if start and end:
            pygame.draw.line(self.screen, COLORS['GOLD'], start, end, 3)
    
    def draw_turn_indicator(self, current_player):
        """Индикатор хода"""
        text = self.font_medium.render(f"ХОД: ИГРОК {current_player}", True, COLORS['UI_TEXT'])
        x = SCREEN_WIDTH // 2 - text.get_width() // 2
        y = 15
        bg_rect = pygame.Rect(x - 10, y - 5, text.get_width() + 20, text.get_height() + 10)
        pygame.draw.rect(self.screen, (0, 0, 0, 200), bg_rect, 0, 10)
        self.screen.blit(text, (x, y))
    
    def draw_game_over(self, winner):
        """Экран победы"""
        if winner:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            text = self.font_large.render(f"ИГРОК {winner} ПОБЕДИЛ!", True, COLORS['UI_TEXT'])
            x = SCREEN_WIDTH // 2 - text.get_width() // 2
            y = SCREEN_HEIGHT // 2 - 50
            self.screen.blit(text, (x, y))
            
            sub_text = self.font_small.render("Нажмите ПРОБЕЛ для новой игры", True, COLORS['WHITE'])
            sub_x = SCREEN_WIDTH // 2 - sub_text.get_width() // 2
            self.screen.blit(sub_text, (sub_x, y + 70))
    
    def draw_instructions(self):
        """Подсказки"""
        instr = [
            "Игрок 1: ЛКМ на белом шаре → ТЯНИТЕ → ОТПУСТИТЕ",
            "Игрок 2: ПКМ на белом шаре → ТЯНИТЕ → ОТПУСТИТЕ",
            "ПРОБЕЛ - новая игра | R - сброс битка"
        ]
        
        y = SCREEN_HEIGHT - 95
        for i, line in enumerate(instr):
            text = self.font_tiny.render(line, True, (180, 180, 180))
            x = SCREEN_WIDTH // 2 - text.get_width() // 2
            self.screen.blit(text, (x, y + i * 22))
