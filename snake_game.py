import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Snake Game')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Snake and food properties
snake_block = 20
snake_speed = 15

# Initialize clock
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.x = window_width // 2
        self.y = window_height // 2
        self.direction = 'RIGHT'
        self.body = [(self.x, self.y)]
        self.length = 1

    def move(self):
        if self.direction == 'RIGHT':
            self.x += snake_block
        elif self.direction == 'LEFT':
            self.x -= snake_block
        elif self.direction == 'UP':
            self.y -= snake_block
        elif self.direction == 'DOWN':
            self.y += snake_block

        self.body.append((self.x, self.y))
        if len(self.body) > self.length:
            del self.body[0]

    def check_collision(self):
        # Check wall collision
        if (self.x >= window_width or self.x < 0 or
            self.y >= window_height or self.y < 0):
            return True

        # Check self collision
        for block in self.body[:-1]:
            if block == (self.x, self.y):
                return True
        return False

def generate_food():
    food_x = round(random.randrange(0, window_width - snake_block) / snake_block) * snake_block
    food_y = round(random.randrange(0, window_height - snake_block) / snake_block) * snake_block
    return food_x, food_y

def main():
    game_over = False
    snake = Snake()
    food_x, food_y = generate_food()
    score = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake.direction != 'RIGHT':
                    snake.direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and snake.direction != 'LEFT':
                    snake.direction = 'RIGHT'
                elif event.key == pygame.K_UP and snake.direction != 'DOWN':
                    snake.direction = 'UP'
                elif event.key == pygame.K_DOWN and snake.direction != 'UP':
                    snake.direction = 'DOWN'

        snake.move()

        # Check if snake ate food
        if snake.x == food_x and snake.y == food_y:
            food_x, food_y = generate_food()
            snake.length += 1
            score += 1

        # Check collision
        if snake.check_collision():
            game_over = True

        # Draw everything
        window.fill(BLACK)
        
        # Draw food
        pygame.draw.rect(window, RED, [food_x, food_y, snake_block, snake_block])
        
        # Draw snake
        for pos in snake.body:
            pygame.draw.rect(window, GREEN, [pos[0], pos[1], snake_block, snake_block])

        # Display score
        font = pygame.font.SysFont(None, 50)
        score_text = font.render(f'Score: {score}', True, WHITE)
        window.blit(score_text, [10, 10])

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()

if __name__ == '__main__':
    main()