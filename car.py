import pygame
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
CAR_WIDTH = 50
CAR_HEIGHT = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Racing Game")
clock = pygame.time.Clock()

# Load car image
car_image = pygame.image.load("car.png")
car_image = pygame.transform.scale(car_image, (CAR_WIDTH, CAR_HEIGHT))

# Game variables
car_x = SCREEN_WIDTH // 2 - CAR_WIDTH // 2
car_y = SCREEN_HEIGHT - CAR_HEIGHT - 10
car_speed = 5
obstacle_width = 100
obstacle_height = 20
obstacle_speed = 5
obstacles = []

# Function to generate obstacles
def generate_obstacle():
    x = random.randint(0, SCREEN_WIDTH - obstacle_width)
    y = -obstacle_height
    obstacles.append(pygame.Rect(x, y, obstacle_width, obstacle_height))

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the car
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car_x -= car_speed
    if keys[pygame.K_RIGHT]:
        car_x += car_speed

    # Boundary check for the car
    if car_x < 0:
        car_x = 0
    elif car_x > SCREEN_WIDTH - CAR_WIDTH:
        car_x = SCREEN_WIDTH - CAR_WIDTH

    # Generate obstacles
    if random.randint(0, 100) < 2:
        generate_obstacle()

    # Move and draw obstacles
    for obstacle in obstacles:
        obstacle.y += obstacle_speed
        pygame.draw.rect(screen, RED, obstacle)

        # Collision detection
        if obstacle.colliderect(pygame.Rect(car_x, car_y, CAR_WIDTH, CAR_HEIGHT)):
            running = False

    # Draw the car
    screen.blit(car_image, (car_x, car_y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()