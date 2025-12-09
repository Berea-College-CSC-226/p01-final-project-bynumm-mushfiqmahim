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

        # fonts for text (score + game over + pause)
        self.font_large = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 32)

        # game state
        self.running = True       # main loop flag
        self.game_over = False    # are we in game over screen?
        self.paused = False       # is the game currently paused?

        # base speed (frames per second)
        self.base_speed = 10

        # score
        self.score = 0

        self._create_objects()

    def _create_objects(self):
        """Create or reset all game objects."""
        self.snake = Snake()
        self.food = Food(
            block_size=self.snake.block_size,
            width=self.width,
            height=self.height,
            top_margin=40,  # must match your HUD bar height
        )

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
                        self.paused = False
                        self._create_objects()
                    # don't process movement keys when game_over
                    continue

                # Toggle pause (only when not game over)
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                    return  # don’t handle movement on the same key press

                # If paused, ignore movement keys
                if self.paused:
                    continue

                # Normal movement controls (only when NOT game over or paused)
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
        # If game over or paused, do not update game logic
        if self.game_over or self.paused:
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

        # check snake–food collision
        head_x, head_y = self.snake.segments[0]
        if head_x == self.food.x and head_y == self.food.y:
            # snake eats food
            self.snake.grow()        # grow by one block
            self.food.respawn()      # move food to a new random spot
            self.score += 5          # +5 points per food
            print(f"Food eaten! Score is now {self.score}")

    def _draw_game_objects(self):
        """Draw snake, food, obstacles, and HUD during normal gameplay."""
        # draw snake, food, obstacles
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        for obs in self.obstacles:
            obs.draw(self.screen)

        # draw top HUD bar
        hud_height = 40
        hud_rect = pygame.Rect(0, 0, self.width, hud_height)
        pygame.draw.rect(self.screen, (25, 25, 35), hud_rect)

        # score text on top of the HUD
        score_text = self.font_small.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        # if paused, overlay a 'Paused' message
        if self.paused:
            paused_text = self.font_large.render("Paused", True, (255, 255, 0))
            instr_text = self.font_small.render("Press P to resume", True, (255, 255, 0))
            p_rect = paused_text.get_rect(center=(self.width // 2, self.height // 2 - 20))
            i_rect = instr_text.get_rect(center=(self.width // 2, self.height // 2 + 20))
            self.screen.blit(paused_text, p_rect)
            self.screen.blit(instr_text, i_rect)

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
        # dark background
        self.screen.fill((15, 15, 20))

        # draw grid lines every 20 pixels
        grid_color = (40, 40, 50)
        cell_size = 20

        for x in range(0, self.width, cell_size):
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, self.height))
        for y in range(0, self.height, cell_size):
            pygame.draw.line(self.screen, grid_color, (0, y), (self.width, y))

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

            # dynamic speed: faster as score increases (every 20 points +1 FPS)
            dynamic_fps = self.base_speed + (self.score // 20)
            self.clock.tick(dynamic_fps)

        pygame.quit()
