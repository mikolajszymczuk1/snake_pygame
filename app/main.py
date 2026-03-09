from app.game.app import Game
from app.game.config import Config


def main() -> None:
    config = Config()

    game = Game(config=config)

    game.run()


if __name__ == "__main__":
    main()
