import pygame
import math
from config import *
from ball import Ball
from physics import Physics

class BilliardGame:
    """Классический пул: один биток, треугольник цветных шаров"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎱 Классический пул для двоих")
        self.clock = pygame.time.Clock()
        
        self.balls = []
        self.scores = {1: 0, 2: 0}
        self.current_player = 1
        self.game_active = True
        self.winner = None
        self.balls_moving = False
        
        # Типы шаров, которые выбрал игрок
        self.player1_type = None  # 'solid' или 'stripe'
        self.player2_type = None
        self.black_pocketed = False
        
        # Управление ударом
        self.dragging = False
        self.drag_start = None
        self.drag_end = None
        self.power = 0
        
        self.init_game()
    
    def create_triangle_balls(self):
        """Создание треугольной расстановки шаров"""
        balls = []
        
        # Треугольная расстановка (15 шаров)
        rows = 5
        start_x = TRIANGLE_CENTER_X
        start_y = TRIANGLE_CENTER_Y - (rows - 1) * (BALL_RADIUS * 1.8) / 2
        
        ball_index = 1
        for row in range(rows):
            y = start_y + row * (BALL_RADIUS * 1.8)
            offset_x = row * (BALL_RADIUS * 1.7)
            
            for col in range(row + 1):
                x = start_x + offset_x + col * (BALL_RADIUS * 1.8)
                
                # 8-й шар (черный) в центре треугольника
                if ball_index == 8:
                    ball_type = 'black'
                    color = COLORS['BLACK']
                elif ball_index <= 7:
                    ball_type = 'solid'
                    color = COLOR_BALLS[ball_index - 1]
                else:
                    ball_type = 'stripe'
                    color = COLOR_BALLS[ball_index - 1]
                
                balls.append(Ball(x, y, color, number=ball_index, ball_type=ball_type))
                ball_index += 1
        
        return balls
    
    def init_game(self):
        """Инициализация новой игры"""
        self.balls.clear()
        self.scores = {1: 0, 2: 0}
        self.current_player = 1
        self.game_active = True
        self.winner = None
        self.balls_moving = False
        self.player1_type = None
        self.player2_type = None
        self.black_pocketed = False
        
        # БИТОК (один белый шар) - общий для обоих игроков
        cue_ball = Ball(
            CUE_BALL_X,
            CUE_BALL_Y,
            COLORS['WHITE'],
            number=None,
            ball_type='cue',
            player=None
        )
        cue_ball.is_cue = True
        self.balls.append(cue_ball)
        
        # Треугольник цветных шаров
        self.balls.extend(self.create_triangle_balls())
    
    def get_cue_ball(self):
        """Получить биток"""
        for ball in self.balls:
            if ball.is_cue and not ball.in_pocket:
                return ball
        return None
    
    def get_remaining_balls_by_type(self, ball_type):
        """Получить оставшиеся шары определённого типа"""
        return [b for b in self.balls 
                if not b.in_pocket and b.ball_type == ball_type and b.number != 8]
    
    def assign_player_types(self, pocketed_ball):
        """Назначить игрокам типы шаров после первого забитого"""
        if pocketed_ball.ball_type == 'solid':
            if self.player1_type is None:
                self.player1_type = 'solid'
                self.player2_type = 'stripe'
            elif self.player2_type is None:
                self.player2_type = 'solid'
                self.player1_type = 'stripe'
        elif pocketed_ball.ball_type == 'stripe':
            if self.player1_type is None:
                self.player1_type = 'stripe'
                self.player2_type = 'solid'
            elif self.player2_type is None:
                self.player2_type = 'stripe'
                self.player1_type = 'solid'
    
    def handle_pocket(self, ball):
        """Обработка попадания шара в лузу"""
        if ball.ball_type == 'cue':
            # Биток забит - штраф, ход переходит
            # Переставляем биток в начальную позицию
            ball.x = CUE_BALL_X
            ball.y = CUE_BALL_Y
            ball.vx = 0
            ball.vy = 0
            ball.in_pocket = False
            return 'foul'
        
        elif ball.ball_type == 'black':
            # Чёрный шар
            self.black_pocketed = True
            # Проверка, может ли игрок забивать чёрный
            my_type = self.player1_type if self.current_player == 1 else self.player2_type
            my_balls_left = len(self.get_remaining_balls_by_type(my_type))
            
            if my_balls_left == 0:
                # Победа
                self.winner = self.current_player
                self.game_active = False
                return 'win'
            else:
                # Забил чёрный раньше времени - поражение
                self.winner = 3 - self.current_player
                self.game_active = False
                return 'loss'
        
        elif ball.ball_type in ['solid', 'stripe']:
            # Назначение типов при первом забитом шаре
            if self.player1_type is None and self.player2_type is None:
                self.assign_player_types(ball)
            
            # Проверка, свой ли это шар
            my_type = self.player1_type if self.current_player == 1 else self.player2_type
            
            if ball.ball_type == my_type:
                self.scores[self.current_player] += 1
                return 'good'
            else:
                return 'foul'
        
        return 'good'
    
    def update_physics(self):
        """Обновление физики и обработка забитых шаров"""
        any_moving = False
        
        # Обновляем позиции шаров
        for ball in self.balls:
            if not ball.in_pocket:
                ball.update()
                Physics.check_wall_collision(ball, TABLE_MARGIN)
                
                # Проверка луз
                if Physics.check_pocket_collision(ball, POCKETS, POCKET_RADIUS):
                    result = self.handle_pocket(ball)
                    
                    # Если чёрный забит неправильно или фол, игра может закончиться
                    if result == 'win' or result == 'loss':
                        self.game_active = False
                
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
        
        # Смена игрока когда всё остановилось (если не было продолжения хода)
        if not any_moving and self.game_active and not self.winner:
            self.switch_player()
    
    def switch_player(self):
        """Смена игрока"""
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1
    
    def shoot(self, start_pos, end_pos):
        """Выполнить удар по битку"""
        if self.balls_moving or not self.game_active or self.winner:
            return False
        
        cue_ball = self.get_cue_ball()
        if not cue_ball:
            return False
        
        fx, fy, power = Physics.calculate_shoot_direction(start_pos, end_pos)
        if power > 0:
            cue_ball.apply_force(fx, fy, power)
            self.balls_moving = True
            return True
        return False
    
    def reset_cue_ball(self):
        """Сбросить биток в начальную позицию (после фола)"""
        cue_ball = self.get_cue_ball()
        if cue_ball:
            cue_ball.x = CUE_BALL_X
            cue_ball.y = CUE_BALL_Y
            cue_ball.vx = 0
            cue_ball.vy = 0
            cue_ball.in_pocket = False
    
    def new_game(self):
        """Полностью новая игра"""
        self.init_game()
