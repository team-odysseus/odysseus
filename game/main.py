import logging
from logging import log

from game import Game


def main():
    print("Hello World!")

    g = Game()
    g.join(1)
    g.join(2)
    g.join(3)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    main()
