import pygame
from snake import Snake
from food import Food
from obstacle import Obstacle
# from scoreboard import Scoreboard


class Game:
    """
    Main Game controller.
    Handles initialization, game loop, updates, and rendering.
    """

    def __init__(self, width=600, height=600):
        pygame.init()
        self.width = width
        self.height = height

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")

        # Clock for controlling FPS
        self.clock = pygame.time.Clock()

        # create objects
        self.snake = Snake()
        self.food = Food()

        # create some example obstacles (grid-aligned)
        self.obstacles = [
            Obstacle(200, 200),
            Obstacle(220, 200),
            Obstacle(240, 200),
        ]

        # self.scoreboard = Scoreboard()

        self.running = True

    def handle_events(self):
        """Handles keyboard and quit events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # basic movement controls for the snake
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_UP:
                    self.snake.change_direction((0, -20))
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction((0, 20))
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction((-20, 0))
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction((20, 0))

    def update(self):
        """Updates all game objects."""
        # move the snake
        self.snake.move()

        # end the game if the snake hits the wall
        if self.snake.is_out_of_bounds(self.width, self.height):
            print("Game Over: Snake hit the wall!")
            self.running = False

        # later: update food, obstacles, collisions, etc.

    def draw(self):
        """Draws everything to the screen."""
        # clear screen
        self.screen.fill((0, 0, 0))  # black background

        # draw snake, food, and obstacles
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        for obs in self.obstacles:
            obs.draw(self.screen)
        # later: draw scoreboard here

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(10)  # 10 FPS for now

        pygame.quit()
