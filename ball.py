import math
import pygame
from config import BALL_RADIUS, COLORS

class Ball:
    """Класс шара - полная инкапсуляция свойств и методов"""
    
    def __init__(self, x, y, color, player=None):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.radius = BALL_RADIUS
        self.color = color
        self.player = player  # 1 или 2 для игроков, None для цветных
        self.in_pocket = False
        self.hit_animation = 0  # для визуального эффекта удара
    
    def update(self):
        """Обновление позиции и физики"""
        if self.in_pocket:
            return
        
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.99
        self.vy *= 0.99
        
        # Остановка при малой скорости
        if abs(self.vx) < 0.3 and abs(self.vy) < 0.3:
            self.vx = 0
            self.vy = 0
        
        # Анимация удара затухает
        if self.hit_animation > 0:
            self.hit_animation -= 1
    
    def apply_force(self, fx, fy, power):
        """Применить силу удара"""
        force = min(power, 22)
        self.vx = fx * force * 1.2
        self.vy = fy * force * 1.2
        self.hit_animation = 5
    
    def draw(self, screen, shadow=True):
        """Отрисовка шара с тенью и бликом"""
        if self.in_pocket:
            return
        
        if shadow:
            # Тень
            pygame.draw.circle(screen, (0, 0, 0, 100), 
                              (int(self.x + 3), int(self.y + 3)), self.radius)
        
        # Основной шар
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Блик (эффект объема)
        highlight_x = int(self.x - self.radius * 0.3)
        highlight_y = int(self.y - self.radius * 0.3)
        pygame.draw.circle(screen, (255, 255, 255, 150), 
                          (highlight_x, highlight_y), self.radius // 3)
        
        # Эффект удара (белое свечение)
        if self.hit_animation > 0:
            alpha = 100 - self.hit_animation * 15
            s = pygame.Surface((self.radius * 4, self.radius * 4), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 255, 255, alpha), 
                              (self.radius * 2, self.radius * 2), self.radius * 1.5)
            screen.blit(s, (int(self.x - self.radius * 2), int(self.y - self.radius * 2)))
    
    def is_stopped(self):
        """Проверка, остановился ли шар"""
        return abs(self.vx) < 0.3 and abs(self.vy) < 0.3 and self.hit_animation == 0
    
    def get_rect(self):
        """Получить прямоугольник для коллизий"""
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                          self.radius * 2, self.radius * 2)
