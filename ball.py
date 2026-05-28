import math
import pygame
from config import BALL_RADIUS, COLORS

class Ball:
    """Класс шара - полная инкапсуляция свойств и методов"""
    
    def __init__(self, x, y, color, number=None, ball_type=None, player=None):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.radius = BALL_RADIUS
        self.color = color
        self.number = number
        self.ball_type = ball_type
        self.player = player
        self.in_pocket = False
        self.hit_animation = 0
        self.is_cue = (ball_type == 'cue')
    
    def update(self):
        if self.in_pocket:
            return
        
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.99
        self.vy *= 0.99
        
        if abs(self.vx) < 0.3 and abs(self.vy) < 0.3:
            self.vx = 0
            self.vy = 0
        
        if self.hit_animation > 0:
            self.hit_animation -= 1
    
    def apply_force(self, fx, fy, power):
        force = min(power, 22)
        self.vx = fx * force * 1.2
        self.vy = fy * force * 1.2
        self.hit_animation = 5
    
    def draw(self, screen, shadow=True):
        if self.in_pocket:
            return
        
        if shadow:
            pygame.draw.circle(screen, (0, 0, 0, 100), 
                              (int(self.x + 3), int(self.y + 3)), self.radius)
        
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        if self.number and self.number <= 15 and self.number != 8:
            if self.ball_type == 'stripe':
                pygame.draw.rect(screen, (255, 255, 255),
                                (int(self.x - self.radius), int(self.y - 3),
                                 self.radius * 2, 6))
                pygame.draw.rect(screen, (255, 255, 255),
                                (int(self.x - 3), int(self.y - self.radius),
                                 6, self.radius * 2))
            
            try:
                font = pygame.font.Font(None, 18)
                text_color = (0, 0, 0) if self.color not in [(0,0,0), (0,0,0)] else (255, 255, 255)
                text = font.render(str(self.number), True, text_color)
                text_rect = text.get_rect(center=(int(self.x), int(self.y)))
                screen.blit(text, text_rect)
            except:
                pass
        
        highlight_x = int(self.x - self.radius * 0.3)
        highlight_y = int(self.y - self.radius * 0.3)
        pygame.draw.circle(screen, (255, 255, 255, 150), 
                          (highlight_x, highlight_y), self.radius // 3)
        
        if self.hit_animation > 0:
            alpha = 100 - self.hit_animation * 15
            s = pygame.Surface((self.radius * 4, self.radius * 4), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 255, 255, alpha), 
                              (self.radius * 2, self.radius * 2), self.radius * 1.5)
            screen.blit(s, (int(self.x - self.radius * 2), int(self.y - self.radius * 2)))
    
    def is_stopped(self):
        return abs(self.vx) < 0.3 and abs(self.vy) < 0.3 and self.hit_animation == 0
