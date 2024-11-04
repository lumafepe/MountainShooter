import pygame
import random
import sys
from preencher import disparaMontanhaMaisAlta
import math

# Inicializar pygame
pygame.init()

# Dimensões da janela
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Destroi a Montanha Mais Alta")

# Cores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

MIN_HEIGHT = 0
MAX_HEIGHT = 200
MIN_WIDTH = 1
MAX_WIDTH = 10

# Fonte de letra para niveis alturas e índices
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)
win_font = pygame.font.Font(None, 72) 


# Função para gerar montanhas de altura aleatória
def generate_mountains(num_mountains):
    heights = [
        random.randint(MIN_HEIGHT, MAX_HEIGHT) for _ in range(num_mountains)
    ]
    return heights


# Função para desenhar montanhas
def draw_mountains(heights):
    mountain_width = WIDTH // len(heights)
    peak_points = []

    # Calcular picos das montanhas como x,y
    for i, height in enumerate(heights):
        peak_x = i * mountain_width + mountain_width // 2
        peak_y = HEIGHT - height
        peak_points.append((peak_x, peak_y))

    # Adicionar ponto inicial e final para a montanha começar e terminar no chão
    peak_points = [(0, HEIGHT)] + peak_points + [(WIDTH, HEIGHT)]

    # Desenhar montanhas
    pygame.draw.polygon(screen, GREEN, peak_points)

    # Desenhar contorno das montanhas
    pygame.draw.lines(screen, BLACK, False, peak_points, 5)

    # Mostrar altura e índice das montanhas
    for i, height in enumerate(heights):
        peak_x = i * mountain_width + mountain_width // 2
        peak_y = HEIGHT - height

        # Mostra a altura no topo da montanha
        height_text = small_font.render(str(height), True, BLACK)
        screen.blit(height_text, (peak_x - 10, peak_y - 30))

        # Mostra o índice da montanha na parte inferior
        index_text = small_font.render(str(i), True, BLACK)
        screen.blit(index_text, (peak_x - 10, HEIGHT - 20))


# Função para simular laser disparado na montanha
def shoot_ray(mountain_index, heights):
    mountain_width = WIDTH // len(heights)
    mountain_height = heights[mountain_index]

    # Desenhar raio vermelho do topo da tela até o pico da montanha
    ray_origin = (WIDTH // 2, 50)
    mountain_center = (mountain_index * mountain_width + mountain_width // 2,
                       HEIGHT - mountain_height)

    pygame.draw.line(screen, RED, ray_origin, mountain_center, 5)
    pygame.display.update()
    pygame.time.delay(1000) # Duração do raio


# Função para desenhar o laser
def draw_player():
    player_width = 50
    pygame.draw.rect(
        screen, BLUE,
        (WIDTH // 2 - player_width // 2, 20, player_width, player_width))


def main():
    running = True
    clock = pygame.time.Clock()
    level = 1

    # Gerar número de montanhas aleatórias
    num_mountains = random.randint(
        MIN_WIDTH, MAX_WIDTH)
    heights = generate_mountains(num_mountains)

    while running:
        screen.fill(WHITE)

        # Desenhar montanhas
        draw_mountains(heights)

        # Desenhar laser
        draw_player()

        # Mostrar nível atual
        level_text = font.render(f"Level: {level}", True, (0, 0, 0))
        screen.blit(level_text, (WIDTH - 150, 10))

        pygame.display.update()
        
        print(f"Altura das Montanhas: {heights}")
        
        # Jogador escolhe a montanha mais alta
        player_input = disparaMontanhaMaisAlta(heights)
        
        print(f"A montanha escolhida foi: {player_input}")

        # Check if the player input is correct
        try:
            tallest_height = max(heights)
            if heights[int(player_input)] == tallest_height:
                shoot_ray(player_input,
                          heights)  # Simula o laser disparado na montanha
                heights[player_input] = math.floor(
                    heights[player_input] /
                    2)  # Reduz a altura da montanha pela metade
            else:
                print("Montanha Errada!")
        except ValueError:
            print("Montanha Invalida!")
        except IndexError:
            print("Montanha Invalida!")

        # Verifica se todas as montanhas foram destruídas
        if all(height == 0 for height in heights):
            screen.fill(WHITE)
            win_text = win_font.render("GANHASTE!", True, BLACK)
            screen.blit(win_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
            pygame.display.update()
            pygame.time.delay(10000)  # Espera 10 segundos
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        clock.tick(60)  # 60 FPS


if __name__ == "__main__":
    main()

