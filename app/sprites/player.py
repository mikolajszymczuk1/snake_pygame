from pygame import Rect, Surface
from pygame.draw import rect


class Player:
    def __init__(self, size: int, x: int, y: int, color: tuple[int, int, int]) -> None:
        self.size: int = size

        self.x: int = x
        self.y: int = y

        self.speed: int = 100

        self.color: tuple[int, int, int] = color

        self.rect = Rect(self.x, self.y, self.size, self.size)

    def _move(self, dt: float) -> None:
        self.rect.x += self.speed * dt

    def update(self, dt: float) -> None:
        self._move(dt)

    def draw(self, surface: Surface) -> None:
        rect(surface=surface, color=self.color, rect=self.rect)
