import pygame

class Obstacle:
    """
    Represents obstacles/hazards in the game.
    Snake must avoid these
    """

    def __init__(self, x, y, size=20):
        self.x = x
        self.y = y
        self.size = size

    def draw(self, screen):
        """
        Draws the obstacle as a gray block.
        """
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(screen, (100, 100, 100), rect)  # gray block

    def get_rect(self):
        """
        Returns a pygame.Rect for collision detection.
        """
        return pygame.Rect(self.x, self.y, self.size, self.size)

