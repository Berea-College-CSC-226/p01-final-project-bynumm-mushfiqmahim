import pygame

class Snake:
    """
    Represents the player's snake.
    Handles position, movement, growing, and collisions.
    """

    def __init__(self, initial_length=3, block_size=20):
        self.block_size = block_size

        # Start with a simple list of segments (x, y)
        self.segments = [(100, 100), (80, 100), (60, 100)]

        # Movement direction (dx, dy)
        self.direction = (20, 0)  # moving right initially

    def change_direction(self, new_direction):
        """
        Changes direction of the snake.
        new_direction is a tuple (dx, dy)
        """
        ###TO Do - need to add logic to prevent reversing directly
        self.direction = new_direction

    def move(self):
        """
        Moves the snake by adding a new head and removing tail.
        """
        # TODO: implement movement logic
        pass

    def grow(self):
        """
        Makes the snake longer by not removing the tail segment during movement.
        """
        # TODO: implement growth logic
        pass

    def draw(self, screen):
        """
        Draws the snake on the screen.
        """
        # TODO: draw each segment as a rectangle
        pass
