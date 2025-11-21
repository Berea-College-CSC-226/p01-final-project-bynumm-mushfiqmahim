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

    ####To Do - create objects
        self.snake = Snake()
        self.food = Food()
        self.obstacles = []          # list of Obstacle objects
        # self.scoreboard = Scoreboard()

        self.running = True

    def handle_events(self):
        """Handles keyboard and quit events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            #####To Do - need to add movement controls later (MJ)
            # if event.type == pygame.KEYDOWN:
            #     pass

    def update(self):
        """Updates all game objects."""
        self.snake.move()
        ####To Do - update the snake, food, and obstacles
        pass

    def draw(self):
        """Draws everything to the screen."""
        self.screen.fill((0, 0, 0))  # for now, it's just black background

        ####To Do - draw snake, food, obstacles, scoreboard
        self.snake.draw(self.screen)
        # self.food.draw(self.screen)
        # for obs in self.obstacles:
        #     obs.draw(self.screen)
        # self.scoreboard.draw(self.screen)

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(10)  # 10 FPS for now

        pygame.quit()
