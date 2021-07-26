import telebot
from telebot.types import Message
from configWorker.configWorker import get_config


def main():
    config = get_config()
    tBot = telebot.TeleBot(config.get("Telegram", "TOKEN"))

    @tBot.message_handler(commands=['start'])
    def send_test(message: Message):
        given_uid = message.text.strip("/start").strip()
        if given_uid:
            tBot.send_message(
                message.chat.id, f"Здравствуйте, номер вашего отзыва: {given_uid}")
        else:
            tBot.send_message(
                message.chat.id, "Здравствуйте, это бот, собирающий отзывы")
    tBot.polling()
