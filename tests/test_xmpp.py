import threading
import time
import logging


from PIL import Image, ImageDraw


from epaper_telegram.models.xmpp import CredentialsHandler
from epaper_telegram.models.xmpp import ReceiverBot, SenderBot


logging.basicConfig(level=logging.INFO)


credential_handler = CredentialsHandler()
try:
    credentials = credential_handler.load_credentials()
except FileNotFoundError:
    credential_handler.create_and_save_new_cred()
    credentials = credential_handler.load_credentials()


def send():
    corresp_jid = input('correspondant: ')

    sender = SenderBot(corresp_jid=corresp_jid, **credentials)

    img = Image.new('1', (200, 100), 255)
    draw = ImageDraw.Draw(img)
    draw.text((100, 50), 'salut!')
    sender.send_img(img)
    print('next')


def receive():
    corresp_jid = input('correspondant: ')
    receiver = ReceiverBot(corresp_jid=corresp_jid, **credentials)
    receiver.wait_for_msg()


def wait():
    corresp_jid = None
    receiver = ReceiverBot(corresp_jid=corresp_jid, **credentials)
    th = threading.Thread(target=receiver.wait_for_msg)
    th.start()
    # receiver.wait_for_msg()
    time.sleep(3)
    receiver.stop_waiting()


if __name__ == '__main__':
    receive()
