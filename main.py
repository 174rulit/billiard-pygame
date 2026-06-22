import pygame
import sys
from config import *
from game import BilliardGame
from ui import UI
from menu import Menu
from guess_game import GuessGame

def init_music():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(MUSIC_FILE)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
        print("🎵 Музыка запущена")
    except:
        print("⚠️ Не удалось загрузить музыку")

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("🎱 Бильярд 2D")
    
    init_music()
    
    STATE_MENU = 0
    STATE_GUESS = 1
    STATE_GAME = 2
    
    state = STATE_MENU
    
    menu = Menu()
    guess_game = None
    game = None
    ui = UI()
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if state == STATE_MENU:
                menu.handle_event(event)
                if menu.is_ready():
                    player1_name, player2_name = menu.get_names()
                    guess_game = GuessGame(player1_name, player2_name)
                    state = STATE_GUESS
            
            elif state == STATE_GUESS:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if guess_game.game_completed and guess_game.button_rect:
                        if guess_game.button_rect.collidepoint(event.pos):
                            winner = guess_game.get_winner()
                            player1_name = guess_game.player1_name
                            player2_name = guess_game.player2_name
                            
                            game = BilliardGame(player1_name, player2_name)
                            game.load_sounds()
                            
                            if winner == 2:
                                game.current_player = 2
                                game.player1_name = player2_name
                                game.player2_name = player1_name
                            
                            state = STATE_GAME
                
                guess_game.handle_event(event)
            
            elif state == STATE_GAME:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not game.balls_moving and game.game_active and not game.winner:
                        cue_ball = game.get_cue_ball()
                        if cue_ball and not cue_ball.in_pocket:
                            pos = pygame.mouse.get_pos()
                            dx = pos[0] - cue_ball.x
                            dy = pos[1] - cue_ball.y
                            if (dx*dx + dy*dy) ** 0.5 <= cue_ball.radius + 25:
                                game.dragging = True
                                game.drag_start = (cue_ball.x, cue_ball.y)
                                game.drag_end = pos
                
                elif event.type == pygame.MOUSEMOTION:
                    if game.dragging:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        game.drag_end = (mouse_x, mouse_y)
                        dx = game.drag_start[0] - game.drag_end[0]
                        dy = game.drag_start[1] - game.drag_end[1]
                        dist = min(((dx*dx + dy*dy) ** 0.5), 180)
                        game.power = (dist / 180) * 25
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    if game.dragging and event.button == 1:
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
        
        # Отрисовка
        if state == STATE_MENU:
            menu.update()
            menu.draw(screen)
        
        elif state == STATE_GUESS:
            guess_game.update()
            guess_game.draw(screen)
        
        elif state == STATE_GAME:
            game.update_physics()
            
            ui.draw_table(screen)
            ui.draw_player_panels(screen, game)
            
            if game.dragging and game.drag_start and game.drag_end and not game.balls_moving:
                cue_ball = game.get_cue_ball()
                ui.draw_cue_and_trajectory(screen, game.drag_start, game.drag_end, cue_ball)
            
            for ball in game.balls:
                ball.draw(screen)
            
            if game.dragging and game.power > 0:
                ui.draw_power_bar(screen, game.power)
            
            ui.draw_instructions(screen)
            
            if game.winner:
                ui.draw_game_over(screen, game.winner, game.player1_name, game.player2_name)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
