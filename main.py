import pygame
import random
import sys
from preencher import disparaMontanhaMaisAlta
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mountain Destroyer")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

MIN_HEIGHT = 0
MAX_HEIGHT = 200
MIN_WIDTH = 1
MAX_WIDTH = 10

# Font for levels, heights, and indices
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)
win_font = pygame.font.Font(None, 72)  # Larger font for win message


# Function to generate mountains
def generate_mountains(num_mountains):
    heights = [
        random.randint(MIN_HEIGHT, MAX_HEIGHT) for _ in range(num_mountains)
    ]
    return heights


# Function to display connected mountain peaks with outlines
def draw_mountains(heights):
    mountain_width = WIDTH // len(heights)
    peak_points = []

    # Create the peak points for the mountain range
    for i, height in enumerate(heights):
        peak_x = i * mountain_width + mountain_width // 2
        peak_y = HEIGHT - height
        peak_points.append((peak_x, peak_y))

    # Add the first and last points to connect the range to the bottom of the screen
    peak_points = [(0, HEIGHT)] + peak_points + [(WIDTH, HEIGHT)]

    # Draw the filled mountain range
    pygame.draw.polygon(screen, GREEN, peak_points)

    # Draw the outline of the mountain range
    pygame.draw.lines(screen, BLACK, False, peak_points, 5)

    # Display the height at the top of each peak and the index at the bottom
    for i, height in enumerate(heights):
        peak_x = i * mountain_width + mountain_width // 2
        peak_y = HEIGHT - height

        # Display the height at the top of the peak
        height_text = small_font.render(str(height), True, BLACK)
        screen.blit(height_text, (peak_x - 10, peak_y - 30))

        # Display the index at the bottom of the peak
        index_text = small_font.render(str(i), True, BLACK)
        screen.blit(index_text, (peak_x - 10, HEIGHT - 20))


# Function to shoot and destroy mountain
def shoot_ray(mountain_index, heights):
    mountain_width = WIDTH // len(heights)
    mountain_height = heights[mountain_index]

    # Draw ray (red line) from the blue square at the top center
    ray_origin = (WIDTH // 2, 50)
    mountain_center = (mountain_index * mountain_width + mountain_width // 2,
                       HEIGHT - mountain_height)

    pygame.draw.line(screen, RED, ray_origin, mountain_center, 5)
    pygame.display.update()
    pygame.time.delay(1000)  # Longer delay for ray effect (1.5 seconds)


# Function to draw the blue player square at the top
def draw_player():
    player_width = 50
    pygame.draw.rect(
        screen, BLUE,
        (WIDTH // 2 - player_width // 2, 20, player_width, player_width))


def main():
    running = True
    clock = pygame.time.Clock()
    level = 1

    # Generate random mountains
    num_mountains = random.randint(
        MIN_WIDTH, MAX_WIDTH)  # Random number of mountains between 3 and 10
    heights = generate_mountains(num_mountains)

    while running:
        screen.fill(WHITE)

        # Draw mountains with peaks and outlines
        draw_mountains(heights)

        # Draw the player (blue square at the top)
        draw_player()

        # Display level passed
        level_text = font.render(f"Level: {level}", True, (0, 0, 0))
        screen.blit(level_text, (WIDTH - 150, 10))

        pygame.display.update()

        # Player inputs the index of the tallest mountain
        tallest_height = max(heights)
        print(f"Altura das Montanhas: {heights}")

        player_input = disparaMontanhaMaisAlta(heights)

        print(f"A montanha escolhida foi: {player_input}")

        # Check if the player input is correct
        try:
            if heights[int(player_input)] == tallest_height:
                shoot_ray(player_input,
                          heights)  # Simulate shooting the mountain
                heights[player_input] = math.floor(
                    heights[player_input] /
                    2)  # Destroy the mountain (reduce its height)
            else:
                print("Montanha Errada!")
        except ValueError:
            print("Montanha Invalida!")
        except IndexError:
            print("Montanha Invalida!")

        # Check if all mountains are destroyed (heights == 0)
        if all(height == 0 for height in heights):
            # Display "YOU WIN" message
            screen.fill(WHITE)
            win_text = win_font.render("YOU WIN!", True, BLACK)
            screen.blit(win_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
            pygame.display.update()
            pygame.time.delay(10000)  # Pause for 5 seconds
            running = False

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        clock.tick(60)  # Limit the frame rate to 60 FPS


if __name__ == "__main__":
    main()

