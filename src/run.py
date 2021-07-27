from telegramBot import telegramBot
from configWorker import configWorker
from databaseWorker import databaseWorker


def main():
    databaseWorker.check()
    configWorker.check()
    telegramBot.main()


if __name__ == "__main__":
    main()
