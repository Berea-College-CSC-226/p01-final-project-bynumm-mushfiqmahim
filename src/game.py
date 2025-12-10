import pygame
import random
from snake import Snake
from food import Food
from obstacle import Obstacle

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


        self.clock = pygame.time.Clock() #Clock for FPS control
        self.font_large = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 32)

        # Game state
        self.running = True
        self.game_over = False
        self.paused = False

        # Base speed, score and level
        self.base_speed = 10
        self.score = 0
        self.level = 1

        self._create_objects()

    def _create_objects(self):
        """Create or reset all game objects."""
        self.snake = Snake()

        # Food should respect HUD
        self.food = Food(
            block_size=self.snake.block_size,
            width=self.width,
            height=self.height,
            top_margin=40,
        )

        # Game start with a few obstacles, but they don't overlap
        self.obstacles = []
        for _ in range(3):
            self._add_random_obstacle()

    def _get_snake_colors_for_level(self):
        """
        Return (head_color, body_color) based on current level.
        """
        palette = [
            # level 1
            ((0, 220, 0), (0, 180, 0)),        # green
            # level 2
            ((0, 210, 255), (0, 150, 220)),    # cyan/blue
            # level 3
            ((255, 210, 0), (220, 170, 0)),    # yellow/orange
            # level 4
            ((255, 120, 0), (220, 90, 0)),     # deeper orange
            # level 5+
            ((220, 0, 120), (180, 0, 90)),     # magenta/purple
        ]
        idx = min(self.level - 1, len(palette) - 1)
        return palette[idx]

    def _update_level(self):
        """Update level based on score, and trigger level-up effects."""
        new_level = self.score // 20 + 1  # every 20 points = new level: 1,2,3,...

        if new_level > self.level:
            self.level = new_level
            self._on_level_up()

    def _on_level_up(self):
        """Effects when a new level is reached."""
        print(f"LEVEL UP! Now level {self.level}")
        # Add a new random obstacle each level
        self._add_random_obstacle()

    def _add_random_obstacle(self):
        """Add a new obstacle at a random safe grid position."""
        block_size = self.snake.block_size
        top_margin = 40  # avoid HUD area
        x_positions = list(range(0, self.width, block_size))
        y_positions = list(range(top_margin, self.height, block_size))

        # NOT allowed position (snake, food, existing obstacles)
        forbidden = set(self.snake.segments)
        forbidden.add((self.food.x, self.food.y))
        for obs in self.obstacles:
            if hasattr(obs, "x") and hasattr(obs, "y"):
                forbidden.add((obs.x, obs.y))

        # find a free spot
        for _ in range(100):
            x = random.choice(x_positions)
            y = random.choice(y_positions)
            if (x, y) not in forbidden:
                self.obstacles.append(Obstacle(x, y))
                print(f"New obstacle added at ({x}, {y})")
                return

        print("Could not find a free spot for new obstacle.")

    def _respawn_food_safely(self):
        """
        Respawn food, but avoid placing it on the snake or on any obstacle.
        """
        forbidden = set(self.snake.segments)
        for obs in self.obstacles:
            if hasattr(obs, "x") and hasattr(obs, "y"):
                forbidden.add((obs.x, obs.y))

        for _ in range(100):
            self.food.respawn()
            if (self.food.x, self.food.y) not in forbidden:
                return

        print("Warning: could not find free spot for food after 100 tries.")

    def handle_events(self):
        """Handles keyboard and quit events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                # ESC quits
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                # Allow restart
                if self.game_over:
                    if event.key == pygame.K_r:
                        # Restart game
                        self.game_over = False
                        self.score = 0
                        self.level = 1
                        self.paused = False
                        self._create_objects()
                    continue

                # Pause during game
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                    return

                # Ignore movement keys
                if self.paused:
                    continue

                # Movement controls
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
        # no update when game over or pause
        if self.game_over or self.paused:
            return


        self.snake.move()

        # End the game if the snake hits the wall
        if self.snake.is_out_of_bounds(self.width, self.height, top_margin=40):
            print("Game Over: Snake hit the wall!")
            self.game_over = True
            return

        # End the game if the snake hits an obstacle
        head_rect = self.snake.get_head_rect()
        for obs in self.obstacles:
            if head_rect.colliderect(obs.get_rect()):
                print("Game Over: Snake hit an obstacle!")
                self.game_over = True
                return

        # End the game if the snake runs into itself
        if self.snake.check_self_collision():
            print("Game Over: Snake ran into itself!")
            self.game_over = True
            return

        # Check snake–food collision
        head_x, head_y = self.snake.segments[0]
        if head_x == self.food.x and head_y == self.food.y:
            # Snake eats food
            if self.food.is_special:
                # Special food: big bonus
                for _ in range(3):
                    self.snake.grow()        # grow by 3 segments total
                self.score += 20             # +20 points
                print(f"SPECIAL food eaten! Score is now {self.score}")
            else:
                # Normal food
                self.snake.grow()            # +1 segment
                self.score += 5              # +5 points
                print(f"Food eaten! Score is now {self.score}")

            # Respawn food somewhere safe (not on snake or obstacles)
            self._respawn_food_safely()

            # Update level
            self._update_level()

    def _draw_game_objects(self):
        """Draw snake, food, obstacles, and HUD during normal gameplay."""
        head_color, body_color = self._get_snake_colors_for_level()
        self.snake.draw(self.screen, head_color=head_color, body_color=body_color)
        self.food.draw(self.screen)
        for obs in self.obstacles:
            obs.draw(self.screen)

        # top HUD bar
        hud_height = 40
        hud_rect = pygame.Rect(0, 0, self.width, hud_height)
        pygame.draw.rect(self.screen, (25, 25, 35), hud_rect)

        # Score and Level text
        score_text = self.font_small.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        level_text = self.font_small.render(f"Level: {self.level}", True, (255, 255, 255))
        level_rect = level_text.get_rect(topright=(self.width - 10, 10))
        self.screen.blit(level_text, level_rect)

        # Paused message
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
        level_text = self.font_small.render(f"Final Level: {self.level}", True, (255, 255, 255))
        instr_text = self.font_small.render("Press R to restart or ESC to quit", True, (255, 255, 255))

        # Center the texts
        go_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 60))
        score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2 - 20))
        level_rect = level_text.get_rect(center=(self.width // 2, self.height // 2 + 20))
        instr_rect = instr_text.get_rect(center=(self.width // 2, self.height // 2 + 60))

        self.screen.blit(game_over_text, go_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(level_text, level_rect)
        self.screen.blit(instr_text, instr_rect)

    def draw(self):
        """Draws everything to the screen."""
        self.screen.fill((15, 15, 20))
        grid_color = (40, 40, 50) #grid lines
        cell_size = self.snake.block_size

        for x in range(0, self.width, cell_size):
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, self.height))
        for y in range(0, self.height, cell_size):
            pygame.draw.line(self.screen, grid_color, (0, y), (self.width, y))

        if not self.game_over:
            self._draw_game_objects()
        else:
            self._draw_game_over_screen()

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            # Speed increases (every level +1 FPS)
            dynamic_fps = self.base_speed + (self.level - 1)
            self.clock.tick(dynamic_fps)

        pygame.quit()
