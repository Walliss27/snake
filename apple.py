"""
Module managing the game's collectible item.

Handles the logic, positioning, and spawning mechanics of the apple 
within the game grid.
"""

import random

class Apple:
    """
    Represents the apple object on the grid.

    The apple is the target that the snake must consume to grow and increase 
    the score. It respawns at random valid coordinates upon consumption.
    """

    def __init__(self, x: int , y: int) -> None:
        """Initializes a new apple.

        Args:
            x (int): The x coordinate on the grid.
            y (int): The y coordinate on the grid.
        """
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        """Returns the x coordinate of the apple."""
        return self._x

    @property
    def y(self) -> int:
        """Returns the y coordinate of the apple."""
        return self._y

    def spawn(self, width: int, height: int, block_size: int,\
               snake_body: list[tuple[int, int]]) -> None:
        """Handles the apple spawning at a new random location.
        
        Args:
            width (int): The width of the window.
            height (int): The height of the window.
            block_size (int): The size of a grid block in pixels.
            snake_body (list[tuple[int, int]]): The list of coordinates of the snake's body.
        """
        self._x, self._y = snake_body[0]
        while (self._x, self._y) in snake_body:
            self._x = random.randrange(0, width, block_size)
            self._y = random.randrange(0, height, block_size)
