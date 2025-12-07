
import pygame
import random
import math
from game.entities.coin import Coin
from game.utils.config import GameConfig

class CoinManager:
    def __init__(self, asset_adapter):
        self.asset_adapter = asset_adapter
        self.coins = []
        self.collected_coins = 0
        self.total_score = 0
        
        print("Inicializando gerenciador de moedas...")
        self.init_coins()
    
    def init_coins(self):
        
        self.coins = []

        for height in [450, 550, 650]:
            start_x = random.randint(300, 1000)
            for i in range(6):
                x = start_x + (i * 200)
                coin = Coin(x, height, self.asset_adapter)
                self.coins.append(coin)

        for _ in range(4):
            cluster_x = random.randint(1500, 3500)
            cluster_y = random.randint(450, 700)

            for angle in range(0, 360, 60):
                rad = math.radians(angle)
                radius = random.randint(80, 150)
                x = cluster_x + radius * math.cos(rad)
                y = cluster_y + radius * math.sin(rad) * 0.7
                coin = Coin(x, y, self.asset_adapter)
                self.coins.append(coin)

        remaining_coins = GameConfig.COIN_COUNT - len(self.coins)
        for _ in range(max(0, remaining_coins)):
            x = random.randint(
                GameConfig.COIN_SPAWN_MIN_X, 
                GameConfig.COIN_SPAWN_MAX_X
            )
            y = random.randint(
                GameConfig.COIN_SPAWN_MIN_Y,
                GameConfig.COIN_SPAWN_MAX_Y
            )

            too_close = False
            for existing_coin in self.coins:
                dist = math.sqrt((x - existing_coin.x)**2 + (y - existing_coin.y)**2)
                if dist < GameConfig.COIN_SIZE * 1.5:
                    too_close = True
                    break
            
            if not too_close:
                coin = Coin(x, y, self.asset_adapter)
                self.coins.append(coin)
        
        print(f"✅ {len(self.coins)} moedas criadas (tamanho: {GameConfig.COIN_SIZE}px)")
    
    def update(self, player_rect, delta_time):
        
        collected_this_frame = 0
        
        coins_to_remove = []
        
        for coin in self.coins:

            coin.update(delta_time)

            if not coin.collected and player_rect.colliderect(coin.get_rect()):
                if coin.collect():
                    collected_this_frame += 1
                    self.total_score += GameConfig.COIN_VALUE

            if coin.should_remove():
                coins_to_remove.append(coin)

        for coin in coins_to_remove:
            self.coins.remove(coin)
            self.collected_coins += 1
        
        return collected_this_frame
    
    def draw(self, graphics_adapter, camera_offset_x):
        
        for coin in self.coins:
            coin.draw(graphics_adapter, camera_offset_x)
    
    def get_remaining_coins(self):
        
        return len([c for c in self.coins if not c.collected])
    
    def get_total_coins(self):
        
        return len(self.coins)
    
    def get_score(self):
        
        return self.total_score
    
    def reset(self):
        
        self.coins = []
        self.collected_coins = 0
        self.total_score = 0
        self.init_coins()