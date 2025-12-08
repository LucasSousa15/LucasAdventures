
import pygame
import random
import time
import os
from game.entities.obstacle import Obstacle
from game.utils.config import GameConfig

class GameManager:
    def __init__(self, asset_adapter):
        self.asset_adapter = asset_adapter
        self.obstacles = []
        self.score = 0
        self.high_score = self.load_high_score()
        self.game_speed = GameConfig.INITIAL_GAME_SPEED
        self.last_obstacle_time = GameConfig.SCREEN_WIDTH - 200
        self.is_game_over = False
        self.is_paused = False
        self.last_obstacle_x = GameConfig.SCREEN_WIDTH

        self.score_since_last_speed_increase = 0
        self.speed_increase_threshold = 100
    
    def load_high_score(self):
        
        try:
            if os.path.exists(GameConfig.HIGH_SCORE_FILE):
                with open(GameConfig.HIGH_SCORE_FILE, 'r') as f:
                    return int(f.read().strip())
        except:
            pass
        return 0
    
    def save_high_score(self):
        
        try:
            with open(GameConfig.HIGH_SCORE_FILE, 'w') as f:
                f.write(str(int(max(self.high_score, self.score))))
        except:
            pass
    
    def spawn_obstacle(self):
        

        obstacle_type = random.choice(['cactus', 'bird'])

        obstacle = Obstacle(obstacle_type, self.asset_adapter)
        print("[SPAWN] Criando obstáculo:", obstacle_type)


        min_x = GameConfig.SCREEN_WIDTH + GameConfig.OBSTACLE_MIN_GAP
        max_x = GameConfig.SCREEN_WIDTH + GameConfig.OBSTACLE_MAX_GAP
        obstacle.x = random.randint(min_x, max_x)

        if obstacle_type == 'bird':
            obstacle.y = obstacle.get_initial_y()

        self.last_obstacle_x = obstacle.x
        
        self.obstacles.append(obstacle)
    
    def update(self, delta_time, player_rect):
        
        if self.is_game_over or self.is_paused:
            return

        self.score += GameConfig.SCORE_MULTIPLIER * self.game_speed

        self.score_since_last_speed_increase += GameConfig.SCORE_MULTIPLIER
        if self.score_since_last_speed_increase >= self.speed_increase_threshold:
            self.game_speed = min(GameConfig.MAX_GAME_SPEED, 
                                 self.game_speed + GameConfig.GAME_SPEED_INCREASE * 100)
            self.score_since_last_speed_increase = 0

        current_time = pygame.time.get_ticks()
        if (current_time - self.last_obstacle_time > GameConfig.OBSTACLE_SPAWN_RATE / self.game_speed and
            len(self.obstacles) < GameConfig.OBSTACLE_COUNT):
            
            self.spawn_obstacle()
            self.last_obstacle_time = current_time

        obstacles_to_remove = []
        for obstacle in self.obstacles:


            try:
                obstacle.speed = GameConfig.OBSTACLE_SPEED * 100 * self.game_speed
            except Exception:
                pass

            if obstacle.update(delta_time):
                obstacles_to_remove.append(obstacle)
            elif player_rect.colliderect(obstacle.rect):
                self.game_over()
                return

        for obstacle in obstacles_to_remove:
            self.obstacles.remove(obstacle)

            if obstacle.x == self.last_obstacle_x and self.obstacles:
                self.last_obstacle_x = max(o.x for o in self.obstacles)
            elif not self.obstacles:
                self.last_obstacle_x = GameConfig.SCREEN_WIDTH
    
    def game_over(self):
        
        self.is_game_over = True
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
    
    def reset(self):
        
        self.obstacles = []
        self.score = 0
        self.game_speed = GameConfig.INITIAL_GAME_SPEED
        self.last_obstacle_time = pygame.time.get_ticks()
        self.is_game_over = False
        self.is_paused = False
        self.last_obstacle_x = GameConfig.SCREEN_WIDTH
        self.score_since_last_speed_increase = 0
    
    def toggle_pause(self):
        
        self.is_paused = not self.is_paused
    
    def draw(self, graphics_adapter):
        
        for obstacle in self.obstacles:
            obstacle.draw(graphics_adapter)
    
    def draw_ui(self, graphics_adapter, font, large_font):
        

        score_text = f"Pontuação: {int(self.score)}"
        score_surface = font.render(score_text, True, (0, 0, 0))
        score_rect = score_surface.get_rect(topright=(GameConfig.SCREEN_WIDTH - 20, 20))

        high_score_text = f"Recorde: {int(self.high_score)}"
        high_score_surface = font.render(high_score_text, True, (100, 100, 100))
        high_score_rect = high_score_surface.get_rect(topright=(GameConfig.SCREEN_WIDTH - 20, 60))

        speed_text = f"Velocidade: {self.game_speed:.1f}x"
        speed_surface = font.render(speed_text, True, (0, 100, 0))
        speed_rect = speed_surface.get_rect(topleft=(20, 20))

        graphics_adapter.screen.blit(score_surface, score_rect)
        graphics_adapter.screen.blit(high_score_surface, high_score_rect)
        graphics_adapter.screen.blit(speed_surface, speed_rect)

        if self.is_game_over:
            self.draw_game_over_screen(graphics_adapter, large_font)

        if self.is_paused:
            self.draw_pause_screen(graphics_adapter, large_font)
    
    def draw_game_over_screen(self, graphics_adapter, large_font):
        

        overlay = pygame.Surface((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(150)
        graphics_adapter.screen.blit(overlay, (0, 0))

        game_over_text = large_font.render("GAME OVER", True, (255, 50, 50))
        score_text = large_font.render(f"Pontuação: {int(self.score)}", True, (255, 255, 255))
        high_score_text = large_font.render(f"Recorde: {int(self.high_score)}", True, (255, 215, 0))
        restart_text = large_font.render("Pressione ESPAÇO para jogar novamente", True, (200, 200, 200))

        game_over_rect = game_over_text.get_rect(center=(GameConfig.SCREEN_WIDTH//2, 200))
        score_rect = score_text.get_rect(center=(GameConfig.SCREEN_WIDTH//2, 280))
        high_score_rect = high_score_text.get_rect(center=(GameConfig.SCREEN_WIDTH//2, 340))
        restart_rect = restart_text.get_rect(center=(GameConfig.SCREEN_WIDTH//2, 420))

        graphics_adapter.screen.blit(game_over_text, game_over_rect)
        graphics_adapter.screen.blit(score_text, score_rect)
        graphics_adapter.screen.blit(high_score_text, high_score_rect)
        graphics_adapter.screen.blit(restart_text, restart_rect)
    
    def draw_pause_screen(self, graphics_adapter, large_font):
        

        overlay = pygame.Surface((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(150)
        graphics_adapter.screen.blit(overlay, (0, 0))

        pause_text = large_font.render("PAUSADO", True, (255, 255, 100))
        continue_text = large_font.render("Pressione P para continuar", True, (200, 200, 200))

        pause_rect = pause_text.get_rect(center=(GameConfig.SCREEN_WIDTH//2, 250))
        continue_rect = continue_text.get_rect(center=(GameConfig.SCREEN_WIDTH//2, 350))

        graphics_adapter.screen.blit(pause_text, pause_rect)
        graphics_adapter.screen.blit(continue_text, continue_rect)