import pygame
from config import *

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.font_tiny = pygame.font.Font(None, 24)
    
    def draw_player_panels(self, scores, current_player, player1_type, player2_type):
        """Рисует панели игроков ВНЕ стола (слева и справа)"""
        
        # ЛЕВАЯ ПАНЕЛЬ - Игрок 1
        panel_width = 220
        panel_x = 15
        panel_y = TABLE_MARGIN + 50
        
        # Фон панели
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, 150)
        pygame.draw.rect(self.screen, (40, 40, 70, 220), panel_rect, 0, 15)
        
        # Рамка активного игрока
        if current_player == 1:
            pygame.draw.rect(self.screen, COLORS['GOLD'], panel_rect, 4, 15)
        
        # Аватар/индикатор
        pygame.draw.circle(self.screen, COLORS['WHITE'], (panel_x + 40, panel_y + 50), 25)
        pygame.draw.circle(self.screen, COLORS['WHITE'], (panel_x + 40, panel_y + 50), 22)
        text_1 = self.font_medium.render("1", True, (0, 0, 0))
        text_rect_1 = text_1.get_rect(center=(panel_x + 40, panel_y + 50))
        self.screen.blit(text_1, text_rect_1)
        
        # Имя и счёт
        name_text = self.font_small.render("ИГРОК 1", True, COLORS['UI_TEXT'])
        self.screen.blit(name_text, (panel_x + 75, panel_y + 25))
        
        score_text = self.font_large.render(str(scores[1]), True, COLORS['WHITE'])
        self.screen.blit(score_text, (panel_x + 75, panel_y + 55))
        
        # Тип шаров
        if player1_type == 'solid':
            type_text = self.font_tiny.render("СПЛОШНЫЕ ●", True, (255, 255, 100))
        elif player1_type == 'stripe':
            type_text = self.font_tiny.render("ПОЛОСАТЫЕ ▬", True, (255, 255, 100))
        else:
            type_text = self.font_tiny.render("ЖДЁТ ЗАБИВАНИЯ", True, (180, 180, 180))
        self.screen.blit(type_text, (panel_x + 10, panel_y + 115))
        
        # ПРАВАЯ ПАНЕЛЬ - Игрок 2
        panel2_x = SCREEN_WIDTH - panel_width - 15
        
        panel2_rect = pygame.Rect(panel2_x, panel_y, panel_width, 150)
        pygame.draw.rect(self.screen, (70, 40, 40, 220), panel2_rect, 0, 15)
        
        if current_player == 2:
            pygame.draw.rect(self.screen, COLORS['GOLD'], panel2_rect, 4, 15)
        
        pygame.draw.circle(self.screen, COLORS['YELLOW'], (panel2_x + 40, panel_y + 50), 25)
        pygame.draw.circle(self.screen, COLORS['YELLOW'], (panel2_x + 40, panel_y + 50), 22)
        text_2 = self.font_medium.render("2", True, (0, 0, 0))
        text_rect_2 = text_2.get_rect(center=(panel2_x + 40, panel_y + 50))
        self.screen.blit(text_2, text_rect_2)
        
        name_text2 = self.font_small.render("ИГРОК 2", True, COLORS['UI_TEXT'])
        self.screen.blit(name_text2, (panel2_x + 75, panel_y + 25))
        
        score_text2 = self.font_large.render(str(scores[2]), True, COLORS['YELLOW'])
        self.screen.blit(score_text2, (panel2_x + 75, panel_y + 55))
        
        if player2_type == 'solid':
            type_text2 = self.font_tiny.render("СПЛОШНЫЕ ●", True, (255, 255, 100))
        elif player2_type == 'stripe':
            type_text2 = self.font_tiny.render("ПОЛОСАТЫЕ ▬", True, (255, 255, 100))
        else:
            type_text2 = self.font_tiny.render("ЖДЁТ ЗАБИВАНИЯ", True, (180, 180, 180))
        self.screen.blit(type_text2, (panel2_x + 10, panel_y + 115))
    
    def draw_table(self):
        """Отрисовка стола (только игровая поверхность)"""
        # Фон стола
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
        
        pygame.draw.line(self.screen, COLORS['LINE'],
                        (SCREEN_WIDTH // 2, TABLE_MARGIN),
                        (SCREEN_WIDTH // 2, SCREEN_HEIGHT - TABLE_MARGIN), 2)
        
        # Лузы (увеличенные)
        for px, py in POCKETS:
            # Внешнее кольцо
            pygame.draw.circle(self.screen, COLORS['POCKET'], (px, py), POCKET_RADIUS)
            # Внутреннее кольцо
            pygame.draw.circle(self.screen, COLORS['POCKET_INNER'], (px, py), POCKET_RADIUS - 8)
            # Блик на лузе
            pygame.draw.circle(self.screen, (100, 100, 100), (px - 4, py - 4), 5)
    
    def draw_power_bar(self, power):
        bar_x = SCREEN_WIDTH // 2 - POWER_BAR_WIDTH // 2
        bar_y = SCREEN_HEIGHT - 50
        
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
        if start and end:
            pygame.draw.line(self.screen, COLORS['GOLD'], start, end, 3)
            # Добавляем точки на линию прицела
            for i in range(0, 100, 15):
                t = i / 100
                x = start[0] + (end[0] - start[0]) * t
                y = start[1] + (end[1] - start[1]) * t
                pygame.draw.circle(self.screen, COLORS['GOLD'], (int(x), int(y)), 4)
    
    def draw_game_over(self, winner):
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
        instr = [
            "🎱 ИГРОК 1: ЛКМ на белом шаре → ТЯНИТЕ → ОТПУСТИТЕ",
            "🎱 ИГРОК 2: ПКМ на белом шаре → ТЯНИТЕ → ОТПУСТИТЕ",
            "⌨ ПРОБЕЛ - новая игра | R - сброс битка | ESC - выход"
        ]
        
        y = SCREEN_HEIGHT - 85
        for i, line in enumerate(instr):
            text = self.font_tiny.render(line, True, (200, 200, 200))
            x = SCREEN_WIDTH // 2 - text.get_width() // 2
            self.screen.blit(text, (x, y + i * 22))
