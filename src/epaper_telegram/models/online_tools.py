import configparser
import logging
from threading import Event, Timer
import os


from PIL import Image


from epaper_telegram.models.xmpp import ImageTransferBot, RegisterBot
from epaper_telegram import DATA_DIR_PATH, ACCOUNTS_CREATED_FILE


class OnlineImgError(Exception):
    pass


class OnlineImg(object):

    _IMG_WIDTH = 250
    _IMG_HEIGHT = 122
    _IMG_FILE_PATH = os.path.join(DATA_DIR_PATH, 'received_img.bmp')

    """manage online img"""
    def __init__(self,
            credentials,
            mock_mode=False,
            ):
        """TODO: to be defined.

        :credentials: dict to use for msg receiver (xmpp or webdav)
        :mock_mode: TODO

        """
        self._mock_mode = mock_mode

        self._wait_interrupted = False

        self._img_received = Event()
        if self._mock_mode:
            self._img = Image.new('1', (self._IMG_WIDTH, self._IMG_HEIGHT), 255)
        else:
            try:
                self._img = Image.open(self._IMG_FILE_PATH)
            except FileNotFoundError:
                self._img = None
        self._img_received.clear()

        path = os.path.join(DATA_DIR_PATH, ACCOUNTS_CREATED_FILE)
        config = configparser.ConfigParser()
        config.read(path)
        if credentials['jabber_id'] not in config:
            logging.info('need to register an account..')
            register_bot = RegisterBot(**credentials)
            register_bot.connect()
            register_bot.process(forever=False)
        self._image_transfer_bot = ImageTransferBot(**credentials, msg_receive_event=self._img_received)

    def wait_for_next_update(self):
        """will block until online img is new

        """
        self._wait_interrupted = False
        self._img_received.wait()
        if not self._wait_interrupted:
            try:
                self._img = Image.open(self._IMG_FILE_PATH)
            except FileNotFoundError:
                self._img = None
            self._img_received.clear()

    def stop_waiting(self):
        """stop the blocking wait even if there is no updated img

        """
        self._wait_interrupted = True
        self._img_received.set()

    def upload(self, img):
        """upload img on the cloud

        :img: PIL img object

        """
        self._image_transfer_bot.send_img(img)

    def get_latest_update_of_img(self):
        """return the img that was previouseley downloaded when update was detected
        :returns: PIL Image

        """
        if self._img is not None:
            return self._img
        else:
            msg = 'there is not last version of received img'
            logging.error(msg)
            raise OnlineImgError(msg)
