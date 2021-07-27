import telebot
from telebot.types import Message
from configWorker.configWorker import getConfig
import databaseWorker.databaseWorker as Dbw


def main():
    config = getConfig()
    tBot = telebot.TeleBot(config.get("Telegram", "TOKEN"))

    @tBot.message_handler(commands=['start'])
    def start_handler(message: Message):
        reviewId = message.text.strip("/start").strip()
        chatId = str(message.chat.id)
        if Dbw.isChatIdExists(chatId) == False:
            Dbw.addChatId(chatId)
        # пришли по ссылке ?start=reviewId или пришло сообщение вида "/start reviewId"
        if reviewId:
            # существует ли этот УИд товара в базе
            if Dbw.isReviewIdExists(reviewId):
                # состояние отзыва: уже написан или ожидает
                reviewIdStage = Dbw.getReviewIdStage(reviewId)
                # если статус ожидания
                if reviewIdStage == "wait":
                    Dbw.setChatIdStage(chatId, "waitForReview")
                    Dbw.setChatIdReviewId(chatId, reviewId)
                    tBot.send_message(
                        chatId, f"Номер текущего билета: {reviewId}.\nПожалуйста, напишите и отправьте свой отзыв.")
                # если отзыв уже был дан
                elif reviewIdStage == "complete":
                    tBot.send_message(
                        chatId, f"Билет с номером {reviewId} уже обработан и недоступен!")
            # этого УИд товара нет в базе
            else:
                tBot.send_message(
                    chatId, f"Билета с номером {reviewId} не существует!")
        # просто пришли в бота
        else:
            tBot.send_message(
                chatId, "Здравствуйте, этот бот обрабатывает отзывы. Перейдите по ссылке в QR коде.")

    @tBot.message_handler()
    def text_handler(message: Message):
        chatId = str(message.chat.id)
        text = message.text.strip()
        if Dbw.isChatIdExists(chatId) == False:
            Dbw.addChatId(chatId)
        chatIdStage = Dbw.getChatIdStage(chatId)
        # чат не закреплён за каким-то билетом
        if chatIdStage == "idle":
            tBot.send_message(
                chatId, "Здравствуйте, этот бот обрабатывает отзывы. Перейдите по ссылке в QR коде.")
        # ожидает написания отзыва
        elif chatIdStage == "waitForReview":
            reviewId = Dbw.getChatIdReviewId(chatId)
            reviewStage = Dbw.getReviewIdStage(reviewId)
            if reviewStage == "complete":
                tBot.send_message(
                    chatId, f"Билет с номером {reviewId} уже обработан и недоступен!")
            elif reviewStage == "wait":
                Dbw.setReviewIdChatId(reviewId, chatId)
                Dbw.setReviewIdMessage(reviewId, text)
                Dbw.setReviewIdStage(reviewId, "complete")

                Dbw.setChatIdReviewId(chatId, "0")
                Dbw.setChatIdStage(chatId, "idle")
                tBot.send_message(
                    chatId, f"Спасибо за ваш отзыв!")
    tBot.polling()
