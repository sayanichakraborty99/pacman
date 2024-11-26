import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Pac-Man")
clock = pygame.time.Clock()

# Maze layout (1 = wall, 0 = empty, 2 = pellet, 3 = power pellet)
MAZE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 3, 1, 2, 1, 2, 1, 3, 1, 3, 1, 2, 1],
    [1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

TILE_WIDTH = WIDTH // len(MAZE[0])
TILE_HEIGHT = HEIGHT // len(MAZE)

# Pac-Man class
class PacMan:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.direction = None
        self.next_direction = None
        self.score = 0

    def move(self):
        if self.next_direction:
            new_x, new_y = self.x, self.y
            if self.next_direction == 'UP':
                new_y -= 1
            elif self.next_direction == 'DOWN':
                new_y += 1
            elif self.next_direction == 'LEFT':
                new_x -= 1
            elif self.next_direction == 'RIGHT':
                new_x += 1
            
            if MAZE[new_y][new_x] != 1:
                self.direction = self.next_direction

        if self.direction == 'UP' and MAZE[self.y - 1][self.x] != 1:
            self.y -= 1
        elif self.direction == 'DOWN' and MAZE[self.y + 1][self.x] != 1:
            self.y += 1
        elif self.direction == 'LEFT' and MAZE[self.y][self.x - 1] != 1:
            self.x -= 1
        elif self.direction == 'RIGHT' and MAZE[self.y][self.x + 1] != 1:
            self.x += 1

        if MAZE[self.y][self.x] == 2:
            self.score += 10
            MAZE[self.y][self.x] = 0
        elif MAZE[self.y][self.x] == 3:
            self.score += 50
            MAZE[self.y][self.x] = 0

    def draw(self):
        pygame.draw.circle(
            screen, YELLOW, 
            (self.x * TILE_WIDTH + TILE_WIDTH // 2, self.y * TILE_HEIGHT + TILE_HEIGHT // 2), 
            TILE_WIDTH // 2 - 5
        )

# Ghost class
class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def move(self):
        # Simple random movement
        directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        random.shuffle(directions)
        for direction in directions:
            new_x, new_y = self.x, self.y
            if direction == 'UP':
                new_y -= 1
            elif direction == 'DOWN':
                new_y += 1
            elif direction == 'LEFT':
                new_x -= 1
            elif direction == 'RIGHT':
                new_x += 1
            
            if MAZE[new_y][new_x] != 1:
                self.x, self.y = new_x, new_y
                break

    def draw(self):
        pygame.draw.circle(
            screen, self.color,
            (self.x * TILE_WIDTH + TILE_WIDTH // 2, self.y * TILE_HEIGHT + TILE_HEIGHT // 2),
            TILE_WIDTH // 2 - 5
        )

# Main game loop
def main():
    pacman = PacMan()
    ghosts = [Ghost(5, 5, RED), Ghost(5, 3, BLUE), Ghost(3, 5, GREEN)]

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pacman.next_direction = 'UP'
                elif event.key == pygame.K_DOWN:
                    pacman.next_direction = 'DOWN'
                elif event.key == pygame.K_LEFT:
                    pacman.next_direction = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    pacman.next_direction = 'RIGHT'

        # Draw maze
        for y, row in enumerate(MAZE):
            for x, tile in enumerate(row):
                if tile == 1:
                    pygame.draw.rect(
                        screen, WHITE,
                        (x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
                    )
                elif tile == 2:
                    pygame.draw.circle(
                        screen, WHITE,
                        (x * TILE_WIDTH + TILE_WIDTH // 2, y * TILE_HEIGHT + TILE_HEIGHT // 2),
                        5
                    )
                elif tile == 3:
                    pygame.draw.circle(
                        screen, BLUE,
                        (x * TILE_WIDTH + TILE_WIDTH // 2, y * TILE_HEIGHT + TILE_HEIGHT // 2),
                        8
                    )

        # Move and draw Pac-Man
        pacman.move()
        pacman.draw()

        # Move and draw ghosts
        for ghost in ghosts:
            ghost.move()
            ghost.draw()

        # Check collisions
        for ghost in ghosts:
            if pacman.x == ghost.x and pacman.y == ghost.y:
                print("Game Over! Final Score:", pacman.score)
                running = False

        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {pacman.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
  
