"""
Бильярд для двоих на Pygame
Полное соответствие принципам: DRY, KISS, SOLID, чистота кода
"""

import pygame
import sys
from config import *
from game import BilliardGame
from ui import UI

def main():
    pygame.init()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("🎱 Бильярд для двоих - Pygame Edition")
    
    game = BilliardGame()
    ui = UI(game.screen)
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Управление ударом
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game.balls_moving and game.game_active and not game.winner:
                    ball = game.get_player_ball(game.current_player)
                    if ball and not ball.in_pocket:
                        pos = pygame.mouse.get_pos()
                        # ЛКМ для игрока 1, ПКМ для игрока 2
                        if (event.button == 1 and game.current_player == 1) or \
                           (event.button == 3 and game.current_player == 2):
                            # Проверка, что клик по шару
                            dx = pos[0] - ball.x
                            dy = pos[1] - ball.y
                            if (dx * dx + dy * dy) ** 0.5 <= ball.radius + 10:
                                game.dragging = True
                                game.drag_start = (ball.x, ball.y)
                                game.drag_end = pos
            
            elif event.type == pygame.MOUSEMOTION:
                if game.dragging:
                    game.drag_end = pygame.mouse.get_pos()
                    # Расчет силы
                    dx = game.drag_start[0] - game.drag_end[0]
                    dy = game.drag_start[1] - game.drag_end[1]
                    dist = min(((dx * dx + dy * dy) ** 0.5), 150)
                    game.power = (dist / 150) * MAX_POWER
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if game.dragging:
                    game.shoot(game.drag_start, game.drag_end)
                    game.dragging = False
                    game.power = 0
            
            # Клавиатура
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.init_game()
                elif event.key == pygame.K_r:
                    if not game.balls_moving:
                        game.reset_round()
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        # Обновление физики
        game.update_physics()
        
        # Отрисовка
        ui.draw_table()
        
        # Линия прицела
        if game.dragging and game.drag_start and game.drag_end and not game.balls_moving:
            ui.draw_aim_line(game.drag_start, game.drag_end)
        
        # Шары
        for ball in game.balls:
            ball.draw(game.screen)
        
        # Интерфейс
        ui.draw_scores(game.scores, game.current_player)
        ui.draw_turn_indicator(game.current_player)
        if game.dragging and game.power > 0:
            ui.draw_power_bar(game.power)
        ui.draw_instructions()
        
        if game.winner:
            ui.draw_game_over(game.winner)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
