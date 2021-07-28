import qrcode
import os.path
from configWorker.configWorker import getConfig


def makeQRCodeAndSave(ticketId: str):
    config = getConfig()
    qr = qrcode.QRCode(
        error_correction=qrcode.ERROR_CORRECT_H,
        border=2
    )
    qr.add_data(
        f"https://t.me/{config.get('Telegram', 'BOT_NAME')}?start={ticketId}")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(os.path.dirname(__file__) + f"/../outputQRCodes/{ticketId}.png")
