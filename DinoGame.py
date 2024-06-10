import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = SCREEN_HEIGHT - 70
DINO_WIDTH = 50
DINO_HEIGHT = 50
OBSTACLE_WIDTH = 20
OBSTACLE_HEIGHT = 50
OBSTACLE_SPEED = 10
GRAVITY = 1

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GROUND_COLOR = (150, 75, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Game")

# Load Dino image
dino_image = pygame.image.load("DinoImage.png")
dino_image = pygame.transform.scale(dino_image, (DINO_WIDTH, DINO_HEIGHT))

# Load Obstacle image
obstacle_image = pygame.image.load("Obstacles.png")
obstacle_image = pygame.transform.scale(obstacle_image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

# Load background image
background_image = pygame.image.load("Background.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Dino class
class Dino:
    def __init__(self):
        self.x = 50
        self.y = GROUND_HEIGHT - DINO_HEIGHT
        self.jump_speed = 15
        self.is_jumping = False
        self.vertical_speed = 0

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.vertical_speed = -self.jump_speed

    def update(self):
        if self.is_jumping:
            self.y += self.vertical_speed
            self.vertical_speed += GRAVITY
            if self.y >= GROUND_HEIGHT - DINO_HEIGHT:
                self.y = GROUND_HEIGHT - DINO_HEIGHT
                self.is_jumping = False
                self.vertical_speed = 0

    def draw(self):
        screen.blit(dino_image, (self.x, self.y))

# Obstacle class
class Obstacle:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.y = GROUND_HEIGHT - OBSTACLE_HEIGHT

    def update(self):
        self.x -= OBSTACLE_SPEED
        if self.x < -OBSTACLE_WIDTH:
            self.x = SCREEN_WIDTH
            self.y = GROUND_HEIGHT - OBSTACLE_HEIGHT

    def draw(self):
        screen.blit(obstacle_image, (self.x, self.y))

# Main game loop
def main():
    clock = pygame.time.Clock()
    dino = Dino()
    obstacles = [Obstacle() for _ in range(3)]
    score = 0
    font = pygame.font.Font(None, 36)
    background_x = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dino.jump()

        dino.update()
        for obstacle in obstacles:
            obstacle.update()

        # Check for collision
        for obstacle in obstacles:
            if (dino.x < obstacle.x + OBSTACLE_WIDTH and
                dino.x + DINO_WIDTH > obstacle.x and
                dino.y < obstacle.y + OBSTACLE_HEIGHT and
                dino.y + DINO_HEIGHT > obstacle.y):
                running = False

        # Update background position
        background_x -= OBSTACLE_SPEED // 2
        if background_x <= -SCREEN_WIDTH:
            background_x = 0

        # Draw everything
        screen.fill(WHITE)
        screen.blit(background_image, (background_x, 0))
        screen.blit(background_image, (background_x + SCREEN_WIDTH, 0))

        pygame.draw.rect(screen, GROUND_COLOR, (0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))

        dino.draw()
        for obstacle in obstacles:
            obstacle.draw()

        # Update score
        score += 1
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
