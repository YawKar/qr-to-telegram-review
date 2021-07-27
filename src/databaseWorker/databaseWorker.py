import sqlite3
from typing import Tuple
from configWorker.configWorker import getConfig


def getConnectionAndCursor(type: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    '''
    Возвращает подключение и курсор на БД sqlite3
    '''
    config = getConfig()
    if type == "ChatsStage":
        con = sqlite3.connect(config.get("Database", "DIR_ChatsStage"))
    elif type == "Reviews":
        con = sqlite3.connect(config.get("Database", "DIR_Reviews"))
    else:
        raise Exception("type не найден")
    cur = con.cursor()
    return con, cur

##################### Для работы с чатами #####################


def addChatId(chatId: str) -> None:
    '''
    Добавляет пользователя в ChatsStage следующим образом:
    [chatId, 'idle', 0       ]
    '''
    con, cur = getConnectionAndCursor("ChatsStage")
    cur.execute(f"INSERT INTO ChatsStage VALUES (?, 'idle', '0')", [chatId])
    con.commit()
    cur.close(), con.close()


def isChatIdExists(chatId: str) -> bool:
    '''
    Возвращает True, если чат существует в базе ChatsStage,
    иначе возвращает False.
    '''
    con, cur = getConnectionAndCursor("ChatsStage")
    res = cur.execute(
        "SELECT * FROM ChatsStage WHERE chatId = ?", [chatId]).fetchall()
    cur.close(), con.close()
    return bool(res)


def setChatIdStage(chatId: str, stage: str) -> None:
    '''
    Устанавливает этап, на котором находится данный пользователь(chatId).
    '''
    con, cur = getConnectionAndCursor("ChatsStage")
    cur.execute(
        f"UPDATE ChatsStage SET stage = ? WHERE chatId = ?", [stage, chatId])
    con.commit()
    cur.close(), con.close()


def getChatIdStage(chatId: str) -> str:
    '''
    Возвращает этап, на котором находится пользователь(chatId).
    '''
    con, cur = getConnectionAndCursor("ChatsStage")
    res = cur.execute(
        f"SELECT * FROM ChatsStage WHERE chatId = ?", [chatId]).fetchone()
    cur.close(), con.close()
    return res[1]


def setChatIdReviewId(chatId: str, reviewId: str) -> None:
    '''
    Устанавливает, к какому билету сейчас привязан пользователь(chatId).
    '''
    con, cur = getConnectionAndCursor("ChatsStage")
    cur.execute(
        f"UPDATE ChatsStage SET reviewId = ? WHERE chatId = ?", [reviewId, chatId])
    con.commit()
    cur.close(), con.close()


def getChatIdReviewId(chatId: str) -> str:
    '''
    Возвращает номер билета, к которому привязан данный пользователь(chatId).
    '''
    con, cur = getConnectionAndCursor("ChatsStage")
    res = cur.execute(
        f"SELECT * FROM ChatsStage WHERE chatId = ?", [chatId]).fetchone()
    cur.close(), con.close()
    return res[2]

##################### Для работы с билетами #####################


def addReviewId(reviewId: str) -> None:
    '''
    Добавляет билет в Reviews следующим образом:
    [reviewId, '0', '', 'wait']
    '''
    con, cur = getConnectionAndCursor("Reviews")
    cur.execute("INSERT INTO Reviews VALUES (?, '0', '', 'wait')", [reviewId])
    con.commit()
    cur.close(), con.close()


def isReviewIdExists(reviewId: str) -> bool:
    '''
    Возвращает True, если УИд товара существует в базе Reviews,
    иначе возвращает False.
    '''
    con, cur = getConnectionAndCursor("Reviews")
    res = cur.execute(
        "SELECT * FROM Reviews WHERE reviewId = ?", [reviewId]).fetchall()
    cur.close(), con.close()
    return bool(res)


def getReviewIdStage(reviewId: str) -> str:
    '''
    Возвращает этап, на котором находится данный билет.
    '''
    con, cur = getConnectionAndCursor("Reviews")
    res = cur.execute(
        f"SELECT * FROM Reviews WHERE reviewId = ?", [reviewId]).fetchone()
    cur.close(), con.close()
    return res[3]


def setReviewIdStage(reviewId: str, stage: str) -> None:
    '''
    Устанавливает этап, на котором находится данный билет.
    '''
    con, cur = getConnectionAndCursor("Reviews")
    cur.execute(
        f"UPDATE Reviews SET stage = ? WHERE reviewId = ?", [stage, reviewId])
    con.commit()
    cur.close(), con.close()


def getReviewIdChatId(reviewId: str) -> str:
    '''
    Возвращает chatId пользователя, оставившего данный отзыв в билете.
    '''
    con, cur = getConnectionAndCursor("Reviews")
    res = cur.execute(
        f"SELECT * FROM Reviews WHERE reviewId = ?", [reviewId]).fetchone()
    cur.close(), con.close()
    return res[1]


def setReviewIdChatId(reviewId: str, chatId: str) -> None:
    '''
    Устанавливает chatId пользователя, оставившего данный отзыв в билете.
    '''
    con, cur = getConnectionAndCursor("Reviews")
    cur.execute(
        f"UPDATE Reviews SET ChatId = ? WHERE reviewId = ?", [chatId, reviewId])
    con.commit()
    cur.close(), con.close()


def getReviewIdMessage(reviewId: str) -> str:
    '''
    Возвращает текст отзыва, находящегося в данном билете.
    '''
    con, cur = getConnectionAndCursor("Reviews")
    res = cur.execute(
        f"SELECT * FROM Reviews WHERE reviewId = ?", [reviewId]).fetchone()
    cur.close(), con.close()
    return res[2]


def setReviewIdMessage(reviewId: str, message: str) -> None:
    '''
    Устанавливает текст отзыва, находящегося в данном билете.
    '''
    con, cur = getConnectionAndCursor("Reviews")
    cur.execute(
        f"UPDATE Reviews SET message = ? WHERE reviewId = ?", [message, reviewId])
    con.commit()
    cur.close(), con.close()


def check() -> None:
    '''
    Обеспечивает существование таблиц ChatsStage и Reviews.
    Если не находит, создаёт их.
    '''
    con, cur = getConnectionAndCursor("ChatsStage")
    cur.execute('''CREATE TABLE IF NOT EXISTS ChatsStage
                   (chatId text, stage text, reviewId text)''')
    con.commit()
    cur.close(), con.close()

    con, cur = getConnectionAndCursor("Reviews")
    cur.execute('''CREATE TABLE IF NOT EXISTS Reviews
                   (reviewId text, ChatId text, message text, stage text)''')
    con.commit()
    cur.close(), con.close()
