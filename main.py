# main.py - Para frames separados manualmente
import pygame
import sys
import os

pygame.init()

# --- CONFIGURAÇÃO ---
SCREEN_W = 1920
SCREEN_H = 1080
SCREEN = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Lucas Adventure - Frames Otimizados")
clock = pygame.time.Clock()

def carregar_frames():
    """Carrega os frames separados manualmente - RÁPIDO E CONFIÁVEL"""
    frames = {"idle": [], "walk": [], "jump": []}
    
    frames_dir = os.path.join("assets", "player_frames")
    
    if not os.path.exists(frames_dir):
        print(f"ERRO: Pasta '{frames_dir}' não encontrada!")
        sys.exit("Crie a pasta assets/player_frames com os frames separados")
    
    # Carrega cada animação
    for animacao in frames.keys():
        for i in range(3):  # 3 frames por animação
            frame_path = os.path.join(frames_dir, f"{animacao}_{i}.png")
            
            if os.path.exists(frame_path):
                try:
                    frame = pygame.image.load(frame_path).convert_alpha()
                    frames[animacao].append(frame)
                    print(f"✓ Carregado: {animacao}_{i}.png")
                except Exception as e:
                    print(f"✗ Erro ao carregar {frame_path}: {e}")
                    # Frame de fallback (cor diferente para cada animação)
                    surf = pygame.Surface((120, 160))
                    colors = {"idle": (255, 100, 100), "walk": (100, 255, 100), "jump": (100, 100, 255)}
                    surf.fill(colors.get(animacao, (255, 0, 255)))
                    frames[animacao].append(surf)
            else:
                print(f"✗ Frame não encontrado: {frame_path}")
                # Frame de fallback
                surf = pygame.Surface((120, 160))
                surf.fill((255, 0, 255))
                frames[animacao].append(surf)
    
    return frames

# Carrega todos os frames
print("=== CARREGANDO FRAMES ===")
FRAMES = carregar_frames()
print("=== FRAMES CARREGADOS ===\n")

# Obtém dimensões do primeiro frame (assume que todos têm mesmo tamanho)
if FRAMES["idle"]:
    FRAME_WIDTH = FRAMES["idle"][0].get_width()
    FRAME_HEIGHT = FRAMES["idle"][0].get_height()
    print(f"Dimensões dos frames: {FRAME_WIDTH}x{FRAME_HEIGHT}")
else:
    FRAME_WIDTH, FRAME_HEIGHT = 120, 160
    print("Usando dimensões padrão para fallback")

class Player:
    def __init__(self, x, ground_y):
        self.ground_y = ground_y 
        self.action = "idle"
        self.image = FRAMES["idle"][0]
        self.frame_idx = 0.0
        self.flip = False
        
        # Física
        self.vy = 0
        self.on_ground = True
        
        # Hitbox (ajustada para o tamanho real dos frames)
        self.rect = pygame.Rect(0, 0, FRAME_WIDTH * 0.6, FRAME_HEIGHT * 0.8)
        self.rect.midbottom = (x, ground_y)

    def update(self, keys):
        dx = 0
        speed = 8
        
        # Controles de movimento
        if keys[pygame.K_LEFT]:
            dx = -speed
            self.flip = True
            if self.on_ground: 
                self.action = "walk"
        elif keys[pygame.K_RIGHT]:
            dx = speed
            self.flip = False
            if self.on_ground: 
                self.action = "walk"
        else:
            if self.on_ground: 
                self.action = "idle"

        # Pulo
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vy = -20
            self.on_ground = False
            self.action = "jump"
        
        # Animação de queda
        if not self.on_ground and self.vy > 0: 
            self.action = "jump"

        # Aplica física
        self.vy += 1.0  # Gravidade
        self.rect.x += dx
        self.rect.y += self.vy

        # Colisão com o chão
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.vy = 0
            self.on_ground = True
        
        # Atualiza animação
        anim_len = len(FRAMES[self.action])
        self.frame_idx += 0.15  # Velocidade da animação
        
        if self.action == "jump":
            # Trava no último frame do pulo
            if self.frame_idx >= anim_len: 
                self.frame_idx = anim_len - 1
        else:
            # Loop para animações contínuas
            if self.frame_idx >= anim_len: 
                self.frame_idx = 0
            
        self.image = FRAMES[self.action][int(self.frame_idx)]

    def draw(self, surf):
        img = self.image
        if self.flip: 
            img = pygame.transform.flip(img, True, False)
        
        # Centraliza a imagem sobre a hitbox
        draw_x = self.rect.centerx - img.get_width() // 2
        draw_y = self.rect.bottom - img.get_height()
        
        surf.blit(img, (draw_x, draw_y))
        
        # DEBUG: Mostra hitbox (comente esta linha na versão final)
        pygame.draw.rect(surf, (0, 255, 0), self.rect, 2)

def main():
    ground_y = SCREEN_H - 100
    player = Player(SCREEN_W // 2, ground_y)
    
    # Fonte para debug (opcional)
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Atualiza
        keys = pygame.key.get_pressed()
        player.update(keys)

        # Renderiza
        SCREEN.fill((135, 206, 235))  # Céu azul
        
        # Chão
        pygame.draw.rect(SCREEN, (50, 200, 50), (0, ground_y, SCREEN_W, SCREEN_H - ground_y))
        
        # Player
        player.draw(SCREEN)
        
        # Informações na tela (debug)
        debug_text = f"Ação: {player.action} | Frame: {int(player.frame_idx)} | Pos: ({player.rect.x}, {player.rect.y})"
        text_surface = font.render(debug_text, True, (0, 0, 0))
        SCREEN.blit(text_surface, (10, 10))
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()