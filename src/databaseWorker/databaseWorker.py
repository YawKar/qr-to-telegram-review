import configparser
import sqlite3
from configWorker.configWorker import get_config
import os.path


def getConnectionAndCursor():
    config = get_config()
    con = sqlite3.connect(config.get("Database", "DIR"))
    cur = con.cursor()
    return con, cur


def isChatIdExists(chatId: str) -> bool:
    con, cur = getConnectionAndCursor()
    res = cur.execute(
        f"SELECT * FROM ChatsStage WHERE chatId = {chatId}").fetchall()
    cur.close(), con.close()
    return bool(res)


def setStage(chatId: str, stage: str) -> None:
    con, cur = getConnectionAndCursor()
    cur.execute(
        f"UPDATE ChatsStage SET stage = {stage} WHERE chatId = {chatId}")
    con.commit()
    cur.close(), con.close()


def getStage(chatId: str) -> str:
    con, cur = getConnectionAndCursor()
    res = cur.execute(
        f"SELECT * FROM ChatsStage WHERE chatId = {chatId}").fetchone()
    cur.close(), con.close()
    return res[1]


def check() -> None:
    con, cur = getConnectionAndCursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS ChatsStage
                   (chatId text, stage text)''')
    con.commit()
    cur.close(), con.close()


def addChatId(chatId: str) -> None:
    con, cur = getConnectionAndCursor()
    cur.execute(f"INSERT INTO ChatsStage VALUES ({chatId}, '0')")
    con.commit()
    cur.close(), con.close()
