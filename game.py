"""Module managing the game's main loop."""

import pygame
import sys
from snake import Snake
from apple import Apple
from direction import Direction

BLACK = (0, 0, 0)           # background
GREEN = (0, 255, 0)         # snake
RED = (255, 0, 0)           # apple
WHITE = (255, 255, 255)     # text

FPS = 15
BLOCK_SIZE = 20

class Game:
    """Represents the main loop of the game."""
    
    def __init__(self, width: int, height: int) -> None:
        """Initializes Pygame, the window, and game objects."""
        pygame.init()
        self._width, self._height = width, height
        self._block_size = BLOCK_SIZE
        self._fps = FPS
        self._screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Snake Project")
        self._clock = pygame.time.Clock()
        self._apple = Apple(0, 0)
        self.reset()
        self._font_title = pygame.font.SysFont(None, 50)
        self._font_score = pygame.font.SysFont(None, 25)
        self._high_score = 0
        self._game_started = False

    def handle_events(self) -> None:
        """Processes keyboard inputs and system events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not self._game_started:
                    if event.key == pygame.K_SPACE:
                        self._game_started = True
                if self._game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset()
                else:
                    if event.key == pygame.K_LEFT:
                        self._snake.direction = Direction.LEFT
                    elif event.key == pygame.K_RIGHT:
                        self._snake.direction = Direction.RIGHT
                    elif event.key == pygame.K_UP:
                        self._snake.direction = Direction.UP
                    elif event.key == pygame.K_DOWN:
                        self._snake.direction = Direction.DOWN

    def update(self) -> None:
        """Updates the state of the game (movements and collisions)."""
        self._snake.move()
        head_x, head_y = self._snake.body[0]
        if head_x == self._apple.x and head_y == self._apple.y:
            self._snake.grow()
            self._apple.spawn(self._width, self._height, self._block_size, self._snake.body)
        if head_x < 0 or head_x >= self._width or head_y < 0 or head_y >= self._height:
            self._game_over = True
        if self._snake.check_self_collision():
            self._game_over = True
        if self._game_over and self._snake.score > self._high_score:
            self._high_score = self._snake.score
        
    def draw(self) -> None:
        """Renders all game objects on the screen."""
        self._screen.fill(BLACK)
        current_score = self._snake.score
        text_score = self._font_score.render("Score : " + str(current_score), True, WHITE)
        self._screen.blit(text_score, (10, 10))
        high_score = self._high_score
        text_score = self._font_score.render("High Score : " + str(high_score), True, WHITE)
        self._screen.blit(text_score, (10, 35))
        pygame.draw.rect(self._screen, RED, [self._apple.x, self._apple.y, self._block_size, self._block_size])
        for block in self._snake.body:
            pygame.draw.rect(self._screen, GREEN, [block[0], block[1], self._block_size, self._block_size])
        pygame.display.update()

    def run(self) -> None:
        """Starts and maintains the game loop."""
        while True:
            self.handle_events()
            if not self._game_started:
                self.show_start_screen()
            elif not self._game_over:
                self.update()
                self.draw()
            else:
                self.show_game_over_screen()
            self._clock.tick(self._fps)

    def show_start_screen(self) -> None:
        """Displays the start menu screen."""
        self._screen.fill(BLACK)
        text_surface = self._font_title.render("SNAKE GAME", True, GREEN)
        self._screen.blit(text_surface, (190, 150))
        text_start = self._font_score.render("Press SPACE to start", True, WHITE)
        self._screen.blit(text_start, (215, 210))
        pygame.display.update()

    def show_game_over_screen(self) -> None:
        """Display the Game over screen."""
        text_surface = self._font_title.render("GAME OVER", True, WHITE)
        self._screen.blit(text_surface, (200, 150))
        text_restart = self._font_score.render("Press SPACE to play again", True, WHITE)
        self._screen.blit(text_restart, (195, 210))
        pygame.display.update()

    def reset(self) -> None:
        """Resets the game state for a new playthrough."""
        self._snake = Snake(x=self._width // 2, y=self._height // 2, block_size=self._block_size)
        self._apple.spawn(self._width, self._height, self._block_size, self._snake.body)
        self._game_over = False

if __name__ == "__main__":
    game = Game(600, 400)
    game.run()