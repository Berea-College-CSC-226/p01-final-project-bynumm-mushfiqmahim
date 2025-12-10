import pygame
import random

class Food:
    """
    Represents the food that the snake eats.
    Supports normal and special food.
    """

    def __init__(self, block_size=20, width=600, height=600, top_margin=40):
        self.block_size = block_size
        self.width = width
        self.height = height
        self.top_margin = top_margin  # keep food below HUD

        self.x = 0
        self.y = 0
        self.is_special = False  # normal by default

        self.respawn()

    def respawn(self):
        """
        Places food at a new random position on the grid.
        Ensures it does NOT spawn under the top HUD bar.
        Randomly decides if this food is special.
        """
        # valid x positions: 0, 20, 40, ..., width - block_size
        x_positions = list(range(0, self.width, self.block_size))

        # valid y positions: start at top_margin (e.g., 40), then 60, 80, ..., height - block_size
        min_y = max(self.top_margin, 0)
        max_y = self.height - self.block_size
        y_positions = list(range(min_y, max_y + 1, self.block_size))

        self.x = random.choice(x_positions)
        self.y = random.choice(y_positions)

        # 15% chance this food is special
        self.is_special = (random.random() < 0.15)

        kind = "SPECIAL" if self.is_special else "normal"
        print(f"{kind} food respawned at ({self.x}, {self.y})")

    def draw(self, screen):
        """
        Draws the food:
        - Normal: red circle
        - Special: blue-gold circle
        """
        center_x = self.x + self.block_size // 2
        center_y = self.y + self.block_size // 2
        radius = self.block_size // 2 - 2

        if self.is_special:
            # special food: blue/gold
            pygame.draw.circle(screen, (0, 120, 255), (center_x, center_y), radius)
            pygame.draw.circle(
                screen,
                (255, 215, 0),
                (center_x - radius // 2, center_y - radius // 2),
                3,
            )
        else:
            # normal food: red with small white highlight
            pygame.draw.circle(screen, (220, 40, 40), (center_x, center_y), radius)
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (center_x - radius // 2, center_y - radius // 2),
                2,
            )
