import unittest
import os
import sys

current_dir = os.path.dirname(__file__)
if current_dir not in sys.path:
    sys.path.append(current_dir)

from food import Food


class TestFood(unittest.TestCase):

    def test_initial_position_in_bounds_and_on_grid(self):
        """Food should start within the window and aligned to the grid."""
        f = Food(block_size=20, width=600, height=600, top_margin=40)
        self.assertGreaterEqual(f.x, 0)
        self.assertLess(f.x, 600)
        self.assertGreaterEqual(f.y, 40)     # respect HUD margin
        self.assertLess(f.y, 600)
        self.assertEqual(f.x % f.block_size, 0)
        self.assertEqual(f.y % f.block_size, 0)

    def test_respawn_stays_in_bounds_and_on_grid(self):
        """After respawn, food should still be in bounds and on the grid."""
        f = Food(block_size=20, width=600, height=600, top_margin=40)

        # call respawn a few times
        for _ in range(10):
            f.respawn()

            self.assertGreaterEqual(f.x, 0)
            self.assertLess(f.x, 600)
            self.assertGreaterEqual(f.y, 40)
            self.assertLess(f.y, 600)
            self.assertEqual(f.x % f.block_size, 0)
            self.assertEqual(f.y % f.block_size, 0)

    def test_is_special_is_boolean(self):
        """Food.is_special should always be a boolean."""
        f = Food(block_size=20, width=600, height=600, top_margin=40)

        for _ in range(10):
            f.respawn()
            self.assertIsInstance(f.is_special, bool)


if __name__ == "__main__":
    unittest.main()
