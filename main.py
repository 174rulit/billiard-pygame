#
"""
Классический пул для двоих на Pygame
Один биток, треугольник из 15 шаров, игра по очереди
"""

import pygame
import sys
from config import *
from game import BilliardGame
from ui import UI

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("🎱 Классический пул для двоих")
    
    game = BilliardGame()
    ui = UI(screen)
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game.balls_moving and game.game_active and not game.winner:
                    cue_ball = game.get_cue_ball()
                    if cue_ball and not cue_ball.in_pocket:
                        pos = pygame.mouse.get_pos()
                        # Игрок 1 - ЛКМ, Игрок 2 - ПКМ
                        if (event.button == 1 and game.current_player == 1) or \
                           (event.button == 3 and game.current_player == 2):
                            # Проверка клика по битку
                            dx = pos[0] - cue_ball.x
                            dy = pos[1] - cue_ball.y
                            if (dx * dx + dy * dy) ** 0.5 <= cue_ball.radius + 10:
                                game.dragging = True
                                game.drag_start = (cue_ball.x, cue_ball.y)
                                game.drag_end = pos
            
            elif event.type == pygame.MOUSEMOTION:
                if game.dragging:
                    game.drag_end = pygame.mouse.get_pos()
                    dx = game.drag_start[0] - game.drag_end[0]
                    dy = game.drag_start[1] - game.drag_end[1]
                    dist = min(((dx * dx + dy * dy) ** 0.5), 150)
                    game.power = (dist / 150) * 22
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if game.dragging:
                    game.shoot(game.drag_start, game.drag_end)
                    game.dragging = False
                    game.power = 0
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.new_game()
                elif event.key == pygame.K_r:
                    if not game.balls_moving:
                        game.reset_cue_ball()
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        game.update_physics()
        
        # Отрисовка
        ui.draw_table()
        
        if game.dragging and game.drag_start and game.drag_end and not game.balls_moving:
            ui.draw_aim_line(game.drag_start, game.drag_end)
        
        for ball in game.balls:
            ball.draw(screen)
        
        ui.draw_scores(game.scores, game.current_player, 
                      game.player1_type, game.player2_type)
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
