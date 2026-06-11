"""Module gérant la logique et l'état de l'entité principale du joueur."""

from direction import Direction

class Snake:
    """Represents the snake controlled by the player.
    
    Manages the internal state of the snake, notably its current length,
    its direction, and the coordinates of its entire body on the grid.
    """

    def __init__(self, x : int , y : int, length : int = 1,\
                  direction : Direction = Direction.RIGHT, block_size : int = 20) -> None:
        """Initializes a new snake at the start of the game.
        
        Args:
            x (int): The starting x coordinate (head of the snake).
            y (int): The starting y coordinate (head of the snake).
            length (int, optional): The initial length of the snake. Defaults to 1.
            direction (Direction, optional): The initial direction of the snake. Defaults to RIGHT.
            block_size (int, optional): The size of the blocks, in pixels. Defaults to 20.
        """
        self._length = length
        self._body: list[tuple[int, int]] = [(x, y)]
        self._direction = direction
        self._block_size = block_size

    @property
    def body(self) -> list[tuple[int, int]]:
        """Returns a copy of the snake's body coordinates."""
        return self._body[:]
    
    @property
    def direction(self) -> Direction:
        """Returns the current direction of the snake's head."""
        return self._direction
    
    @direction.setter
    def direction(self, dir : Direction) -> None:
        """Modifies the current direction of the snake's head."""
        forbidden_moves = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        if dir != forbidden_moves[self._direction]:
            self._direction = dir

    def move(self) -> None:
        """Handles the movement of the snake."""
        x_head, y_head = self._body[0]
        if self._direction == Direction.UP:
            self._body.insert(0, (x_head, y_head - self._block_size))
        elif self._direction == Direction.DOWN:
            self._body.insert(0, (x_head, y_head + self._block_size))
        elif self._direction == Direction.LEFT:
            self._body.insert(0, (x_head - self._block_size, y_head))
        elif self._direction == Direction.RIGHT:
            self._body.insert(0, (x_head + self._block_size, y_head))

        if len(self._body) != self._length:
            self._body.pop()

    def grow(self) -> None:
        """Increases the snake's length by 1."""
        self._length += 1

    def check_self_collision(self) -> bool:
        """Checks if the snake's head collides with its own body."""
        head = self._body[0]
        return head in self._body[1:]
    
    @property
    def score(self) -> int:
        """Returns the current score."""
        return self._length - 1