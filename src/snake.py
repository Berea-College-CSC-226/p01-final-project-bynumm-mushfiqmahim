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

        # How many growth steps are pending
        self.grow_pending = 0

    def change_direction(self, new_direction):
        """
        Changes direction of the snake.
        new_direction is a tuple (dx, dy).

        Prevents reversing directly (e.g., right -> left).
        """
        current_dx, current_dy = self.direction
        new_dx, new_dy = new_direction

        # If new direction is exactly opposite, ignore it
        if (new_dx == -current_dx) and (new_dy == -current_dy):
            return  # do not allow 180-degree turn

        self.direction = new_direction

    def move(self):
        """
        Moves the snake by adding a new head and removing the last tail segment.
        Uses the current direction tuple (dx, dy).
        If grow_pending > 0, the tail is NOT removed, so the snake grows.
        """
        # Current head position
        head_x, head_y = self.segments[0]

        # Direction movement
        dx, dy = self.direction

        # New head (move one block)
        new_head = (head_x + dx, head_y + dy)

        # Add new head to the front of the list
        self.segments.insert(0, new_head)

        # If we still need to grow, keep the tail (no pop)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            # Remove the last segment (tail) to keep same length
            self.segments.pop()

    def grow(self):
        """
        Makes the snake longer by one block on the next move.
        """
        self.grow_pending += 1

    def draw(self, screen):
        """
        Draws the snake on the screen:
        - Head with a brighter color and eyes
        - Body with a slightly darker green
        """
        if not self.segments:
            return

        # draw head
        head_x, head_y = self.segments[0]
        head_rect = pygame.Rect(head_x, head_y, self.block_size, self.block_size)
        pygame.draw.rect(screen, (0, 220, 0), head_rect)  # brighter head

        # draw eyes on the head
        eye_radius = 3
        offset = 4
        # two little eye circles
        pygame.draw.circle(
            screen,
            (0, 0, 0),
            (head_x + self.block_size - offset, head_y + offset),
            eye_radius,
        )
        pygame.draw.circle(
            screen,
            (0, 0, 0),
            (head_x + self.block_size - offset, head_y + self.block_size - offset),
            eye_radius,
        )

        # draw body
        for (x, y) in self.segments[1:]:
            rect = pygame.Rect(x, y, self.block_size, self.block_size)
            pygame.draw.rect(screen, (0, 180, 0), rect)

    def check_self_collision(self):
        """Check if the snake ran into itself"""
        # TO DO: implement self-collision logic later
        pass

    def is_out_of_bounds(self, width, height):
        """Return True if snake head goes outside the game window."""
        head_x, head_y = self.segments[0]

        # check left, right, top, bottom boundaries
        if head_x < 0 or head_x >= width:
            return True
        if head_y < 0 or head_y >= height:
            return True

        return False

    def get_head_rect(self):
        """Return a pygame.Rect for the snake's head (for collision checks)."""
        head_x, head_y = self.segments[0]
        return pygame.Rect(head_x, head_y, self.block_size, self.block_size)
