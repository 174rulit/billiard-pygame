import pygame
import math
from config import *
from ball import Ball
from physics import Physics

class BilliardGame:
    """Основной класс игры - управление состоянием, игроками, правилами"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎱 Бильярд для двоих")
        self.clock = pygame.time.Clock()
        
        self.balls = []
        self.scores = {1: 0, 2: 0}
        self.current_player = 1
        self.game_active = True
        self.winner = None
        self.balls_moving = False
        
        # Управление ударом
        self.dragging = False
        self.drag_start = None
        self.drag_end = None
        self.power = 0
        
        self.init_game()
    
    def init_game(self):
        """Инициализация новой игры"""
        self.balls.clear()
        self.scores = {1: 0, 2: 0}
        self.current_player = 1
        self.game_active = True
        self.winner = None
        self.balls_moving = False
        
        # Шар игрока 1 (белый) - слева сверху
        ball1 = Ball(
            TABLE_MARGIN + 100, 
            TABLE_MARGIN + 100,
            COLORS['WHITE'],
            player=1
        )
        self.balls.append(ball1)
        
        # Шар игрока 2 (желтый) - справа снизу
        ball2 = Ball(
            SCREEN_WIDTH - TABLE_MARGIN - 100,
            SCREEN_HEIGHT - TABLE_MARGIN - 100,
            COLORS['YELLOW'],
            player=2
        )
        self.balls.append(ball2)
        
        # Цветные шары (треугольником в центре)
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        
        for i in range(NUM_COLOR_BALLS):
            angle = (i / NUM_COLOR_BALLS) * math.pi * 2
            radius = 35 + (i // 4) * 25
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius
            color = COLOR_BALLS[i % len(COLOR_BALLS)]
            self.balls.append(Ball(x, y, color, player=None))
    
    def get_player_ball(self, player):
        """Получить шар текущего игрока"""
        for ball in self.balls:
            if ball.player == player and not ball.in_pocket:
                return ball
        return None
    
    def switch_player(self):
        """Смена игрока"""
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1
    
    def check_win(self):
        """Проверка победы"""
        if self.scores[1] >= WIN_SCORE:
            self.winner = 1
            self.game_active = False
        elif self.scores[2] >= WIN_SCORE:
            self.winner = 2
            self.game_active = False
    
    def update_physics(self):
        """Обновление физики всех шаров"""
        any_moving = False
        
        # Обновляем позиции шаров
        for ball in self.balls:
            if not ball.in_pocket:
                ball.update()
                Physics.check_wall_collision(ball, TABLE_MARGIN)
                
                # Проверка луз
                if Physics.check_pocket_collision(ball, POCKETS, POCKET_RADIUS):
                    if ball.player in [1, 2]:
                        self.scores[ball.player] += 1
                        self.check_win()
                
                if not ball.is_stopped():
                    any_moving = True
        
        # Столкновения между шарами
        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                if not self.balls[i].in_pocket and not self.balls[j].in_pocket:
                    Physics.resolve_ball_collision(self.balls[i], self.balls[j])
                    if not any_moving:
                        if not (self.balls[i].is_stopped() and self.balls[j].is_stopped()):
                            any_moving = True
        
        self.balls_moving = any_moving
        
        # Смена игрока когда всё остановилось
        if not any_moving and self.game_active and not self.winner:
            self.switch_player()
    
    def shoot(self, start_pos, end_pos):
        """Выполнить удар"""
        if self.balls_moving or not self.game_active or self.winner:
            return False
        
        ball = self.get_player_ball(self.current_player)
        if not ball:
            return False
        
        fx, fy, power = Physics.calculate_shoot_direction(start_pos, end_pos)
        if power > 0:
            ball.apply_force(fx, fy, power)
            self.balls_moving = True
            return True
        return False
    
    def reset_round(self):
        """Сброс текущего раунда (перестановка шаров)"""
        if not self.balls_moving:
            self.init_game()
    
    def get_color_balls_count(self):
        """Количество оставшихся цветных шаров"""
        return sum(1 for ball in self.balls if ball.player is None and not ball.in_pocket)
