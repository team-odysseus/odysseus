import logging
from logging import log

from game import Game


def main():
    print("Hello World!")

    g = Game()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    main()
