import pygame

class Obstacle:
    """
    Represents obstacles/hazards in the game.
    Snake must avoid these.
    """

    def __init__(self, x, y, size=20):
        self.x = x
        self.y = y
        self.size = size

    def draw(self, screen):
        """
        Draws the obstacle.
        """
        ### TO DO: draw a rectangle or image for obstacle
        pass

    def get_rect(self):
        """
        Returns a pygame.Rect for collision detection.
        """
        return pygame.Rect(self.x, self.y, self.size, self.size)
