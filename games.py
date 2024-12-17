import pygame
import random
import sys

# Snake Game Function
def snake_game():
    pygame.init()

    # Screen dimensions
    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")

    # Colors
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)

    # Game variables
    clock = pygame.time.Clock()
    snake_pos = [100, 50]  # Initial position
    snake_body = [[100, 50], [90, 50], [80, 50]]  # Initial snake body
    direction = 'RIGHT'
    change_to = direction
    speed = 15
    score = 0

    # Food position
    food_pos = [random.randrange(1, (WIDTH // 10)) * 10,
                random.randrange(1, (HEIGHT // 10)) * 10]
    food_spawn = True

    def show_score():
        font = pygame.font.SysFont('arial', 25)
        score_surface = font.render(f'Score: {score}', True, BLACK)
        screen.blit(score_surface, (10, 10))

    def game_over():
        font = pygame.font.SysFont('arial', 35)
        game_over_surface = font.render(f'Game Over! Score: {score}', True, RED)
        screen.blit(game_over_surface, (WIDTH // 2 - game_over_surface.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(3000)

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not direction == 'DOWN':
                    change_to = 'UP'
                if event.key == pygame.K_DOWN and not direction == 'UP':
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT and not direction == 'RIGHT':
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT and not direction == 'LEFT':
                    change_to = 'RIGHT'
                if event.key == pygame.K_q:  # Quit confirmation
                    if confirm_quit():
                        return score

        # Update direction
        direction = change_to

        # Update snake position
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        # Snake body growing
        snake_body.insert(0, list(snake_pos))
        if snake_pos == food_pos:
            score += 10
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, (WIDTH // 10)) * 10,
                        random.randrange(1, (HEIGHT // 10)) * 10]
        food_spawn = True

        # Draw snake and food
        for block in snake_body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(block[0], block[1], 10, 10))
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Game over conditions
        if snake_pos[0] < 0 or snake_pos[0] >= WIDTH or snake_pos[1] < 0 or snake_pos[1] >= HEIGHT:
            game_over()
            return score
        for block in snake_body[1:]:
            if snake_pos == block:
                game_over()
                return score

        show_score()
        pygame.display.flip()
        clock.tick(speed)





# Quit confirmation function
def confirm_quit():
    screen = pygame.display.set_mode((400, 200))
    screen.fill((255, 255, 255))
    pygame.display.set_caption("Confirm Quit")
    font = pygame.font.Font(None, 36)
    text = font.render("Quit Game? (Y/N)", True, (0, 0, 0))
    screen.blit(text, (50, 80))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    return False




def flappy_bird():
    # Initialize Pygame
    pygame.init()

    # Screen dimensions
    SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (135, 206, 250)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    # Clock for controlling frame rate
    clock = pygame.time.Clock()
    FPS = 60

    # Bird properties
    bird_x, bird_y = 100, 300
    bird_width, bird_height = 30, 30
    bird_velocity = 0
    gravity = 0.2
    jump_strength = -10

    # Pipe properties
    pipe_width = 60
    pipe_gap = 150
    pipe_velocity = -4
    pipe_list = []

    # Initialize score
    score = 0


    def create_pipe():
        """Creates a new pipe with random height."""
        pipe_height = random.randint(100, SCREEN_HEIGHT - pipe_gap - 100)
        top_pipe = pygame.Rect(SCREEN_WIDTH, 0, pipe_width, pipe_height)
        bottom_pipe = pygame.Rect(
            SCREEN_WIDTH, pipe_height + pipe_gap, pipe_width, SCREEN_HEIGHT - pipe_height - pipe_gap
        )
        return top_pipe, bottom_pipe


    def check_collision(bird_rect, pipes):
        """Checks for collisions between the bird and pipes or boundaries."""
        for pipe in pipes:
            if bird_rect.colliderect(pipe):
                return True
        if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
            return True
        return False


    def get_score(bird_x, pipes):
        """Calculates the score based on passed pipes."""
        global score
        for pipe in pipes:
            if pipe.right < bird_x and not hasattr(pipe, "scored"):
                score += 1
                pipe.scored = True  # Mark the pipe as passed
        return score 


    # Create initial pipes
    pipe_list.extend(create_pipe())

    # Main game loop
    running = True
    while running:
        screen.fill(BLUE)  # Background color
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_velocity = jump_strength

        # Bird movement
        bird_velocity += gravity
        bird_y += bird_velocity
        bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)

        # Pipe movement
        for pipe in pipe_list:
            pipe.x += pipe_velocity

        # Remove pipes that are off-screen
        pipe_list = [pipe for pipe in pipe_list if pipe.right > 0]

        # Add new pipes
        if len(pipe_list) < 4 and pipe_list[-1].x < SCREEN_WIDTH // 2:
            pipe_list.extend(create_pipe())

        # Draw bird
        pygame.draw.rect(screen, RED, bird_rect)

        # Draw pipes
        for pipe in pipe_list:
            pygame.draw.rect(screen, GREEN, pipe)

        # Check collisions
        if check_collision(bird_rect, pipe_list):
            print("Game Over!")
            running = False

        # Update score
        score = get_score(bird_x, pipe_list)

        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Update the screen
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    return score
