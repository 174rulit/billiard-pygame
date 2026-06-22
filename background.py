import pygame
import random
import math
from config import *

class AnimatedBackground:
    """Анимированный фон с летающими бильярдными шарами"""
    
    def __init__(self):
        self.particles = []
        self.balls = []
        self.time = 0
        
        # Создаём частицы (звёздочки/искры)
        for _ in range(100):
            self.particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.randint(1, 3),
                'speed_x': random.uniform(-0.3, 0.3),
                'speed_y': random.uniform(-0.3, 0.3),
                'alpha': random.randint(50, 200)
            })
        
        # Создаём летающие шары (уменьшенные копии)
        colors = [
            (255, 215, 0),   # жёлтый
            (0, 0, 200),     # синий
            (200, 0, 0),     # красный
            (120, 0, 120),   # фиолетовый
            (255, 140, 0),   # оранжевый
            (0, 150, 0),     # зелёный
            (255, 255, 255), # белый
            (255, 215, 0),   # жёлтый полосатый
            (0, 0, 200),     # синий полосатый
            (200, 0, 0),     # красный полосатый
        ]
        
        for i in range(15):
            self.balls.append({
                'x': random.randint(50, SCREEN_WIDTH - 50),
                'y': random.randint(50, SCREEN_HEIGHT - 50),
                'radius': random.randint(10, 25),
                'color': random.choice(colors),
                'speed_x': random.uniform(-1.5, 1.5),
                'speed_y': random.uniform(-1.5, 1.5),
                'rotation': random.uniform(0, math.pi * 2),
                'rotation_speed': random.uniform(-0.02, 0.02),
                'number': random.randint(1, 15),
                'is_stripe': random.choice([True, False]),
                'alpha': random.randint(150, 255)
            })
    
    def update(self):
        self.time += 0.01
        
        # Обновляем частицы
        for p in self.particles:
            p['x'] += p['speed_x']
            p['y'] += p['speed_y']
            p['alpha'] = 150 + 50 * math.sin(self.time + p['x'] * 0.01)
            
            # Отражение от границ
            if p['x'] < 0 or p['x'] > SCREEN_WIDTH:
                p['speed_x'] = -p['speed_x']
            if p['y'] < 0 or p['y'] > SCREEN_HEIGHT:
                p['speed_y'] = -p['speed_y']
        
        # Обновляем шары
        for ball in self.balls:
            ball['x'] += ball['speed_x']
            ball['y'] += ball['speed_y']
            ball['rotation'] += ball['rotation_speed']
            
            # Отражение от границ
            if ball['x'] < ball['radius'] or ball['x'] > SCREEN_WIDTH - ball['radius']:
                ball['speed_x'] = -ball['speed_x']
            if ball['y'] < ball['radius'] or ball['y'] > SCREEN_HEIGHT - ball['radius']:
                ball['speed_y'] = -ball['speed_y']
            
            # Медленное изменение скорости для плавности
            ball['speed_x'] += random.uniform(-0.05, 0.05)
            ball['speed_y'] += random.uniform(-0.05, 0.05)
            
            # Ограничение скорости
            max_speed = 2.5
            speed = math.sqrt(ball['speed_x']**2 + ball['speed_y']**2)
            if speed > max_speed:
                ball['speed_x'] = (ball['speed_x'] / speed) * max_speed
                ball['speed_y'] = (ball['speed_y'] / speed) * max_speed
    
    def draw(self, screen):
        # Градиентный фон
        for y in range(SCREEN_HEIGHT):
            # Плавный переход от тёмно-зелёного к тёмно-синему
            t = y / SCREEN_HEIGHT
            r = int(10 + 20 * t)
            g = int(30 + 30 * t)
            b = int(40 + 60 * t)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Рисуем частицы (звёздочки)
        for p in self.particles:
            alpha = int(p['alpha'])
            if alpha > 0:
                color = (200, 220, 255, alpha)
                # Используем surface для прозрачности
                s = pygame.Surface((p['size'] * 2, p['size'] * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (200, 220, 255, alpha), 
                                  (p['size'], p['size']), p['size'])
                screen.blit(s, (int(p['x'] - p['size']), int(p['y'] - p['size'])))
        
        # Рисуем шары
        for ball in self.balls:
            self.draw_ball(screen, ball)
    
    def draw_ball(self, screen, ball):
        """Отрисовка одного шара с тенью и номером"""
        x, y = int(ball['x']), int(ball['y'])
        r = ball['radius']
        color = ball['color']
        alpha = ball['alpha']
        
        # Тень
        shadow_alpha = 80
        s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (0, 0, 0, shadow_alpha), (r + 3, r + 3), r)
        screen.blit(s, (x - r, y - r))
        
        # Основной шар
        s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, color, (r, r), r)
        screen.blit(s, (x - r, y - r))
        
        # Полоса для полосатых шаров
        if ball['is_stripe']:
            s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.rect(s, (255, 255, 255, 150),
                            (r - r//2, r - 3, r, 6))
            pygame.draw.rect(s, (255, 255, 255, 150),
                            (r - 3, r - r//2, 6, r))
            screen.blit(s, (x - r, y - r))
        
        # Номер
        if ball['number']:
            try:
                font_size = max(12, int(r * 0.8))
                font = pygame.font.Font(None, font_size)
                text_color = (255, 255, 255) if color in [(0, 0, 200), (200, 0, 0), (0, 0, 0)] else (0, 0, 0)
                text = font.render(str(ball['number']), True, text_color)
                text_rect = text.get_rect(center=(x, y))
                screen.blit(text, text_rect)
            except:
                pass
        
        # Блик
        s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        highlight_x = r - int(r * 0.3)
        highlight_y = r - int(r * 0.3)
        highlight_r = max(2, r // 4)
        pygame.draw.circle(s, (255, 255, 255, 180), 
                          (highlight_x, highlight_y), highlight_r)
        screen.blit(s, (x - r, y - r))
        
        # Тонкая обводка
        s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (255, 255, 255, 30), (r, r), r, 1)
        screen.blit(s, (x - r, y - r))

    def draw_overlay(self, screen, alpha=180):
        """Затемнение для наложения меню"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(alpha)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
