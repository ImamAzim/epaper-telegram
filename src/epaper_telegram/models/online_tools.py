import logging
from threading import Event, Timer
import os


import xdg_base_dirs
from PIL import Image


APP_NAME = 'epaper-telegram'
DATA_DIR_PATH = os.path.join(xdg_base_dirs.xdg_data_home(), APP_NAME)
if not os.path.exists(DATA_DIR_PATH):
    os.makedirs(DATA_DIR_PATH)


class OnlineImgError(Exception):
    pass


class OnlineImg(object):

    _IMG_WIDTH = 250
    _IMG_HEIGHT = 122
    # _INTERVAL_BETWEEN_CHECKS = 1
    _IMG_FILE_PATH = os.path.join(DATA_DIR_PATH, 'received_img.bmp')

    """manage online img"""
    def __init__(self,
            upload_url=None,
            upload_username=None,
            upload_password=None,
            download_url=None,
            download_username=None,
            download_password=None,
            mock_mode=False,
            ):
        """TODO: to be defined.

        :upload_url: TODO
        :upload_username: TODO
        :upload_password: TODO
        :download_url: TODO
        :download_username: TODO
        :download_password: TODO
        :mock_mode: TODO
        :: TODO

        """
        self._upload_url = upload_url
        self._upload_username = upload_username
        self._upload_password = upload_password
        self._download_url = download_url
        self._download_username = download_username
        self._download_password = download_password
        self._mock_mode = mock_mode

        self._img_received = Event()
        try:
            self._img = Image.open(self._IMG_FILE_PATH)
        except FileNotFoundError:
            self._img = None

    def wait_for_next_update(self):
        """will block until online img is new

        """
        self._img_received.clear()
        # self._timer = Timer(
                # self._INTERVAL_BETWEEN_CHECKS,
                # lambda: self._img_received.set()
                # )
        # self._timer.start()
        self._img_received.wait()

    def stop_waiting(self):
        """stop the blocking wait even if there is no updated img

        """
        self._img_received.set()

    def upload(self, img):
        """upload img on the cloud

        :img: PIL img object

        """
        if self._mock_mode:
            logging.info('mock upload img')
        else:
            logging.debug('TODO: upload img')

    def download(self):
        """download img from the cloud
        :returns: PIL Image

        """
        if self._mock_mode:
            img = Image.new('1', (self._IMG_WIDTH, self._IMG_HEIGHT), 255)
        else:
            logging.debug('TODO: download img')
        return img
