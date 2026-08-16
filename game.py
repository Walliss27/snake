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

FPS = 25
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
        self._ai_mode = False

    def handle_events(self) -> None:
        """Processes keyboard inputs and system events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not self._game_started:
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        self._ai_mode = False
                        self._game_started = True
                    elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        self._ai_mode = True
                        self._game_started = True
                elif self._game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset()
                elif not self._ai_mode:
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
                if self._ai_mode:
                    self._run_ai()
                self.update()
                self.draw()
            else:
                self.show_game_over_screen()
            self._clock.tick(self._fps)

    def _run_ai(self):
        start = self._snake.body[0]
        target = self._apple.x, self._apple.y
        came_from = self._snake._bfs(start, target, self._width, self._height)
        path = self._snake._get_path(came_from, start, target)
        if path:
            next_node = path[0]
        else:
            target = self._snake.body[-1]
            came_from = self._snake._bfs(start, target, self._width, self._height)
            path = self._snake._get_path(came_from, start, target)
            if path:
                next_node = path[0]
            else:
                next_node = {Direction.UP: (start[0], start[1] - self._block_size),\
                              Direction.DOWN: (start[0], start[1] + self._block_size),\
                                  Direction.LEFT: (start[0] - self._block_size, start[1]),\
                                      Direction.RIGHT: (start[0] + self._block_size, start[1])}\
                                        [self._snake.direction]
        if next_node[0] < start[0]:
            self._snake.direction = Direction.LEFT
        elif next_node[0] > start[0]:
            self._snake.direction = Direction.RIGHT
        elif next_node[1] < start[1]:
            self._snake.direction = Direction.UP
        elif next_node[1] > start[1]:
            self._snake.direction = Direction.DOWN

    def show_start_screen(self) -> None:
        """Displays the start menu screen."""
        self._screen.fill(BLACK)
        text_surface = self._font_title.render("SNAKE GAME", True, GREEN)
        self._screen.blit(text_surface, (190, 150))
        text_player = self._font_score.render("1. Human player", True, WHITE)
        self._screen.blit(text_player, (215, 210))
        text_ai = self._font_score.render("2. AI player", True, WHITE)
        self._screen.blit(text_ai, (215, 240))
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