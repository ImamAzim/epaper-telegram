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
    thread = sender.send_img(img)
    print('next')
    thread.join()
    # time.sleep(5)



def receive():
    corresp_jid = input('correspondant: ')
    receiver = ReceiverBot(corresp_jid=corresp_jid, **credentials)
    receiver.wait_for_msg()


def wait():
    corresp_jid = input('correspondant: ')
    receiver = ReceiverBot(corresp_jid=corresp_jid, **credentials)
    flag = threading.Event()
    flag.set()
    def wait_in_loop():
        while flag.is_set():
            receiver.wait_for_msg()
    th = threading.Thread(target=wait_in_loop)
    th.start()
    input()
    flag.clear()
    receiver.stop_waiting()


if __name__ == '__main__':
    wait()
