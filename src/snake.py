import pygame

class Snake:
    """
    Represents the player's snake.
    Handles position, movement growing and collisions.
    """

    def __init__(self, initial_length=3, block_size=20):
        self.block_size = block_size
        start_x = 200
        start_y = 200
        self.segments = [
            (start_x, start_y),
            (start_x - block_size, start_y),
            (start_x - 2 * block_size, start_y),
        ]

        # Movement direction (dx, dy)
        self.direction = (block_size, 0)
        self.next_direction = self.direction
        self.grow_pending = 0

    def change_direction(self, new_direction):
        """
        Change direction for the next move and prevents reversing directly """
        new_dx, new_dy = new_direction
        curr_dx, curr_dy = self.direction
        next_dx, next_dy = self.next_direction
        if (new_dx == -curr_dx and new_dy == -curr_dy) or \
           (new_dx == -next_dx and new_dy == -next_dy):
            return  # do not allow 180-degree turn
        self.next_direction = new_direction

    def move(self):
        """
        Moves the snake by adding a new head and removing the last tail segment.
        the tail is NOT removed, so the snake grows.
        """
        self.direction = self.next_direction
        head_x, head_y = self.segments[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.segments.insert(0, new_head)

        # If it still needs to grow, keep the tail
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.segments.pop() # Remove tail to keep same length

    def grow(self):
        """
        Makes the snake longer by one block on the next move.
        """
        self.grow_pending += 1

    def draw(self, screen, head_color=(0, 220, 0), body_color=(0, 180, 0)):
        """
        Draws the snake on the screen
        """
        if not self.segments:
            return
        head_x, head_y = self.segments[0]
        head_rect = pygame.Rect(head_x, head_y, self.block_size, self.block_size)
        pygame.draw.rect(screen, head_color, head_rect)

        # draw eyes on the head based on direction
        eye_radius = 3
        padding = 3
        dx, dy = self.direction

        if dx > 0:  # moving RIGHT
            eye1 = (head_x + self.block_size - padding,
                    head_y + padding)
            eye2 = (head_x + self.block_size - padding,
                    head_y + self.block_size - padding)
        elif dx < 0:  # moving LEFT
            eye1 = (head_x + padding,
                    head_y + padding)
            eye2 = (head_x + padding,
                    head_y + self.block_size - padding)
        elif dy < 0:  # moving UP
            eye1 = (head_x + padding,
                    head_y + padding)
            eye2 = (head_x + self.block_size - padding,
                    head_y + padding)
        else:  # moving DOWN
            eye1 = (head_x + padding,
                    head_y + self.block_size - padding)
            eye2 = (head_x + self.block_size - padding,
                    head_y + self.block_size - padding)

        pygame.draw.circle(screen, (0, 0, 0), eye1, eye_radius)
        pygame.draw.circle(screen, (0, 0, 0), eye2, eye_radius)

        # draw body
        for (x, y) in self.segments[1:]:
            rect = pygame.Rect(x, y, self.block_size, self.block_size)
            pygame.draw.rect(screen, body_color, rect)

    def check_self_collision(self):
        """Return True if the snake's head runs into its own body"""
        if len(self.segments) <= 3:
            return False

        head = self.segments[0]
        body = self.segments[1:]
        return head in body

    def is_out_of_bounds(self, width, height, top_margin=40):
        """
        Return True if snake head goes outside the playable area.
        Playable:
        - x from 0 to width - block_size
        - y from top_margin to height - block_size
        """
        head_x, head_y = self.segments[0]

        # left/right
        if head_x < 0 or head_x >= width:
            return True

        # top: respect HUD margin
        if head_y < top_margin or head_y >= height:
            return True

        return False

    def get_head_rect(self):
        """for collision checks."""
        head_x, head_y = self.segments[0]
        return pygame.Rect(head_x, head_y, self.block_size, self.block_size)

    def teleport_to(self, new_x, new_y):
        """
        Move the entire snake so that the head appears at (new_x, new_y)
        """
        head_x, head_y = self.segments[0]
        dx = new_x - head_x
        dy = new_y - head_y

        self.segments = [(x + dx, y + dy) for (x, y) in self.segments]
