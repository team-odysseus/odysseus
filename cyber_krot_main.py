from bot.bot import set_bot_controller, bot_main
from bot.com_telegram import ComTelegram
from game.bot_controller import BotController

if __name__ == '__main__':
    bot_controller = BotController(ComTelegram())
    set_bot_controller(bot_controller)
    bot_main()
