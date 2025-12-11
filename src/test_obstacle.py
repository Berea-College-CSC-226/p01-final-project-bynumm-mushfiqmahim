import unittest
import os
import sys
import pygame

current_dir = os.path.dirname(__file__)
if current_dir not in sys.path:
    sys.path.append(current_dir)

from obstacle import Obstacle


class TestObstacle(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_get_rect_matches_position_and_size(self):
        """get_rect should return a rect with the same x, y and size."""
        obs = Obstacle(100, 160, size=20)
        rect = obs.get_rect()

        self.assertEqual(rect.x, 100)
        self.assertEqual(rect.y, 160)
        self.assertEqual(rect.width, 20)
        self.assertEqual(rect.height, 20)

    def test_rect_collision_behaves_as_expected(self):
        """Obstacle rect should collide with another rect at the same place."""
        obs = Obstacle(200, 220, size=20)
        rect = obs.get_rect()

        other = pygame.Rect(200, 220, 20, 20)
        self.assertTrue(rect.colliderect(other))
        far = pygame.Rect(400, 400, 20, 20)
        self.assertFalse(rect.colliderect(far))


if __name__ == "__main__":
    unittest.main()
