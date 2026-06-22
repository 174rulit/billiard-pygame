import pygame
import random
from config import *

class GuessGame:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_guess = ""
        self.player2_guess = ""
        self.active_input = 1  # 1 - первый, 2 - второй
        self.computer_number = None
        self.winner = None
        self.game_completed = False
        self.is_tie = False  # Флаг ничьей
        self.error_message = ""
        self.error_timer = 0
        self.tie_message = ""
        self.tie_timer = 0
        
        # Шрифты
        self.font_title = pygame.font.Font(None, 56)
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_normal = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Кнопка
        self.button_rect = None
        self.button_hover = False
    
    def handle_event(self, event):
        if self.game_completed:
            # Если игра завершена, ждём только клик по кнопке или Enter
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.reset_game()
                return True
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.button_rect and self.button_rect.collidepoint(event.pos):
                    self.reset_game()
                    return True
            
            return True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                # Переключение между полями
                if self.active_input == 1:
                    self.active_input = 2
                else:
                    self.active_input = 1
                return True
            
            elif event.key == pygame.K_BACKSPACE:
                if self.active_input == 1:
                    self.player1_guess = self.player1_guess[:-1]
                else:
                    self.player2_guess = self.player2_guess[:-1]
                return True
            
            elif event.key == pygame.K_RETURN:
                # Проверяем, что оба ввели числа
                if self.player1_guess and self.player2_guess:
                    self.calculate_winner()
                else:
                    self.error_message = "Оба игрока должны ввести числа!"
                    self.error_timer = 120
                return True
            
            else:
                # Добавляем цифру
                char = event.unicode
                if char.isdigit():
                    if self.active_input == 1 and len(self.player1_guess) < 3:
                        self.player1_guess += char
                    elif self.active_input == 2 and len(self.player2_guess) < 3:
                        self.player2_guess += char
                return True
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверка клика по полям
            pos = event.pos
            
            # Поле игрока 1
            input1_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 320, 400, 50)
            if input1_rect.collidepoint(pos):
                self.active_input = 1
                return True
            
            # Поле игрока 2
            input2_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 420, 400, 50)
            if input2_rect.collidepoint(pos):
                self.active_input = 2
                return True
        
        return True
    
    def reset_game(self):
        """Перезапуск мини-игры при ничьей"""
        self.player1_guess = ""
        self.player2_guess = ""
        self.active_input = 1
        self.computer_number = None
        self.winner = None
        self.game_completed = False
        self.is_tie = False
        self.tie_message = ""
        self.tie_timer = 0
        self.error_message = ""
        self.error_timer = 0
    
    def calculate_winner(self):
        """Расчёт победителя с проверкой на ничью"""
        try:
            guess1 = int(self.player1_guess)
            guess2 = int(self.player2_guess)
            
            # Проверка диапазона
            if guess1 < 0 or guess1 > 100 or guess2 < 0 or guess2 > 100:
                self.error_message = "Числа должны быть от 0 до 100!"
                self.error_timer = 120
                return
            
            # Генерируем число компьютера
            self.computer_number = random.randint(0, 100)
            
            # Вычисляем расстояния
            dist1 = abs(guess1 - self.computer_number)
            dist2 = abs(guess2 - self.computer_number)
            
            # Проверка на ничью
            if dist1 == dist2:
                # Ничья - показываем сообщение и перезапускаем
                self.is_tie = True
                self.tie_message = f"НИЧЬЯ! Оба игрока одинаково близки к {self.computer_number}! Играем заново..."
                self.tie_timer = 180  # 3 секунды показа
                # Запускаем перезапуск через таймер
                return
            
            if dist1 < dist2:
                self.winner = 1
            else:
                self.winner = 2
            
            self.game_completed = True
            
        except ValueError:
            self.error_message = "Введите корректные числа (0-100)!"
            self.error_timer = 120
    
    def update(self):
        # Обновление таймеров
        if self.error_timer > 0:
            self.error_timer -= 1
            if self.error_timer == 0:
                self.error_message = ""
        
        # Автоматический перезапуск при ничьей
        if self.is_tie:
            self.tie_timer -= 1
            if self.tie_timer == 0:
                # Очищаем поля и начинаем заново
                self.reset_game()
                # После перезапуска показываем сообщение на короткое время
                self.error_message = "Введите числа заново!"
                self.error_timer = 60
    
    def draw(self, screen):
        # Затемнение фона
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Основное меню
        menu_rect = pygame.Rect(SCREEN_WIDTH // 2 - 350, 80, 700, 550)
        pygame.draw.rect(screen, (30, 30, 50, 240), menu_rect, 0, 20)
        pygame.draw.rect(screen, COLORS['GOLD'], menu_rect, 3, 20)
        
        # Заголовок
        if self.is_tie:
            title = self.font_title.render("НИЧЬЯ! ПЕРЕЗАПУСК...", True, (255, 200, 50))
        else:
            title = self.font_title.render("КТО БЬЁТ ПЕРВЫМ?", True, COLORS['GOLD'])
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title, title_rect)
        
        if self.is_tie:
            # Показываем сообщение о ничьей
            tie_text = self.font_medium.render(self.tie_message, True, (255, 200, 100))
            tie_rect = tie_text.get_rect(center=(SCREEN_WIDTH // 2, 230))
            screen.blit(tie_text, tie_rect)
            
            sub_text = self.font_small.render("Игра перезапускается...", True, (200, 200, 200))
            sub_rect = sub_text.get_rect(center=(SCREEN_WIDTH // 2, 280))
            screen.blit(sub_text, sub_rect)
        
        elif self.game_completed:
            # === РЕЗУЛЬТАТ ===
            winner_name = self.player1_name if self.winner == 1 else self.player2_name
            
            # Показываем число компьютера
            comp_text = self.font_large.render(f"Число компьютера: {self.computer_number}", True, COLORS['WHITE'])
            comp_rect = comp_text.get_rect(center=(SCREEN_WIDTH // 2, 220))
            screen.blit(comp_text, comp_rect)
            
            # Показываем числа игроков
            # Игрок 1
            if self.winner == 1:
                color1 = COLORS['GOLD']
                marker1 = ""
            else:
                color1 = (200, 200, 200)
                marker1 = ""
            
            guess1_text = self.font_medium.render(f"{marker1}{self.player1_name}: {self.player1_guess}", True, color1)
            screen.blit(guess1_text, (SCREEN_WIDTH // 2 - 200, 280))
            
            # Игрок 2
            if self.winner == 2:
                color2 = COLORS['GOLD']
                marker2 = ""
            else:
                color2 = (200, 200, 200)
                marker2 = ""
            
            guess2_text = self.font_medium.render(f"{marker2}{self.player2_name}: {self.player2_guess}", True, color2)
            screen.blit(guess2_text, (SCREEN_WIDTH // 2 - 200, 330))
            
            # Победитель
            winner_text = self.font_large.render(f"ПЕРВЫЙ ХОДИТ: {winner_name}", True, COLORS['GOLD'])
            winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, 420))
            screen.blit(winner_text, winner_rect)
            
            # Кнопка "Начать игру"
            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, 490, 240, 60)
            self.button_rect = button_rect
            
            mouse_pos = pygame.mouse.get_pos()
            self.button_hover = button_rect.collidepoint(mouse_pos)
            
            if self.button_hover:
                pygame.draw.rect(screen, COLORS['BUTTON_HOVER'], button_rect, 0, 15)
            else:
                pygame.draw.rect(screen, COLORS['BUTTON'], button_rect, 0, 15)
            pygame.draw.rect(screen, COLORS['GOLD'], button_rect, 2, 15)
            
            btn_text = self.font_normal.render("НАЧАТЬ ИГРУ", True, COLORS['WHITE'])
            btn_rect = btn_text.get_rect(center=(SCREEN_WIDTH // 2, 520))
            screen.blit(btn_text, btn_rect)
            
            # Подсказка
            hint = self.font_small.render("ENTER или клик по кнопке", True, (150, 150, 150))
            hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, 575))
            screen.blit(hint, hint_rect)
            
        else:
            # === ВВОД ЧИСЕЛ ===
            # Игрок 1
            label1 = self.font_normal.render(f"{self.player1_name} (введите число 0-100):", True, COLORS['WHITE'])
            screen.blit(label1, (SCREEN_WIDTH // 2 - 200, 295))
            
            input1_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 320, 400, 50)
            if self.active_input == 1:
                pygame.draw.rect(screen, (80, 80, 120, 220), input1_rect, 0, 10)
                pygame.draw.rect(screen, COLORS['GOLD'], input1_rect, 2, 10)
            else:
                pygame.draw.rect(screen, (60, 60, 80, 200), input1_rect, 0, 10)
                pygame.draw.rect(screen, (100, 100, 120), input1_rect, 2, 10)
            
            guess1 = self.font_medium.render(self.player1_guess + ("|" if self.active_input == 1 else ""), 
                                            True, COLORS['WHITE'])
            screen.blit(guess1, (SCREEN_WIDTH // 2 - 190, 330))
            
            # Игрок 2
            label2 = self.font_normal.render(f"{self.player2_name} (введите число 0-100):", True, COLORS['WHITE'])
            screen.blit(label2, (SCREEN_WIDTH // 2 - 200, 395))
            
            input2_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 420, 400, 50)
            if self.active_input == 2:
                pygame.draw.rect(screen, (80, 80, 120, 220), input2_rect, 0, 10)
                pygame.draw.rect(screen, COLORS['GOLD'], input2_rect, 2, 10)
            else:
                pygame.draw.rect(screen, (60, 60, 80, 200), input2_rect, 0, 10)
                pygame.draw.rect(screen, (100, 100, 120), input2_rect, 2, 10)
            
            guess2 = self.font_medium.render(self.player2_guess + ("|" if self.active_input == 2 else ""), 
                                            True, COLORS['YELLOW'])
            screen.blit(guess2, (SCREEN_WIDTH // 2 - 190, 430))
            
            # Ошибка
            if self.error_message:
                error_text = self.font_small.render(self.error_message, True, (255, 100, 100))
                error_rect = error_text.get_rect(center=(SCREEN_WIDTH // 2, 500))
                screen.blit(error_text, error_rect)
            
            # Подсказка
            hint = self.font_small.render("TAB - переключить поле | ENTER - определить первого", True, (150, 150, 150))
            hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, 540))
            screen.blit(hint, hint_rect)
    
    def is_ready(self):
        return self.game_completed
    
    def get_winner(self):
        """Возвращает номер победителя (1 или 2)"""
        return self.winner
