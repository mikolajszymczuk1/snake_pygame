from pygame import QUIT, init
from pygame.display import flip, set_caption, set_mode
from pygame.event import get as get_events
from pygame.surface import Surface
from pygame.time import Clock

from app.game.config import Config
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

        self.player: Player = Player(size=40, x=100, y=100, color=self.config.GREEN)

    def run(self) -> None:
        """
        Main game loop
        """

        while self.running:
            dt: float = self.clock.tick(self.config.FPS) / 1000

            self._events()

            self._update(dt)

            self._draw()

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

    def _draw(self) -> None:
        """
        Draw everything on the screen
        """

        self.screen.fill(self.config.BLACK)

        self.player.draw(self.screen)

        flip()
