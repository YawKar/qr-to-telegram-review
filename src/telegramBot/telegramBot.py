import telebot
from telebot.types import Message
from configWorker.configWorker import get_config
import databaseWorker.databaseWorker as Dbw


def main():
    config = get_config()
    tBot = telebot.TeleBot(config.get("Telegram", "TOKEN"))

    @tBot.message_handler(commands=['start'])
    def start_handler(message: Message):
        given_uid = message.text.strip("/start").strip()
        chatId = str(message.chat.id)
        if given_uid:
            if Dbw.isChatIdExists(chatId) == False:
                Dbw.addChatId(chatId)
            Dbw.setStage(chatId, '1')
            tBot.send_message(
                message.chat.id, f"Здравствуйте, номер вашего отзыва: {given_uid}, напишите отзыв:")
        else:
            tBot.send_message(
                message.chat.id, "Здравствуйте, это бот, собирающий отзывы")

    @tBot.message_handler()
    def text_handler(message: Message):
        chatId = message.chat.id
        text = message.text
        if Dbw.isChatIdExists(chatId):
            if Dbw.getStage(chatId) == '1':
                Dbw.setStage(chatId, '2')
                tBot.send_message(chatId, "Спасибо за ваш отзыв!")
        else:
            Dbw.addChatId(chatId)
            tBot.send_message(
                chatId, "Здравствуйте, это бот, собирающий отзывы")
    tBot.polling()
