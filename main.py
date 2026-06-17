
import pygame
import sys
from config import *
from game import BilliardGame
from ui import UI

def init_music():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(MUSIC_FILE)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
        print("🎵 Музыка запущена")
    except Exception as e:
        print(f"⚠️ Не удалось загрузить музыку: {e}")

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("🎱 Бильярд 2D - Poolians Style")
    
    init_music()
    
    game = BilliardGame()
    game.set_screen(screen)
    game.load_sounds()
    
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
                        if (event.button == 1 and game.current_player == 1) or \
                           (event.button == 3 and game.current_player == 2):
                            dx = pos[0] - cue_ball.x
                            dy = pos[1] - cue_ball.y
                            if (dx * dx + dy * dy) ** 0.5 <= cue_ball.radius + 20:
                                game.dragging = True
                                game.drag_start = (cue_ball.x, cue_ball.y)
                                game.drag_end = pos
            
            elif event.type == pygame.MOUSEMOTION:
                if game.dragging:
                    game.drag_end = pygame.mouse.get_pos()
                    dx = game.drag_start[0] - game.drag_end[0]
                    dy = game.drag_start[1] - game.drag_end[1]
                    dist = min(((dx * dx + dy * dy) ** 0.5), 180)
                    game.power = (dist / 180) * 25
            
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
                elif event.key == pygame.K_m:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        game.update_physics()
        
        # Отрисовка
        ui.draw_table()
        ui.draw_player_panels(game.scores, game.current_player, 
                              game.player1_type, game.player2_type)
        
        # ТРАЕКТОРИЯ ПОЛЁТА (исправленная - вперёд от шара)
        if game.dragging and game.drag_start and game.drag_end and not game.balls_moving:
            cue_ball = game.get_cue_ball()
            ui.draw_trajectory(game.drag_start, game.drag_end, cue_ball)
        
        # Шары
        for ball in game.balls:
            ball.draw(screen)
        
        # Шкала силы
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
