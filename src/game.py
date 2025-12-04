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

        # fonts for text (score + game over)
        self.font_large = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 32)

        # game state
        self.running = True       # main loop flag
        self.game_over = False    # are we in game over screen?

        # score (will be increased later when food is eaten)
        self.score = 0

        self._create_objects()

    def _create_objects(self):
        """Create or reset all game objects."""
        self.snake = Snake()
        self.food = Food()
        self.obstacles = [
            Obstacle(200, 200),
            Obstacle(220, 200),
            Obstacle(240, 200),
        ]
        # self.scoreboard = Scoreboard()

    def handle_events(self):
        """Handles keyboard and quit events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                # ESC always quits
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                # If game is over: allow restart
                if self.game_over:
                    if event.key == pygame.K_r:
                        # restart game
                        self.game_over = False
                        self.score = 0
                        self._create_objects()
                    # don't process movement keys when game_over
                    continue

                # Normal movement controls (only when NOT game over)
                if event.key == pygame.K_UP:
                    self.snake.change_direction((0, -20))
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction((0, 20))
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction((-20, 0))
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction((20, 0))

    def update(self):
        """Updates all game objects."""
        # If game over, do not update game logic
        if self.game_over:
            return

        # move the snake
        self.snake.move()

        # end the game if the snake hits the wall
        if self.snake.is_out_of_bounds(self.width, self.height):
            print("Game Over: Snake hit the wall!")
            self.game_over = True
            return

        # end the game if the snake hits an obstacle
        head_rect = self.snake.get_head_rect()
        for obs in self.obstacles:
            if head_rect.colliderect(obs.get_rect()):
                print("Game Over: Snake hit an obstacle!")
                self.game_over = True
                return

        # later: check snake-food collisions, scoring, etc.

    def _draw_game_objects(self):
        """Draw snake, food, obstacles during normal gameplay."""
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        for obs in self.obstacles:
            obs.draw(self.screen)
        # later: draw scoreboard here

    def _draw_game_over_screen(self):
        """Draw the Game Over screen with final score and instructions."""
        game_over_text = self.font_large.render("Game Over", True, (255, 255, 255))
        score_text = self.font_small.render(f"Final Score: {self.score}", True, (255, 255, 255))
        instr_text = self.font_small.render("Press R to restart or ESC to quit", True, (255, 255, 255))

        # center the texts
        go_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 40))
        score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2))
        instr_rect = instr_text.get_rect(center=(self.width // 2, self.height // 2 + 40))

        self.screen.blit(game_over_text, go_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(instr_text, instr_rect)

    def draw(self):
        """Draws everything to the screen."""
        # clear screen
        self.screen.fill((0, 0, 0))  # black background

        if not self.game_over:
            # normal game rendering
            self._draw_game_objects()
        else:
            # show game over screen
            self._draw_game_over_screen()

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(10)  # 10 FPS for now

        pygame.quit()
