"""Module managing the game's main loop."""

import pygame
import sys
from snake import Snake
from apple import Apple
from direction import Direction

BLACK = (0, 0, 0)           # background
GREEN = (0, 255, 0)         # snake
RED = (255, 0, 0)           # apple

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
        self._snake = Snake(x=width // 2, y=height // 2, block_size=self._block_size)
        self._apple = Apple(0, 0)
        self._apple.spawn(width, height, self._block_size, self._snake.body)

    def handle_events(self) -> None:
        """Processes keyboard inputs and system events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self) -> None:
        """Updates the state of the game (movements and collisions)."""
        
    def draw(self) -> None:
        """Renders all game objects on the screen."""

    def run(self) -> None:
        """Starts and maintains the game loop."""
        while True:
            self.handle_events()

if __name__ == "__main__":
    game = Game(600, 400)
    game.run()