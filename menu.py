import pygame
import sys
from config import *

class Menu:
    def __init__(self):
        self.player1_name = ""
        self.player2_name = ""
        self.active_input = 1  # 1 - первый игрок, 2 - второй игрок
        self.game_started = False
        self.error_message = ""
        self.error_timer = 0
        
        # Шрифты
        self.font_title = pygame.font.Font(None, 72)
        self.font_subtitle = pygame.font.Font(None, 48)
        self.font_normal = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Кнопка
        self.button_rect = None
        self.button_hover = False
    
    def handle_event(self, event):
        if self.game_started:
            return True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                # Переключение между полями
                if self.active_input == 1:
                    self.active_input = 2
                else:
                    self.active_input = 1
                return True
            
            elif event.key == pygame.K_RETURN:
                # Попытка начать игру
                if len(self.player1_name) >= 1 and len(self.player2_name) >= 1:
                    self.game_started = True
                    return True
                else:
                    self.error_message = "Введите имена обоих игроков!"
                    self.error_timer = 120  # 2 секунды
                return True
            
            elif event.key == pygame.K_BACKSPACE:
                if self.active_input == 1:
                    self.player1_name = self.player1_name[:-1]
                else:
                    self.player2_name = self.player2_name[:-1]
                return True
            
            else:
                # Добавляем символ (только буквы, цифры и пробел)
                char = event.unicode
                if char.isprintable() and len(char) == 1 and char != '\r' and char != '\n':
                    if self.active_input == 1 and len(self.player1_name) < 20:
                        self.player1_name += char
                    elif self.active_input == 2 and len(self.player2_name) < 20:
                        self.player2_name += char
                return True
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверка клика по кнопке
            if self.button_rect and self.button_rect.collidepoint(event.pos):
                if len(self.player1_name) >= 1 and len(self.player2_name) >= 1:
                    self.game_started = True
                    return True
                else:
                    self.error_message = "Введите имена обоих игроков!"
                    self.error_timer = 120
            
            # Проверка клика по полям ввода
            pos = event.pos
            # Поле игрока 1
            input1_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 320, 400, 50)
            if input1_rect.collidepoint(pos):
                self.active_input = 1
                return True
            
            # Поле игрока 2
            input2_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 400, 400, 50)
            if input2_rect.collidepoint(pos):
                self.active_input = 2
                return True
        
        return True
    
    def update(self):
        if self.error_timer > 0:
            self.error_timer -= 1
            if self.error_timer == 0:
                self.error_message = ""
    
    def draw(self, screen):
        # Затемнение фона
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Фоновый прямоугольник меню
        menu_rect = pygame.Rect(SCREEN_WIDTH // 2 - 300, 100, 600, 550)
        pygame.draw.rect(screen, (30, 30, 50, 240), menu_rect, 0, 20)
        pygame.draw.rect(screen, COLORS['GOLD'], menu_rect, 3, 20)
        
        # Заголовок
        title = self.font_title.render("🎱 БИЛЬЯРД", True, COLORS['GOLD'])
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 170))
        screen.blit(title, title_rect)
        
        sub_title = self.font_small.render("Введите имена игроков", True, (200, 200, 200))
        sub_rect = sub_title.get_rect(center=(SCREEN_WIDTH // 2, 220))
        screen.blit(sub_title, sub_rect)
        
        # Игрок 1
        label1 = self.font_normal.render("Игрок 1", True, COLORS['WHITE'])
        screen.blit(label1, (SCREEN_WIDTH // 2 - 200, 295))
        
        input1_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 320, 400, 50)
        if self.active_input == 1:
            pygame.draw.rect(screen, (80, 80, 120, 220), input1_rect, 0, 10)
            pygame.draw.rect(screen, COLORS['GOLD'], input1_rect, 2, 10)
        else:
            pygame.draw.rect(screen, (60, 60, 80, 200), input1_rect, 0, 10)
            pygame.draw.rect(screen, (100, 100, 120), input1_rect, 2, 10)
        
        name1 = self.font_normal.render(self.player1_name + ("|" if self.active_input == 1 else ""), 
                                       True, COLORS['WHITE'])
        screen.blit(name1, (SCREEN_WIDTH // 2 - 190, 330))
        
        # Игрок 2
        label2 = self.font_normal.render("Игрок 2", True, COLORS['WHITE'])
        screen.blit(label2, (SCREEN_WIDTH // 2 - 200, 395))
        
        input2_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 420, 400, 50)
        if self.active_input == 2:
            pygame.draw.rect(screen, (80, 80, 120, 220), input2_rect, 0, 10)
            pygame.draw.rect(screen, COLORS['GOLD'], input2_rect, 2, 10)
        else:
            pygame.draw.rect(screen, (60, 60, 80, 200), input2_rect, 0, 10)
            pygame.draw.rect(screen, (100, 100, 120), input2_rect, 2, 10)
        
        name2 = self.font_normal.render(self.player2_name + ("|" if self.active_input == 2 else ""), 
                                       True, COLORS['YELLOW'])
        screen.blit(name2, (SCREEN_WIDTH // 2 - 190, 430))
        
        # Кнопка "Начать игру"
        button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, 510, 240, 60)
        self.button_rect = button_rect
        
        # Проверка наведения
        mouse_pos = pygame.mouse.get_pos()
        self.button_hover = button_rect.collidepoint(mouse_pos)
        
        if self.button_hover:
            pygame.draw.rect(screen, COLORS['BUTTON_HOVER'], button_rect, 0, 15)
        else:
            pygame.draw.rect(screen, COLORS['BUTTON'], button_rect, 0, 15)
        pygame.draw.rect(screen, COLORS['GOLD'], button_rect, 2, 15)
        
        btn_text = self.font_normal.render("НАЧАТЬ ИГРУ", True, COLORS['WHITE'])
        btn_rect = btn_text.get_rect(center=(SCREEN_WIDTH // 2, 540))
        screen.blit(btn_text, btn_rect)
        
        # Ошибка
        if self.error_message:
            error_text = self.font_small.render(self.error_message, True, (255, 100, 100))
            error_rect = error_text.get_rect(center=(SCREEN_WIDTH // 2, 490))
            screen.blit(error_text, error_rect)
        
        # Подсказка
        hint = self.font_small.render("TAB - переключить поле | ENTER - начать игру", True, (150, 150, 150))
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, 600))
        screen.blit(hint, hint_rect)
    
    def is_ready(self):
        return self.game_started
    
    def get_names(self):
        return self.player1_name, self.player2_name
