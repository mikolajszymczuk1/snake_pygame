from random import randint

from pygame import QUIT, init
from pygame.display import flip, set_caption, set_mode
from pygame.draw import line
from pygame.event import get as get_events
from pygame.surface import Surface
from pygame.time import Clock

from app.game.config import Config
from app.sprites.apple import Apple
from app.sprites.player import Player


class Game:
    config: Config
    screen: Surface
    clock: Clock
    running: bool

    def __init__(self, config: Config) -> None:
        init()

        self.config: Config = config

        self.screen: Surface = set_mode((self.config.WIDTH, self.config.HEIGHT))
        set_caption(self.config.TITLE)

        self.clock: Clock = Clock()
        self.running: bool = True

        self.player: Player = Player(
            size=self.config.CELL_SIZE, x=10, y=10, color=self.config.GREEN
        )

        self.apple = Apple(size=self.config.CELL_SIZE, x=0, y=0, color=self.config.RED)

        self._generate_new_apple_position()

    def _draw_helper_grid(self) -> None:
        """
        Draw helper grid on the screen
        """

        for i in range(self.config.CELL_SIZE, self.config.WIDTH, self.config.CELL_SIZE):
            line(self.screen, self.config.GRAY, (i, 0), (i, self.config.HEIGHT))

        for j in range(
            self.config.CELL_SIZE, self.config.HEIGHT, self.config.CELL_SIZE
        ):
            line(self.screen, self.config.GRAY, (0, j), (self.config.WIDTH, j))

    def _events(self) -> None:
        """
        Game events
        """

        for event in get_events():
            if event.type == QUIT:
                self.running = False

    def _update(self, dt: float) -> None:
        """
        Any game logic
        """

        self.player.update(dt)
        self.player.check_board_bounds(self.config.WIDTH, self.config.HEIGHT)

        if self.player.check_apple_collision(self.apple):
            self._generate_new_apple_position()

    def _draw(self) -> None:
        """
        Draw everything on the screen
        """

        self.screen.fill(self.config.BLACK)

        # self._draw_helper_grid()

        self.player.draw(self.screen)

        self.apple.draw(self.screen)

        flip()

    def _generate_new_apple_position(self) -> None:
        """
        Generate new apple position
        """

        new_apple_x = (
            randint(0, self.config.WIDTH // self.config.CELL_SIZE - 1)
            * self.config.CELL_SIZE
        )

        new_apple_y = (
            randint(0, self.config.HEIGHT // self.config.CELL_SIZE - 1)
            * self.config.CELL_SIZE
        )

        if self.player.check_apple_generate_on_snake(new_apple_x, new_apple_y):
            self._generate_new_apple_position()
            return

        self.apple.x = new_apple_x
        self.apple.y = new_apple_y

    def run(self) -> None:
        """
        Main game loop
        """

        while self.running:
            dt: float = self.clock.tick(self.config.FPS) / 1000

            self._events()

            self._update(dt)

            self._draw()
