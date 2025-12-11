import os
import sys
import unittest

sys.path.append(os.path.dirname(__file__))

from snake import Snake


class TestSnake(unittest.TestCase):
    def test_initial_length_is_three(self):
        """Snake should start with 3 segments."""
        snake = Snake()
        self.assertEqual(len(snake.segments), 3)

    def test_move_changes_head_position(self):
        """After one move, the head position should change."""
        snake = Snake()
        head_before = snake.segments[0]
        snake.move()
        head_after = snake.segments[0]
        self.assertNotEqual(head_before, head_after)

    def test_grow_increases_length_by_one(self):
        """Calling grow() then move() should increase length by 1."""
        snake = Snake()
        original_length = len(snake.segments)
        snake.grow()
        snake.move()
        self.assertEqual(len(snake.segments), original_length + 1)


if __name__ == "__main__":
    unittest.main()
