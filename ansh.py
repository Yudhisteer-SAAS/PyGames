import pygame
import random

# Initialize pygame
pygame.init()

# Set the width and height of the window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the window title
pygame.display.set_caption("Dodge the Falling Blocks!")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Player settings
player_width = 50
player_height = 50
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10
player_speed = 5

# Block settings
block_width = 50
block_height = 50
block_speed = 5
block_frequency = 30

# Set up font for text display
font = pygame.font.SysFont(None, 30)

# Clock to control the frame rate
clock = pygame.time.Clock()

# Function to draw the player
def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, [x, y, player_width, player_height])

# Function to draw the blocks
def draw_block(x, y):
    pygame.draw.rect(screen, RED, [x, y, block_width, block_height])

# Function to display the score
def display_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, [100, 100])

# Function to check collision between player and block
def check_collision(player_x, player_y, block_x, block_y):
    if (player_x < block_x + block_width and
        player_x + player_width > block_x and
        player_y < block_y + block_height and
        player_y + player_height > block_y):
        return True
    return False

# Main game loop
def game_loop():
    # Game variables
    player_x = screen_width // 2 - player_width // 2
    player_y = screen_height - player_height - 10
    score = 0
    blocks = []

    game_over = False
    while not game_over:
        screen.fill(BLACK)

        # Check for events (key presses, quitting)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Get the keys pressed and move the player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += player_speed

        # Add new block periodically
        if random.randint(1, block_frequency) == 1:
            block_x = random.randint(0, screen_width - block_width)
            blocks.append([block_x, 0])

        # Move the blocks down
        for block in blocks[:]:
            block[1] += block_speed
            # Remove block if it goes off the screen
            if block[1] > screen_height:
                blocks.remove(block)
                score += 1
            # Check if the player collides with a block
            if check_collision(player_x, player_y, block[0], block[1]):
                game_over = True

            # Draw the block
            draw_block(block[0], block[1])

        # Draw the player
        draw_player(player_x, player_y)

        # Display the score
        display_score(score)

        # Update the display
        pygame.display.update()

        # Set the frame rate (frames per second)
        clock.tick(60)

    pygame.quit()

# Run the game
game_loop()