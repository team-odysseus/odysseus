import logging

from controller import Controller
from game import Game


def main():
    g = Game()

    # player1 id
    g.join(7374768)
    # player2 id
    g.join(8347838)
    # player3 id
    g.join(3)

    c = Controller(g)
    c.game_loop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    main()
