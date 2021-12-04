import logging

from controller import Controller
from game import Game


def main():
    g = Game()
    g.join(1)
    g.join(2)
    g.join(3)

    c = Controller(g)
    c.game_loop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    main()
