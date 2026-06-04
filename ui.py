
import pygame
import math
from config import *

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.font_tiny = pygame.font.Font(None, 24)
    
    def draw_player_panels(self, scores, current_player, player1_type, player2_type):
        """Панели игроков (слева и справа ВНЕ стола)"""
        
        # ЛЕВАЯ ПАНЕЛЬ - Игрок 1 (сверху слева)
        panel_width = 220
        panel_x = 15
        panel_y = 20
        
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, 140)
        pygame.draw.rect(self.screen, (40, 40, 70, 220), panel_rect, 0, 15)
        
        if current_player == 1:
            pygame.draw.rect(self.screen, COLORS['GOLD'], panel_rect, 4, 15)
        
        # Аватар
        pygame.draw.circle(self.screen, COLORS['WHITE'], (panel_x + 40, panel_y + 45), 25)
        text_1 = self.font_medium.render("1", True, (0, 0, 0))
        text_rect_1 = text_1.get_rect(center=(panel_x + 40, panel_y + 45))
        self.screen.blit(text_1, text_rect_1)
        
        name_text = self.font_small.render("ИГРОК 1", True, COLORS['UI_TEXT'])
        self.screen.blit(name_text, (panel_x + 75, panel_y + 25))
        
        score_text = self.font_large.render(str(scores[1]), True, COLORS['WHITE'])
        self.screen.blit(score_text, (panel_x + 75, panel_y + 60))
        
        if player1_type == 'solid':
            type_text = self.font_tiny.render("СПЛОШНЫЕ ●", True, (255, 255, 100))
        elif player1_type == 'stripe':
            type_text = self.font_tiny.render("ПОЛОСАТЫЕ ▬", True, (255, 255, 100))
        else:
            type_text = self.font_tiny.render("ЖДЁТ ЗАБИВАНИЯ", True, (180, 180, 180))
        self.screen.blit(type_text, (panel_x + 10, panel_y + 105))
        
        # ПРАВАЯ ПАНЕЛЬ - Игрок 2 (сверху справа)
        panel2_x = SCREEN_WIDTH - panel_width - 15
        
        panel2_rect = pygame.Rect(panel2_x, panel_y, panel_width, 140)
        pygame.draw.rect(self.screen, (70, 40, 40, 220), panel2_rect, 0, 15)
        
        if current_player == 2:
            pygame.draw.rect(self.screen, COLORS['GOLD'], panel2_rect, 4, 15)
        
        pygame.draw.circle(self.screen, COLORS['YELLOW'], (panel2_x + 40, panel_y + 45), 25)
        text_2 = self.font_medium.render("2", True, (0, 0, 0))
        text_rect_2 = text_2.get_rect(center=(panel2_x + 40, panel_y + 45))
        self.screen.blit(text_2, text_rect_2)
        
        name_text2 = self.font_small.render("ИГРОК 2", True, COLORS['UI_TEXT'])
        self.screen.blit(name_text2, (panel2_x + 75, panel_y + 25))
        
        score_text2 = self.font_large.render(str(scores[2]), True, COLORS['YELLOW'])
        self.screen.blit(score_text2, (panel2_x + 75, panel_y + 60))
        
        if player2_type == 'solid':
            type_text2 = self.font_tiny.render("СПЛОШНЫЕ ●", True, (255, 255, 100))
        elif player2_type == 'stripe':
            type_text2 = self.font_tiny.render("ПОЛОСАТЫЕ ▬", True, (255, 255, 100))
        else:
            type_text2 = self.font_tiny.render("ЖДЁТ ЗАБИВАНИЯ", True, (180, 180, 180))
        self.screen.blit(type_text2, (panel2_x + 10, panel_y + 105))
    
    def draw_table(self):
        """Отрисовка стола"""
        pygame.draw.rect(self.screen, COLORS['TABLE'], 
                        (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Борта
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
        
        # Центральная линия (разделение половин)
        pygame.draw.line(self.screen, COLORS['LINE'],
                        (HALF_LINE, TABLE_MARGIN),
                        (HALF_LINE, SCREEN_HEIGHT - TABLE_MARGIN), 2)
        
        # Лузы
        for px, py in POCKETS:
            pygame.draw.circle(self.screen, COLORS['POCKET'], (px, py), POCKET_RADIUS)
            pygame.draw.circle(self.screen, COLORS['POCKET_INNER'], (px, py), POCKET_RADIUS - 10)
            pygame.draw.circle(self.screen, (100, 100, 100), (px - 6, py - 6), 6)
    
    def draw_power_bar(self, power):
        bar_x = SCREEN_WIDTH // 2 - POWER_BAR_WIDTH // 2
        bar_y = SCREEN_HEIGHT - 55
        
        pygame.draw.rect(self.screen, (50, 50, 50),
                        (bar_x, bar_y, POWER_BAR_WIDTH, POWER_BAR_HEIGHT))
        
        fill_width = int((power / 25) * POWER_BAR_WIDTH)
        color = (100, 255, 100) if power < 12 else (255, 150, 100) if power < 20 else (255, 80, 80)
        pygame.draw.rect(self.screen, color,
                        (bar_x, bar_y, fill_width, POWER_BAR_HEIGHT))
        
        pygame.draw.rect(self.screen, COLORS['UI_TEXT'],
                        (bar_x, bar_y, POWER_BAR_WIDTH, POWER_BAR_HEIGHT), 2)
        
        power_text = self.font_tiny.render(f"⚡ СИЛА: {int(power)}", True, COLORS['UI_TEXT'])
        self.screen.blit(power_text, (bar_x + POWER_BAR_WIDTH // 2 - 50, bar_y - 28))
    
    def draw_trajectory(self, start, end, cue_ball):
        """Траектория полёта белого шара"""
        if not start or not end or not cue_ball or cue_ball.in_pocket:
            return
        
        # Направление удара: от мыши к шару
        dx = start[0] - end[0]
        dy = start[1] - end[1]
        length = math.sqrt(dx * dx + dy * dy)
        
        if length < 5:
            return
        
        dir_x = dx / length
        dir_y = dy / length
        
        aim_x = end[0]
        aim_y = end[1]
        
        # Основная линия от шара до точки прицела
        pygame.draw.line(self.screen, (255, 255, 100, 200), start, (aim_x, aim_y), 4)
        
        # Продолжение траектории (пунктир)
        step = 15
        for i in range(1, 40):
            t = i * step
            x = aim_x + dir_x * t
            y = aim_y + dir_y * t
            
            if (x < TABLE_MARGIN + BALL_RADIUS or 
                x > SCREEN_WIDTH - TABLE_MARGIN - BALL_RADIUS or
                y < TABLE_MARGIN + BALL_RADIUS or 
                y > SCREEN_HEIGHT - TABLE_MARGIN - BALL_RADIUS):
                break
            
            if i % 2 == 0:
                pygame.draw.circle(self.screen, (255, 255, 200), (int(x), int(y)), 3)
            else:
                pygame.draw.circle(self.screen, (200, 200, 150), (int(x), int(y)), 2)
        
        # Точка прицела
        pygame.draw.circle(self.screen, (255, 80, 80), (int(aim_x), int(aim_y)), 8, 2)
        pygame.draw.circle(self.screen, (255, 255, 255), (int(aim_x), int(aim_y)), 3)
        
        # Стрелка направления
        arrow_x = aim_x + dir_x * 25
        arrow_y = aim_y + dir_y * 25
        pygame.draw.line(self.screen, (255, 200, 100), (aim_x, aim_y), (arrow_x, arrow_y), 3)
    
    def draw_game_over(self, winner):
        if winner:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            text = self.font_large.render(f"🏆 ИГРОК {winner} ПОБЕДИЛ! 🏆", True, COLORS['UI_TEXT'])
            x = SCREEN_WIDTH // 2 - text.get_width() // 2
            y = SCREEN_HEIGHT // 2 - 60
            self.screen.blit(text, (x, y))
            
            sub_text = self.font_small.render("Нажмите ПРОБЕЛ для новой игры", True, COLORS['WHITE'])
            sub_x = SCREEN_WIDTH // 2 - sub_text.get_width() // 2
            self.screen.blit(sub_text, (sub_x, y + 80))
    
    def draw_instructions(self):
        instr = [
            "🎯 ИГРОК 1: ЛКМ на белом шаре → ТЯНИТЕ НАЗАД → ОТПУСТИТЕ",
            "🎯 ИГРОК 2: ПКМ на белом шаре → ТЯНИТЕ НАЗАД → ОТПУСТИТЕ",
            "📏 Жёлтая линия показывает траекторию полёта белого шара",
            "⌨ ПРОБЕЛ - новая игра | R - сброс битка | M - музыка | ESC - выход"
        ]
        
        y = SCREEN_HEIGHT - 110
        for i, line in enumerate(instr):
            text = self.font_tiny.render(line, True, (200, 200, 200))
            x = SCREEN_WIDTH // 2 - text.get_width() // 2
            self.screen.blit(text, (x, y + i * 22))
