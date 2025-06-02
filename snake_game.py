import pygame
import random
import json
import os

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
GRAY = (128, 128, 128)
HOVER_COLOR = (200, 200, 200)

# Snake and food properties
snake_block = 20
snake_speed = 15

# Initialize clock
clock = pygame.time.Clock()

# Game states
STATE_MENU = 'menu'
STATE_GAME = 'game'
STATE_PAUSE = 'pause'
STATE_SETTINGS = 'settings'

class MenuItem:
    def __init__(self, text, y_pos):
        self.text = text
        self.y_pos = y_pos
        self.font = pygame.font.SysFont(None, 50)
        self.is_hovered = False
        self.rect = None

    def draw(self, surface):
        color = HOVER_COLOR if self.is_hovered else WHITE
        text_surface = self.font.render(self.text, True, color)
        self.rect = text_surface.get_rect(center=(window_width/2, self.y_pos))
        surface.blit(text_surface, self.rect)

    def check_hover(self, mouse_pos):
        if self.rect:
            self.is_hovered = self.rect.collidepoint(mouse_pos)
            return self.is_hovered
        return False

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
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
        if (self.x >= window_width or self.x < 0 or
            self.y >= window_height or self.y < 0):
            return True

        for block in self.body[:-1]:
            if block == (self.x, self.y):
                return True
        return False

    def save_state(self):
        return {
            'x': self.x,
            'y': self.y,
            'direction': self.direction,
            'body': self.body,
            'length': self.length
        }

    def load_state(self, state):
        self.x = state['x']
        self.y = state['y']
        self.direction = state['direction']
        self.body = state['body']
        self.length = state['length']

class Game:
    def __init__(self):
        self.state = STATE_MENU
        self.snake = Snake()
        self.food_x, self.food_y = self.generate_food()
        self.score = 0
        self.snake_speed = snake_speed
        self.menu_items = []
        self.init_menu_items()
        self.load_settings()

    def init_menu_items(self):
        self.menu_items = [
            MenuItem('New Game', 250),
            MenuItem('Resume Game', 320) if os.path.exists('saved_game.json') else None,
            MenuItem('Settings', 390),
            MenuItem('Quit', 460)
        ]
        self.menu_items = [item for item in self.menu_items if item is not None]

    def load_settings(self):
        if os.path.exists('settings.json'):
            try:
                with open('settings.json', 'r') as f:
                    settings = json.load(f)
                    self.snake_speed = settings.get('snake_speed', snake_speed)
            except:
                pass

    def save_settings(self):
        settings = {'snake_speed': self.snake_speed}
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

    def save_game(self):
        game_state = {
            'snake': self.snake.save_state(),
            'food': (self.food_x, self.food_y),
            'score': self.score
        }
        with open('saved_game.json', 'w') as f:
            json.dump(game_state, f)

    def load_game(self):
        if os.path.exists('saved_game.json'):
            try:
                with open('saved_game.json', 'r') as f:
                    game_state = json.load(f)
                    self.snake.load_state(game_state['snake'])
                    self.food_x, self.food_y = game_state['food']
                    self.score = game_state['score']
                    return True
            except:
                pass
        return False

    def generate_food(self):
        food_x = round(random.randrange(0, window_width - snake_block) / snake_block) * snake_block
        food_y = round(random.randrange(0, window_height - snake_block) / snake_block) * snake_block
        return food_x, food_y

    def draw_menu(self):
        window.fill(BLACK)
        font = pygame.font.SysFont(None, 74)
        title = font.render('Snake Game', True, WHITE)
        window.blit(title, [window_width/2 - title.get_width()/2, 100])

        mouse_pos = pygame.mouse.get_pos()
        for item in self.menu_items:
            item.check_hover(mouse_pos)
            item.draw(window)

    def draw_settings(self):
        window.fill(BLACK)
        font = pygame.font.SysFont(None, 74)
        title = font.render('Settings', True, WHITE)
        window.blit(title, [window_width/2 - title.get_width()/2, 100])

        font = pygame.font.SysFont(None, 50)
        speed_text = font.render(f'Snake Speed: {self.snake_speed}', True, WHITE)
        window.blit(speed_text, [window_width/2 - speed_text.get_width()/2, 250])

        controls_text = font.render('← → to adjust speed', True, WHITE)
        window.blit(controls_text, [window_width/2 - controls_text.get_width()/2, 300])

        back_text = font.render('Press ESC to return', True, WHITE)
        window.blit(back_text, [window_width/2 - back_text.get_width()/2, 400])

    def run(self):
        running = True
        while running:
            if self.state == STATE_MENU:
                self.handle_menu()
            elif self.state == STATE_GAME:
                self.handle_game()
            elif self.state == STATE_PAUSE:
                self.handle_pause()
            elif self.state == STATE_SETTINGS:
                self.handle_settings()

            pygame.display.update()
            clock.tick(self.snake_speed)

    def handle_menu(self):
        self.draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                for item in self.menu_items:
                    if item.is_hovered:
                        if item.text == 'New Game':
                            self.snake.reset()
                            self.score = 0
                            self.food_x, self.food_y = self.generate_food()
                            self.state = STATE_GAME
                        elif item.text == 'Resume Game':
                            if self.load_game():
                                self.state = STATE_GAME
                        elif item.text == 'Settings':
                            self.state = STATE_SETTINGS
                        elif item.text == 'Quit':
                            pygame.quit()
                            return

    def handle_pause(self):
        font = pygame.font.SysFont(None, 74)
        pause_text = font.render('PAUSED', True, WHITE)
        window.blit(pause_text, [window_width/2 - pause_text.get_width()/2, window_height/2 - 37])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = STATE_GAME
                elif event.key == pygame.K_s:
                    self.save_game()
                    self.state = STATE_MENU
                    self.init_menu_items()

    def handle_settings(self):
        self.draw_settings()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.save_settings()
                    self.state = STATE_MENU
                elif event.key == pygame.K_LEFT and self.snake_speed > 5:
                    self.snake_speed -= 1
                elif event.key == pygame.K_RIGHT and self.snake_speed < 30:
                    self.snake_speed += 1

    def handle_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = STATE_PAUSE
                elif event.key == pygame.K_LEFT and self.snake.direction != 'RIGHT':
                    self.snake.direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and self.snake.direction != 'LEFT':
                    self.snake.direction = 'RIGHT'
                elif event.key == pygame.K_UP and self.snake.direction != 'DOWN':
                    self.snake.direction = 'UP'
                elif event.key == pygame.K_DOWN and self.snake.direction != 'UP':
                    self.snake.direction = 'DOWN'

        self.snake.move()

        if self.snake.x == self.food_x and self.snake.y == self.food_y:
            self.food_x, self.food_y = self.generate_food()
            self.snake.length += 1
            self.score += 1

        if self.snake.check_collision():
            self.state = STATE_MENU
            self.init_menu_items()

        window.fill(BLACK)
        pygame.draw.rect(window, RED, [self.food_x, self.food_y, snake_block, snake_block])
        
        for pos in self.snake.body:
            pygame.draw.rect(window, GREEN, [pos[0], pos[1], snake_block, snake_block])

        font = pygame.font.SysFont(None, 50)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        window.blit(score_text, [10, 10])

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()