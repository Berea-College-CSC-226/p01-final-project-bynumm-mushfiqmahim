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
           Moves the snake by adding a new head and removing the last tail segment.
           Uses the current direction tuple (dx, dy).
           Ensures movement stays aligned to the block grid.
           """

        # Current head position
        head_x, head_y = self.segments[0]

        # Direction movement
        dx, dy = self.direction

        # New head (move one block)
        new_head = (head_x + dx, head_y + dy)

        # Add new head to the front of the list
        self.segments.insert(0, new_head)

        # Remove the last segment (tail) to keep same length
        self.segments.pop()
        pass

    def grow(self):
        """
        Makes the snake longer by not removing the tail segment during movement.
        """
        ### TO DO: implement growth logic
        pass

    def draw(self, screen):
        """
        Draws the snake on the screen as green blocks.
        """
        for (x, y) in self.segments:
            rect = pygame.Rect(x, y, self.block_size, self.block_size)
            pygame.draw.rect(screen, (0, 255, 0), rect)
        pass

    def check_self_collision(self):
        """Check if the snake ran into itself."""
        pass

