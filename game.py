
import pygame
import math
from config import *
from ball import Ball
from physics import Physics

class BilliardGame:
    def __init__(self):
        self.screen = None
        self.balls = []
        self.scores = {1: 0, 2: 0}
        self.current_player = 1
        self.game_active = True
        self.winner = None
        self.balls_moving = False
        
        self.player1_type = None
        self.player2_type = None
        self.black_pocketed = False
        
        self.dragging = False
        self.drag_start = None
        self.drag_end = None
        self.power = 0
        
        self.pocket_sound = None
        self.cue_hit_sound = None
        
        self.init_game()
    
    def set_screen(self, screen):
        self.screen = screen
    
    def load_sounds(self):
        try:
            self.pocket_sound = pygame.mixer.Sound(POCKET_SOUND_FILE)
            self.cue_hit_sound = pygame.mixer.Sound(CUE_HIT_SOUND_FILE)
        except Exception as e:
            print(f"Не удалось загрузить звуки: {e}")
    
    def play_pocket_sound(self):
        if self.pocket_sound:
            self.pocket_sound.play()
    
    def play_cue_hit_sound(self):
        if self.cue_hit_sound:
            self.cue_hit_sound.play()
    
    def create_triangle_balls(self):
        """
        Создание треугольника из 15 шаров на ПРАВОЙ половине стола
        Вершина треугольника (шар №1) направлена ВЛЕВО (к белому шару)
        Ряды: 1, 2, 3, 4, 5 шаров
        """
        balls = []
        
        rows = 5
        # Вершина треугольника (первый шар, номер 1)
        tip_x = TRIANGLE_TIP_X
        tip_y = TRIANGLE_TIP_Y
        
        # Угол наклона для равностороннего треугольника
        # В классическом пуле треугольник расширяется вправо и вниз/вверх
        # Но вершина смотрит влево, поэтому ряды идут вправо
        
        ball_index = 1
        for row in range(rows):
            balls_in_row = row + 1
            # Ширина ряда = (balls_in_row - 1) * BALL_DISTANCE
            # Начальная X для этого ряда (сдвиг вправо от вершины)
            row_start_x = tip_x + row * (BALL_DISTANCE * 0.866)  # Угол 60 градусов
            
            # Y координата: центрируем треугольник по вертикали
            # Вершина в центре, остальные ряды выше и ниже
            row_height = (balls_in_row - 1) * BALL_DISTANCE / 2
            row_start_y = tip_y - row_height
            
            for col in range(balls_in_row):
                x = row_start_x
                y = row_start_y + col * BALL_DISTANCE
                
                # Номер шара
                if ball_index == 8:
                    ball_type = 'black'
                    color = COLOR_BALLS[8]
                elif ball_index <= 7:
                    ball_type = 'solid'
                    color = COLOR_BALLS[ball_index]
                else:
                    ball_type = 'stripe'
                    color = COLOR_BALLS[ball_index]
                
                balls.append(Ball(x, y, color, number=ball_index, ball_type=ball_type))
                ball_index += 1
        
        # Альтернативная, более правильная расстановка треугольника
        # Пересоздаём с правильной геометрией
        balls = []
        ball_index = 1
        
        # Треугольник: 5 рядов
        # Ряд 1: 1 шар (x=tip_x, y=tip_y)
        # Ряд 2: 2 шара (x=tip_x + dist, y=tip_y ± dist/2)
        # Ряд 3: 3 шара (x=tip_x + 2*dist, y=tip_y ± dist, tip_y)
        # и так далее
        
        for row in range(5):
            balls_in_row = row + 1
            offset_x = row * BALL_DISTANCE
            
            # Начальная Y для этого ряда (центрируем)
            start_y = tip_y - (balls_in_row - 1) * BALL_DISTANCE / 2
            
            for col in range(balls_in_row):
                x = tip_x + offset_x
                y = start_y + col * BALL_DISTANCE
                
                if ball_index == 8:
                    ball_type = 'black'
                    color = COLOR_BALLS[8]
                elif ball_index <= 7:
                    ball_type = 'solid'
                    color = COLOR_BALLS[ball_index]
                else:
                    ball_type = 'stripe'
                    color = COLOR_BALLS[ball_index]
                
                balls.append(Ball(x, y, color, number=ball_index, ball_type=ball_type))
                ball_index += 1
        
        return balls
    
    def init_game(self):
        self.balls.clear()
        self.scores = {1: 0, 2: 0}
        self.current_player = 1
        self.game_active = True
        self.winner = None
        self.balls_moving = False
        self.player1_type = None
        self.player2_type = None
        self.black_pocketed = False
        
        # БЕЛЫЙ ШАР - на ЛЕВОЙ половине, напротив вершины треугольника
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
        
        # ТРЕУГОЛЬНИК - на ПРАВОЙ половине
        self.balls.extend(self.create_triangle_balls())
    
    def get_cue_ball(self):
        for ball in self.balls:
            if ball.is_cue and not ball.in_pocket:
                return ball
        return None
    
    def get_remaining_balls_by_type(self, ball_type):
        return [b for b in self.balls 
                if not b.in_pocket and b.ball_type == ball_type and b.number != 8]
    
    def assign_player_types(self, pocketed_ball):
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
        self.play_pocket_sound()
        
        if ball.ball_type == 'cue':
            ball.x = CUE_BALL_X
            ball.y = CUE_BALL_Y
            ball.vx = 0
            ball.vy = 0
            ball.in_pocket = False
            return 'foul'
        
        elif ball.ball_type == 'black':
            self.black_pocketed = True
            my_type = self.player1_type if self.current_player == 1 else self.player2_type
            my_balls_left = len(self.get_remaining_balls_by_type(my_type))
            
            if my_balls_left == 0:
                self.winner = self.current_player
                self.game_active = False
                return 'win'
            else:
                self.winner = 3 - self.current_player
                self.game_active = False
                return 'loss'
        
        elif ball.ball_type in ['solid', 'stripe']:
            if self.player1_type is None and self.player2_type is None:
                self.assign_player_types(ball)
            
            my_type = self.player1_type if self.current_player == 1 else self.player2_type
            
            if ball.ball_type == my_type:
                self.scores[self.current_player] += 1
                return 'good'
            else:
                return 'foul'
        
        return 'good'
    
    def update_physics(self):
        any_moving = False
        
        for ball in self.balls:
            if not ball.in_pocket:
                ball.update()
                Physics.check_wall_collision(ball, TABLE_MARGIN)
                
                in_pocket, pocket_pos = Physics.check_pocket_collision(ball, POCKETS, POCKET_RADIUS)
                if in_pocket:
                    result = self.handle_pocket(ball)
                    if result == 'win' or result == 'loss':
                        self.game_active = False
                
                if not ball.is_stopped():
                    any_moving = True
        
        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                if not self.balls[i].in_pocket and not self.balls[j].in_pocket:
                    Physics.resolve_ball_collision(self.balls[i], self.balls[j])
                    if not any_moving:
                        if not (self.balls[i].is_stopped() and self.balls[j].is_stopped()):
                            any_moving = True
        
        self.balls_moving = any_moving
        
        if not any_moving and self.game_active and not self.winner:
            self.switch_player()
    
    def switch_player(self):
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1
    
    def shoot(self, start_pos, end_pos):
        if self.balls_moving or not self.game_active or self.winner:
            return False
        
        cue_ball = self.get_cue_ball()
        if not cue_ball:
            return False
        
        # Направление от мыши к шару (удар в сторону отведения)
        fx = start_pos[0] - end_pos[0]
        fy = start_pos[1] - end_pos[1]
        length = math.sqrt(fx*fx + fy*fy)
        if length > 0:
            fx /= length
            fy /= length
        
        power = min((length / 180) * 25, 25)
        
        if power > 3:
            cue_ball.apply_force(fx, fy, power)
            self.balls_moving = True
            self.play_cue_hit_sound()
            return True
        return False
    
    def reset_cue_ball(self):
        cue_ball = self.get_cue_ball()
        if cue_ball:
            cue_ball.x = CUE_BALL_X
            cue_ball.y = CUE_BALL_Y
            cue_ball.vx = 0
            cue_ball.vy = 0
            cue_ball.in_pocket = False
    
    def new_game(self):
        self.init_game()
