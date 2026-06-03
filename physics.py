#
import math
from config import TABLE_MARGIN, SCREEN_WIDTH, SCREEN_HEIGHT, WALL_BOUNCE_DAMP

class Physics:
    @staticmethod
    def check_wall_collision(ball, margin):
        left = margin + ball.radius
        right = SCREEN_WIDTH - margin - ball.radius
        top = margin + ball.radius
        bottom = SCREEN_HEIGHT - margin - ball.radius
        
        collided = False
        
        if ball.x < left:
            ball.x = left
            ball.vx = -ball.vx * WALL_BOUNCE_DAMP
            collided = True
        if ball.x > right:
            ball.x = right
            ball.vx = -ball.vx * WALL_BOUNCE_DAMP
            collided = True
        if ball.y < top:
            ball.y = top
            ball.vy = -ball.vy * WALL_BOUNCE_DAMP
            collided = True
        if ball.y > bottom:
            ball.y = bottom
            ball.vy = -ball.vy * WALL_BOUNCE_DAMP
            collided = True
        
        return collided
    
    @staticmethod
    def resolve_ball_collision(b1, b2):
        dx = b2.x - b1.x
        dy = b2.y - b1.y
        distance = math.sqrt(dx * dx + dy * dy)
        min_dist = b1.radius + b2.radius
        
        if distance < min_dist and distance > 0:
            nx = dx / distance
            ny = dy / distance
            
            vrel_x = b2.vx - b1.vx
            vrel_y = b2.vy - b1.vy
            vrel_dot_n = vrel_x * nx + vrel_y * ny
            
            if vrel_dot_n < 0:
                e = 0.95
                impulse = (1 + e) * vrel_dot_n / 2
                
                b1.vx += impulse * nx
                b1.vy += impulse * ny
                b2.vx -= impulse * nx
                b2.vy -= impulse * ny
            
            overlap = min_dist - distance
            correction_x = (dx / distance) * overlap * 0.5
            correction_y = (dy / distance) * overlap * 0.5
            b1.x -= correction_x
            b1.y -= correction_y
            b2.x += correction_x
            b2.y += correction_y
            
            return True
        return False
    
    @staticmethod
    def check_pocket_collision(ball, pockets, pocket_radius):
        for px, py in pockets:
            dx = ball.x - px
            dy = ball.y - py
            dist = math.sqrt(dx * dx + dy * dy)
            if dist < pocket_radius:
                if not ball.in_pocket:
                    ball.in_pocket = True
                    return True, (px, py)
        return False, None
    
    @staticmethod
    def calculate_shoot_direction(start_pos, end_pos):
        dx = start_pos[0] - end_pos[0]
        dy = start_pos[1] - end_pos[1]
        distance = math.sqrt(dx * dx + dy * dy)
        max_dist = 180
        distance = min(distance, max_dist)
        
        power = (distance / max_dist) * 25
        
        if distance > 15:
            fx = dx / distance
            fy = dy / distance
            return fx, fy, power
        return 0, 0, 0
