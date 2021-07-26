from telegramBot import telegramBot
from configWorker import configWorker
from databaseWorker import databaseWorker
import telebot


def main():
    databaseWorker.check()
    configWorker.check()
    telegramBot.main()


if __name__ == "__main__":
    main()
