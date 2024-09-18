
"""
test online tool module
"""

import unittest
from threading import RLock
import time
import logging


from PIL import Image, ImageDraw


from epaper_telegram.models.online_tools import OnlineImg


class TestMyClass(unittest.TestCase):

    """all test concerning OnlineImg """

    @classmethod
    def setUpClass(cls):
        credentials = dict()
        cls.online_img_tool = OnlineImg(credentials, mock_mode=True)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_get_latest_img(self):
        img = self.online_img_tool.get_latest_update_of_img()
        self.assertIsInstance(img, Image.Image)

""" script tests """


def download():
    logging.basicConfig(level=logging.INFO)
    credentials = dict()
    online_img_tool = OnlineImg(credentials)
    img = online_img_tool.get_latest_update_of_img()
    img.show()


if __name__ == '__main__':
    download()
