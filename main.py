import pygame
import sys
import pyautogui
from games import *

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

# Fonts and Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
font_title = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 30)

# Game Data
high_scores = [0] * 6  # High scores for all games
unlocked_games = [True] + [False] * 5  # Game 1 unlocked by default

def play_game(game_index):
    if game_index == 0:
        score = snake_game()  # Run snakegame and get score
        return score
    elif game_index == 1:
        score = flappy_bird()  # Placeholder for game2
        return score
    # elif game_index == 2:
    #     score = game3()  # Placeholder for game3
    #     return score
    else:
        print(f"Game {game_index + 1} is not implemented yet!")
        pygame.time.delay(2000)
        return 0  # Default score for unimplemented games

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mini Game Platform")
    running = True

    while running:
        screen.fill(WHITE)
        title = font_title.render("Mini Game Platform", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        # Game cards
        card_width, card_height = 300, 200
        margin = 50
        for i in range(6):
            x = (i % 3) * (card_width + margin) + (SCREEN_WIDTH - (card_width * 3 + margin * 2)) // 2
            y = (i // 3) * (card_height + margin) + 150
            color = GREEN if unlocked_games[i] else GRAY
            pygame.draw.rect(screen, color, (x, y, card_width, card_height), 0, 15)
            
            # Game info
            logo = font_small.render(f"Game {i + 1}", True, WHITE if unlocked_games[i] else BLACK)
            dev_name = font_small.render("By Developer", True, WHITE if unlocked_games[i] else BLACK)
            high_score_text = font_small.render(f"High Score: {high_scores[i]}", True, WHITE if unlocked_games[i] else BLACK)
            screen.blit(logo, (x + 20, y + 20))
            screen.blit(dev_name, (x + 20, y + 60))
            screen.blit(high_score_text, (x + 20, y + 100))

        # Total points at top right
        total_points = sum(high_scores)
        total_points_text = font_title.render(f"Points: {total_points}", True, BLACK)
        screen.blit(total_points_text, (SCREEN_WIDTH - total_points_text.get_width() - 20, 20))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i in range(6):
                    x = (i % 3) * (card_width + margin) + (SCREEN_WIDTH - (card_width * 3 + margin * 2)) // 2
                    y = (i // 3) * (card_height + margin) + 150
                    if x <= mouse_x <= x + card_width and y <= mouse_y <= y + card_height:
                        if unlocked_games[i]:
                            score = play_game(i)
                            high_scores[i] = max(high_scores[i], score)
                            if i == 0 and high_scores[i] >= 100 and not unlocked_games[1]:
                                unlocked_games[1] = True  # Unlock game 2

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()
