from bot.bot import set_bot_controller, main
import game.bot_controller

if __name__ == '__main__':
    set_bot_controller(game.bot_controller.BotController())
    main()
