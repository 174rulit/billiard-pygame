import pygame
import math
from config import *

class UI:
    def __init__(self):
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.font_tiny = pygame.font.Font(None, 24)
        
        self.last_player = -1
        self.cached_turn_surface = None
    
    def draw_player_panels(self, screen, game):
        """Таблички игроков с никами"""
        
        # ЛЕВАЯ ПАНЕЛЬ - Игрок 1
        panel_width = 280
        panel_height = 75
        panel_x = TABLE_MARGIN + 20
        panel_y = 5
        
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(screen, (40, 40, 80, 240), panel_rect, 0, 8)
        if game.current_player == 1:
            pygame.draw.rect(screen, COLORS['GOLD'], panel_rect, 2, 8)
        
        # Имя игрока
        name = self.font_tiny.render(game.player1_name, True, COLORS['UI_TEXT'])
        screen.blit(name, (panel_x + 8, panel_y + 4))
        
        # Счёт
        score = self.font_medium.render(str(game.scores[1]), True, (255, 255, 255))
        screen.blit(score, (panel_x + 8, panel_y + 30))
        
        # Тип шаров
        if game.player1_type == 'solid':
            type_text = self.font_tiny.render("● СПЛОШНЫЕ", True, (255, 255, 100))
        elif game.player1_type == 'stripe':
            type_text = self.font_tiny.render("▬ ПОЛОСАТЫЕ", True, (255, 255, 100))
        else:
            type_text = self.font_tiny.render("ЖДЁТ...", True, (180, 180, 180))
        screen.blit(type_text, (panel_x + 100, panel_y + 35))
        
        # ПРАВАЯ ПАНЕЛЬ - Игрок 2
        panel2_x = SCREEN_WIDTH - TABLE_MARGIN - panel_width - 20
        
        panel2_rect = pygame.Rect(panel2_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(screen, (80, 40, 40, 240), panel2_rect, 0, 8)
        if game.current_player == 2:
            pygame.draw.rect(screen, COLORS['GOLD'], panel2_rect, 2, 8)
        
        name2 = self.font_tiny.render(game.player2_name, True, COLORS['UI_TEXT'])
        screen.blit(name2, (panel2_x + 8, panel_y + 4))
        
        score2 = self.font_medium.render(str(game.scores[2]), True, (255, 215, 0))
        screen.blit(score2, (panel2_x + 8, panel_y + 30))
        
        if game.player2_type == 'solid':
            type_text2 = self.font_tiny.render("● СПЛОШНЫЕ", True, (255, 255, 100))
        elif game.player2_type == 'stripe':
            type_text2 = self.font_tiny.render("▬ ПОЛОСАТЫЕ", True, (255, 255, 100))
        else:
            type_text2 = self.font_tiny.render("ЖДЁТ...", True, (180, 180, 180))
        screen.blit(type_text2, (panel2_x + 100, panel_y + 35))
        
        # === ИНДИКАТОР ХОДА С НИКОМ ===
        current_name = game.get_current_player_name()
        turn_text = f"🎯 ХОДИТ: {current_name}"
        turn_x = SCREEN_WIDTH // 2 - 130
        turn_y = 8
        
        # Кешируем только при смене игрока
        if game.current_player != self.last_player:
            self.last_player = game.current_player
            self.cached_turn_surface = self.font_small.render(turn_text, True, COLORS['GOLD'])
        
        bg_rect = pygame.Rect(turn_x - 10, turn_y - 2, 260, 32)
        pygame.draw.rect(screen, (0, 0, 0, 220), bg_rect, 0, 8)
        
        if self.cached_turn_surface:
            screen.blit(self.cached_turn_surface, (turn_x, turn_y))
        
        # === ТАЙМЕР ===
        timer_text = f"⏱ {game.format_time()}"
        timer_x = SCREEN_WIDTH - 150
        timer_y = 10
        
        timer_bg = pygame.Rect(timer_x - 10, timer_y - 2, 130, 32)
        pygame.draw.rect(screen, (0, 0, 0, 200), timer_bg, 0, 8)
        pygame.draw.rect(screen, COLORS['GOLD'], timer_bg, 1, 8)
        
        timer_surface = self.font_small.render(timer_text, True, COLORS['WHITE'])
        screen.blit(timer_surface, (timer_x, timer_y))
    
    def draw_table(self, screen):
        """Отрисовка стола"""
        pygame.draw.rect(screen, COLORS['TABLE'], (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Борта
        pygame.draw.rect(screen, COLORS['WOOD'],
                        (0, 0, SCREEN_WIDTH, TABLE_MARGIN))
        pygame.draw.rect(screen, COLORS['WOOD'],
                        (0, SCREEN_HEIGHT - TABLE_MARGIN, SCREEN_WIDTH, TABLE_MARGIN))
        pygame.draw.rect(screen, COLORS['WOOD'],
                        (0, 0, TABLE_MARGIN, SCREEN_HEIGHT))
        pygame.draw.rect(screen, COLORS['WOOD'],
                        (SCREEN_WIDTH - TABLE_MARGIN, 0, TABLE_MARGIN, SCREEN_HEIGHT))
        
        # Сукно
        pygame.draw.rect(screen, COLORS['CLOTH'],
                        (TABLE_MARGIN, TABLE_MARGIN, TABLE_WIDTH, TABLE_HEIGHT))
        
        # Разметка
        pygame.draw.rect(screen, COLORS['LINE'],
                        (TABLE_MARGIN, TABLE_MARGIN, TABLE_WIDTH, TABLE_HEIGHT), 3)
        pygame.draw.line(screen, COLORS['LINE'],
                        (HALF_LINE, TABLE_MARGIN),
                        (HALF_LINE, SCREEN_HEIGHT - TABLE_MARGIN), 2)
        
        # Лузы
        for px, py in POCKETS:
            pygame.draw.circle(screen, COLORS['POCKET'], (px, py), POCKET_RADIUS)
            pygame.draw.circle(screen, COLORS['POCKET_INNER'], (px, py), POCKET_RADIUS - 12)
            pygame.draw.circle(screen, (100, 100, 100), (px - 8, py - 8), 8)
    
    def draw_power_bar(self, screen, power):
        bar_x = SCREEN_WIDTH // 2 - POWER_BAR_WIDTH // 2
        bar_y = SCREEN_HEIGHT - 55
        
        pygame.draw.rect(screen, (50, 50, 50),
                        (bar_x, bar_y, POWER_BAR_WIDTH, POWER_BAR_HEIGHT))
        
        fill_width = int((power / 25) * POWER_BAR_WIDTH)
        if power < 12:
            color = (100, 255, 100)
        elif power < 20:
            color = (255, 150, 100)
        else:
            color = (255, 80, 80)
        pygame.draw.rect(screen, color,
                        (bar_x, bar_y, fill_width, POWER_BAR_HEIGHT))
        
        pygame.draw.rect(screen, COLORS['UI_TEXT'],
                        (bar_x, bar_y, POWER_BAR_WIDTH, POWER_BAR_HEIGHT), 2)
        
        power_text = self.font_tiny.render(f"⚡ СИЛА: {int(power)}", True, COLORS['UI_TEXT'])
        screen.blit(power_text, (bar_x + POWER_BAR_WIDTH // 2 - 50, bar_y - 28))
    
    def draw_cue_and_trajectory(self, screen, start, end, cue_ball):
        if not start or not end or not cue_ball or cue_ball.in_pocket:
            return
        
        dx = start[0] - end[0]
        dy = start[1] - end[1]
        length = math.sqrt(dx * dx + dy * dy)
        
        if length < 5:
            return
        
        dir_x = dx / length
        dir_y = dy / length
        
        # Кий
        cue_length = 120
        cue_x = start[0] + dir_x * cue_length
        cue_y = start[1] + dir_y * cue_length
        
        pygame.draw.line(screen, (180, 120, 60), start, (cue_x, cue_y), 6)
        pygame.draw.line(screen, (220, 160, 80), start, (cue_x, cue_y), 3)
        
        tip_x = start[0] + dir_x * 20
        tip_y = start[1] + dir_y * 20
        pygame.draw.circle(screen, (255, 255, 255), (int(tip_x), int(tip_y)), 4)
        
        # Траектория
        step = 20
        for i in range(1, 35):
            t = i * step
            x = start[0] + dir_x * (cue_length + t)
            y = start[1] + dir_y * (cue_length + t)
            
            if (x < TABLE_MARGIN + BALL_RADIUS or 
                x > SCREEN_WIDTH - TABLE_MARGIN - BALL_RADIUS or
                y < TABLE_MARGIN + BALL_RADIUS or 
                y > SCREEN_HEIGHT - TABLE_MARGIN - BALL_RADIUS):
                break
            
            if i % 2 == 0:
                pygame.draw.circle(screen, (255, 255, 100), (int(x), int(y)), 3)
            else:
                pygame.draw.circle(screen, (200, 200, 150), (int(x), int(y)), 2)
        
        # Точка прицела
        aim_x = max(TABLE_MARGIN + BALL_RADIUS, 
                   min(SCREEN_WIDTH - TABLE_MARGIN - BALL_RADIUS, end[0]))
        aim_y = max(TABLE_MARGIN + BALL_RADIUS, 
                   min(SCREEN_HEIGHT - TABLE_MARGIN - BALL_RADIUS, end[1]))
        
        pygame.draw.circle(screen, (255, 80, 80), (int(aim_x), int(aim_y)), 8, 2)
        pygame.draw.circle(screen, (255, 255, 255), (int(aim_x), int(aim_y)), 3)
    
    def draw_game_over(self, screen, winner, player1_name, player2_name):
        if winner:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            
            winner_name = player1_name if winner == 1 else player2_name
            text = self.font_large.render(f"🏆 {winner_name} ПОБЕДИЛ! 🏆", True, COLORS['UI_TEXT'])
            x = SCREEN_WIDTH // 2 - text.get_width() // 2
            y = SCREEN_HEIGHT // 2 - 60
            screen.blit(text, (x, y))
            
            sub_text = self.font_small.render("Нажмите ПРОБЕЛ для новой игры", True, (255, 255, 255))
            sub_x = SCREEN_WIDTH // 2 - sub_text.get_width() // 2
            screen.blit(sub_text, (sub_x, y + 80))
    
    def draw_instructions(self, screen):
        instr = [
            "🎯 Удар: Зажмите ЛКМ на белом шаре → ТЯНИТЕ НАЗАД → ОТПУСТИТЕ",
            "⌨ ПРОБЕЛ - новая игра | R - сброс битка | M - музыка | ESC - выход"
        ]
        
        y = SCREEN_HEIGHT - 80
        for i, line in enumerate(instr):
            text = self.font_tiny.render(line, True, (200, 200, 200))
            x = SCREEN_WIDTH // 2 - text.get_width() // 2
            screen.blit(text, (x, y + i * 22))
