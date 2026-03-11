from pygame import Rect, Surface
from pygame.draw import rect


class GameObject:
    size: int
    color: tuple[int, int, int]
    rect: Rect

    def __init__(
        self, size: int, x: int | float, y: int | float, color: tuple[int, int, int]
    ) -> None:
        self.size: int = size

        self.color: tuple[int, int, int] = color

        self.rect = Rect(x * self.size, y * self.size, self.size, self.size)

    @property
    def x(self) -> float:
        return self.rect.x

    @x.setter
    def x(self, value: float) -> None:
        self.rect.x = value

    @property
    def y(self) -> float:
        return self.rect.y

    @y.setter
    def y(self, value: float) -> None:
        self.rect.y = value

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: Surface) -> None:
        rect(surface=surface, color=self.color, rect=self.rect)
