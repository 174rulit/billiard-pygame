import pygame
import math
import random
import time
from config import *
from ball import Ball
from physics import Physics

class BilliardGame:
    def __init__(self, player1_name="Игрок 1", player2_name="Игрок 2"):
        self.player1_name = player1_name
        self.player2_name = player2_name
        
        self.balls = []
        self.scores = {1: 0, 2: 0}
        self.current_player = 1
        self.game_active = True
        self.winner = None
        self.balls_moving = False
        
        self.player1_type = None
        self.player2_type = None
        self.types_assigned = False
        
        self.dragging = False
        self.drag_start = None
        self.drag_end = None
        self.power = 0
        
        self.pocket_sound = None
        self.cue_hit_sound = None
        
        self.pending_foul = False
        self.pocketed_this_turn = False  # Был ли забит шар в этом ударе
        self.turn_processed = False      # Флаг, что смена хода уже обработана
        
        # Таймер
        self.start_time = time.time()
        self.elapsed_time = 0
        
        self.init_game()
    
    def load_sounds(self):
        try:
            self.pocket_sound = pygame.mixer.Sound(POCKET_SOUND_FILE)
            self.cue_hit_sound = pygame.mixer.Sound(CUE_HIT_SOUND_FILE)
        except:
            pass
    
    def play_pocket_sound(self):
        if self.pocket_sound:
            self.pocket_sound.play()
    
    def play_cue_hit_sound(self):
        if self.cue_hit_sound:
            self.cue_hit_sound.play()
    
    def get_current_player_name(self):
        if self.current_player == 1:
            return self.player1_name
        else:
            return self.player2_name
    
    def get_current_player_color(self):
        if self.current_player == 1:
            return (255, 255, 255)
        else:
            return (255, 215, 0)
    
    def create_triangle_balls(self):
        balls = []
        ball_index = 1
        for row in range(5):
            balls_in_row = row + 1
            offset_x = row * BALL_DISTANCE
            start_y = TRIANGLE_TIP_Y - (balls_in_row - 1) * BALL_DISTANCE / 2
            for col in range(balls_in_row):
                x = TRIANGLE_TIP_X + offset_x
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
        self.types_assigned = False
        self.pending_foul = False
        self.pocketed_this_turn = False
        self.turn_processed = False
        self.start_time = time.time()
        
        cue_ball = Ball(CUE_BALL_X, CUE_BALL_Y, (255, 255, 255), 
                       number=None, ball_type='cue')
        cue_ball.is_cue = True
        self.balls.append(cue_ball)
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
        if self.types_assigned:
            return
        if pocketed_ball.ball_type == 'solid':
            self.player1_type = 'solid'
            self.player2_type = 'stripe'
        elif pocketed_ball.ball_type == 'stripe':
            self.player1_type = 'stripe'
            self.player2_type = 'solid'
        else:
            return
        self.types_assigned = True
    
    def get_random_position(self):
        max_attempts = 100
        for _ in range(max_attempts):
            x = random.randint(TABLE_MARGIN + BALL_RADIUS * 3, 
                              SCREEN_WIDTH - TABLE_MARGIN - BALL_RADIUS * 3)
            y = random.randint(TABLE_MARGIN + BALL_RADIUS * 3, 
                              SCREEN_HEIGHT - TABLE_MARGIN - BALL_RADIUS * 3)
            
            collision = False
            for ball in self.balls:
                if ball.in_pocket:
                    continue
                dx = ball.x - x
                dy = ball.y - y
                if (dx*dx + dy*dy) ** 0.5 < BALL_RADIUS * 3:
                    collision = True
                    break
            
            if not collision:
                return x, y
        
        return CUE_BALL_X, CUE_BALL_Y
    
    def handle_pocket(self, ball):
        """Обработка попадания в лузу"""
        self.play_pocket_sound()
        
        # Биток (белый шар) - фол
        if ball.ball_type == 'cue':
            x, y = self.get_random_position()
            ball.x = x
            ball.y = y
            ball.vx = 0
            ball.vy = 0
            ball.in_pocket = False
            self.pending_foul = True
            return 'foul'
        
        # Чёрный шар
        elif ball.ball_type == 'black':
            my_type = self.player1_type if self.current_player == 1 else self.player2_type
            my_balls_left = len(self.get_remaining_balls_by_type(my_type))
            if my_balls_left == 0:
                self.winner = self.current_player
                self.game_active = False
                self.pocketed_this_turn = True
                return 'win'
            else:
                self.winner = 3 - self.current_player
                self.game_active = False
                self.pocketed_this_turn = True
                return 'loss'
        
        # Цветной шар
        elif ball.ball_type in ['solid', 'stripe']:
            if not self.types_assigned:
                self.assign_player_types(ball)
                self.scores[self.current_player] += 1
                self.pocketed_this_turn = True
                return 'good'
            
            my_type = self.player1_type if self.current_player == 1 else self.player2_type
            
            if ball.ball_type == my_type:
                self.scores[self.current_player] += 1
                self.pocketed_this_turn = True  # Шар забит!
                return 'good'
            else:
                self.pending_foul = True
                return 'foul'
        
        return 'good'
    
    def update_physics(self):
        any_moving = False
        
        # Обновляем все шары
        for ball in self.balls:
            if not ball.in_pocket:
                ball.update()
                Physics.check_wall_collision(ball, TABLE_MARGIN)
                in_pocket, _ = Physics.check_pocket_collision(ball, POCKETS, POCKET_RADIUS)
                if in_pocket:
                    self.handle_pocket(ball)
                if not ball.is_stopped():
                    any_moving = True
        
        # Столкновения шаров между собой
        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                if not self.balls[i].in_pocket and not self.balls[j].in_pocket:
                    Physics.resolve_ball_collision(self.balls[i], self.balls[j])
                    if not self.balls[i].is_stopped() or not self.balls[j].is_stopped():
                        any_moving = True
        
        self.balls_moving = any_moving
        
        # === КОГДА ШАРЫ ОСТАНОВИЛИСЬ (обрабатываем ТОЛЬКО ОДИН РАЗ) ===
        if not any_moving and self.game_active and not self.winner and not self.turn_processed:
            self.turn_processed = True  # Блокируем повторную обработку
            
            # Если был фол (забит чужой шар или биток)
            if self.pending_foul:
                cue_ball = self.get_cue_ball()
                if cue_ball:
                    x, y = self.get_random_position()
                    cue_ball.x = x
                    cue_ball.y = y
                    cue_ball.vx = 0
                    cue_ball.vy = 0
                    cue_ball.in_pocket = False
                self.pending_foul = False
                # Фол - ход переходит к сопернику
                self.switch_player()
                self.pocketed_this_turn = False
            else:
                # Если НЕ было забито ни одного шара в этом ударе
                if not self.pocketed_this_turn:
                    # Промах - ход переходит к сопернику
                    self.switch_player()
                # Если шар был забит - ход остаётся у текущего игрока (ничего не делаем)
            
            # Сбрасываем флаг для следующего удара
            self.pocketed_this_turn = False
        
        # Если шары снова начали двигаться - сбрасываем флаг обработки
        if any_moving:
            self.turn_processed = False
        
        # Обновляем таймер
        if self.game_active and not self.winner:
            self.elapsed_time = time.time() - self.start_time
    
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
        
        dx = start_pos[0] - end_pos[0]
        dy = start_pos[1] - end_pos[1]
        length = math.sqrt(dx*dx + dy*dy)
        if length < 5:
            return False
        
        fx = dx / length
        fy = dy / length
        power = min((length / 180) * 25, 25)
        
        if power > 3:
            cue_ball.apply_force(fx, fy, power)
            self.balls_moving = True
            self.pocketed_this_turn = False
            self.pending_foul = False
            self.turn_processed = False
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
    
    def format_time(self):
        minutes = int(self.elapsed_time // 60)
        seconds = int(self.elapsed_time % 60)
        return f"{minutes:02d}:{seconds:02d}"
