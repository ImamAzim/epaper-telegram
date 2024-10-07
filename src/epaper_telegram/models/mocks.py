import logging
from threading import Event


from PIL import Image


class SenderBotMock():

    def __init__(self, jabber_id, password, corresp_jid):
        pass

    def send_img(self, img):
        pass

    def terminate(self):
        pass


class ReceiverBotMock():

    _IMG_WIDTH = 122
    _IMG_HEIGHT = 250

    def __init__(self, jabber_id, password, corresp_jid):
        self._img = Image.new('1', (self._IMG_WIDTH, self._IMG_HEIGHT), 255)
        self._event = Event()

    @property
    def img(self):
        return self._img

    def wait_for_msg(self):
        self._event.clear()
        self._event.wait()

    def stop_waiting(self):
        self._event.set()
