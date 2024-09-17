
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
        cls.online_img_tool = OnlineImg(mock_mode=True)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_download(self):
        img = self.online_img_tool.download()
        self.assertIsInstance(img, Image.Image)

""" script tests """


def download():
    logging.basicConfig(level=logging.INFO)
    online_img_tool = OnlineImg()
    img = online_img_tool.download()
    img.show()


if __name__ == '__main__':
    download()
