import pygame
import random

class Food:

    def __init__(self, block_size=20, width=600, height=600):
        self.block_size = block_size
        self.width = width
        self.height = height

        # Random position on grid
        self.x = random.randrange(0, width, block_size)
        self.y = random.randrange(0, height, block_size)

    def respawn(self):
        """
        Places food at a new random position.
        """
        ### TO DO: maybe check that food doesn't spawn on snake
        self.x = random.randrange(0, self.width, self.block_size)
        self.y = random.randrange(0, self.height, self.block_size)

    def draw(self, screen):
        """
        Draws the food on the screen.
        """
        ### TO DO: draw a simple rectangle for food
        pass
