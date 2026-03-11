from pygame import K_DOWN, K_LEFT, K_RIGHT, K_UP, Surface, Vector2
from pygame.key import ScancodeWrapper, get_pressed

from app.sprites.apple import Apple
from app.sprites.game_object import GameObject
from app.sprites.tail import Tail


class Player(GameObject):
    speed: float
    time_since_last_move: float
    direction: Vector2
    next_direction: Vector2

    def __init__(self, size: int, x: int, y: int, color: tuple[int, int, int]) -> None:
        super().__init__(size, x, y, color)

        self.speed: float = 0.08  # move interval in seconds
        self.time_since_last_move: float = 0
        self.direction: Vector2 = Vector2(1, 0)
        self.next_direction: Vector2 = self.direction

        self.length: int = 3
        self.tail: list[Tail] = []

        self._create_base_tail()

    def _create_base_tail(self) -> None:
        for _ in range(self.length):
            self._grow()

    def _move(self, dt: float) -> None:
        self.time_since_last_move += dt

        if self.time_since_last_move >= self.speed:
            self.time_since_last_move = 0

            self._set_direction()

            self._move_tail()

            self.x += self.direction.x * self.size
            self.y += self.direction.y * self.size

    def _move_tail(self) -> None:
        last_segment: Tail = self.tail.pop()
        last_segment.x = self.x
        last_segment.y = self.y
        self.tail.insert(0, last_segment)

    def _set_direction(self) -> None:
        if self.next_direction + self.direction != Vector2(0, 0):
            self.direction: Vector2 = self.next_direction

    def _grow(self) -> None:
        tail: Tail = Tail(self.size, self.x, self.y, self.color)
        self.tail.append(tail)
        self.length += 1

    def _reset_body(self) -> None:
        self.length = 3
        self.tail.clear()
        self._create_base_tail()

    def _game_over(self) -> None:
        self._reset_body()
        self.x = 10 * self.size
        self.y = 10 * self.size
        self.direction = Vector2(1, 0)
        self.next_direction = self.direction

    def _handle_input(self) -> None:
        keys: ScancodeWrapper = get_pressed()

        if keys[K_LEFT]:
            self.next_direction = Vector2(-1, 0)

        elif keys[K_RIGHT]:
            self.next_direction = Vector2(1, 0)

        elif keys[K_UP]:
            self.next_direction = Vector2(0, -1)

        elif keys[K_DOWN]:
            self.next_direction = Vector2(0, 1)

    def _check_tail_collision(self) -> None:
        for tail in self.tail:
            if self.rect.colliderect(tail.rect):
                self._game_over()
                break

    def check_board_bounds(self, screen_width: int, screen_height: int) -> None:
        if self.x < 0 or self.x >= self.size * (screen_width // self.size):
            self._game_over()

        if self.y < 0 or self.y >= self.size * (screen_height // self.size):
            self._game_over()

    def check_apple_collision(self, apple: Apple) -> bool:
        if self.rect.colliderect(apple.rect):
            self._grow()
            return True

        return False

    def check_apple_generate_on_snake(self, apple_x: int, apple_y: int) -> bool:
        if self.x == apple_x and self.y == apple_y:
            return True

        return any(tail.x == apple_x and tail.y == apple_y for tail in self.tail)

    def update(self, dt: float) -> None:
        self._handle_input()
        self._move(dt)
        self._check_tail_collision()

    def draw(self, surface: Surface) -> None:
        super().draw(surface)

        for tail in self.tail:
            tail.draw(surface)
