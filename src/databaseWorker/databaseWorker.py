import configparser
import sqlite3
from configWorker.configWorker import get_config
import os.path


def getConnectionAndCursor():
    config = get_config()
    con = sqlite3.connect(config.get("Database", "DIR"))
    cur = con.cursor()
    return con, cur


def isChatIdExists(chat_id: str):
    con, cur = getConnectionAndCursor()
    res = cur.execute(
        f"SELECT * FROM ChatsStage WHERE chatId = {chat_id}").fetchall()
    cur.close(), con.close()


def setStage(chat_id: str, stage: str) -> None:
    con, cur = getConnectionAndCursor()
    cur.close(), con.close()


def getStage(chat_id: str) -> str:
    con, cur = getConnectionAndCursor()
    cur.close(), con.close()


def check() -> None:
    con, cur = getConnectionAndCursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS ChatsStage
                   (chatId text, stage text)''')
    cur.close(), con.close()
